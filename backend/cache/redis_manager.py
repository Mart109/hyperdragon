import redis.asyncio as redis
from functools import lru_cache
from typing import Optional, Union
import logging
from backend.config import settings

class RedisConnectionError(Exception):
    pass

class RedisManager:
    _instance: Optional['RedisManager'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.pool = None
        self.logger = logging.getLogger('redis')
        self._connect()

    def _connect(self):
        try:
            self.pool = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                max_connections=100
            )
            self.logger.info("Redis connection pool initialized")
        except Exception as e:
            self.logger.error(f"Redis connection failed: {str(e)}")
            raise RedisConnectionError("Failed to connect to Redis")

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.logger.info("Redis connection closed")

    async def execute_command(self, command: str, *args, **kwargs) -> Union[str, int, list, None]:
        try:
            async with self.pool.client() as conn:
                method = getattr(conn, command)
                return await method(*args, **kwargs)
        except redis.RedisError as e:
            self.logger.error(f"Redis command failed: {command} - {str(e)}")
            raise

    async def set_with_ttl(self, key: str, value: str, ttl: int = 3600) -> bool:
        return await self.execute_command('setex', key, ttl, value)

    async def get_or_set(self, key: str, value_fn, ttl: int = 3600) -> str:
        cached = await self.execute_command('get', key)
        if cached is not None:
            return cached.decode('utf-8')
        
        fresh_value = await value_fn()
        await self.set_with_ttl(key, str(fresh_value), ttl)
        return str(fresh_value)

    async def acquire_lock(self, lock_name: str, timeout: int = 10) -> bool:
        return await self.execute_command('set', f"lock:{lock_name}", "1", nx=True, ex=timeout)

    async def release_lock(self, lock_name: str) -> None:
        await self.execute_command('del', f"lock:{lock_name}")

@lru_cache(maxsize=1)
def get_redis_manager() -> RedisManager:
    return RedisManager()