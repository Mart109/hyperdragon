import inspect
import json
from functools import wraps
from typing import Callable, Any, Optional, TypeVar, Coroutine
import hashlib
from backend.cache.redis_manager import get_redis_manager
from backend.config import settings

T = TypeVar('T')

class CacheMiss(Exception):
    pass

def cache_key_generator(func: Callable, *args, **kwargs) -> str:
    func_name = func.__qualname__
    arg_names = inspect.getfullargspec(func).args
    args_dict = {
        **dict(zip(arg_names, args)),
        **kwargs
    }
    args_json = json.dumps(args_dict, sort_keys=True)
    return f"cache:{func_name}:{hashlib.md5(args_json.encode()).hexdigest()}"

def async_cache(
    ttl: int = 3600,
    key_func: Optional[Callable] = None,
    cache_none: bool = False
) -> Callable[[Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]]:
    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            if settings.CACHE_DISABLED:
                return await func(*args, **kwargs)

            redis = get_redis_manager()
            key = key_func(*args, **kwargs) if key_func else cache_key_generator(func, *args, **kwargs)

            try:
                cached = await redis.execute_command('get', key)
                if cached is not None:
                    return json.loads(cached.decode('utf-8'))
            except Exception as e:
                logging.warning(f"Cache read failed: {str(e)}")

            result = await func(*args, **kwargs)

            if result is None and not cache_none:
                return result

            try:
                await redis.set_with_ttl(key, json.dumps(result), ttl)
            except Exception as e:
                logging.warning(f"Cache write failed: {str(e)}")

            return result
        return wrapper
    return decorator

def cache_invalidate(*keys: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = get_redis_manager()
            result = await func(*args, **kwargs)
            
            try:
                for key_pattern in keys:
                    keys_to_delete = await redis.execute_command('keys', key_pattern)
                    if keys_to_delete:
                        await redis.execute_command('del', *keys_to_delete)
            except Exception as e:
                logging.warning(f"Cache invalidation failed: {str(e)}")
            
            return result
        return wrapper
    return decorator