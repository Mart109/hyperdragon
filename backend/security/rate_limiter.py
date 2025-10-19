import time
from typing import Callable, Optional, Tuple
from functools import wraps
from enum import Enum
from backend.cache.redis_manager import get_redis_manager
from aiogram import types
from backend.config import settings

class RateLimitExceeded(Exception):
    def __init__(self, retry_after: float):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Try again in {retry_after:.1f} seconds")

class RateLimitScope(Enum):
    USER = "user"
    CHAT = "chat"
    GLOBAL = "global"

def get_identifier(scope: RateLimitScope, update: types.Update) -> str:
    if scope == RateLimitScope.USER:
        user = update.message.from_user if update.message else update.callback_query.from_user
        return f"user:{user.id}"
    elif scope == RateLimitScope.CHAT:
        chat = update.message.chat if update.message else update.callback_query.message.chat
        return f"chat:{chat.id}"
    return "global"

def rate_limit(
    calls: int,
    period: float,
    scope: RateLimitScope = RateLimitScope.USER,
    key: Optional[str] = None,
    exempt_admins: bool = True
):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(update: types.Update, *args, **kwargs):
            if exempt_admins:
                user = update.message.from_user if update.message else update.callback_query.from_user
                if user.id in settings.ADMIN_IDS:
                    return await handler(update, *args, **kwargs)

            redis = get_redis_manager()
            identifier = key if key else get_identifier(scope, update)
            rate_key = f"rate:{identifier}:{handler.__name__}"

            try:
                current = await redis.execute_command('llen', rate_key)
                if current >= calls:
                    oldest = float(await redis.execute_command('lindex', rate_key, 0))
                    retry_after = period - (time.time() - oldest)
                    if retry_after > 0:
                        raise RateLimitExceeded(retry_after)
                    await redis.execute_command('lpop', rate_key)

                await redis.execute_command('rpush', rate_key, time.time())
                await redis.execute_command('expire', rate_key, int(period))
            except Exception as e:
                if not isinstance(e, RateLimitExceeded):
                    logging.error(f"Rate limit error: {str(e)}")
                raise

            return await handler(update, *args, **kwargs)
        return wrapper
    return decorator

class AdaptiveRateLimiter:
    def __init__(self):
        self.thresholds = {
            'low': (10, 60),
            'medium': (30, 60),
            'high': (60, 60)
        }
        self.user_states = {}

    async def check_rate(self, user_id: int) -> Tuple[int, float]:
        current_time = time.time()
        state = self.user_states.get(user_id, {'count': 0, 'last_time': current_time})
        
        time_diff = current_time - state['last_time']
        if time_diff > 60:
            state = {'count': 0, 'last_time': current_time}
        
        state['count'] += 1
        self.user_states[user_id] = state
        
        for level, (max_calls, period) in self.thresholds.items():
            if state['count'] > max_calls:
                return max_calls, period
        
        return 0, 0