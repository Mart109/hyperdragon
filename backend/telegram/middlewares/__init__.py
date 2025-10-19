from aiogram import Dispatcher
from aiogram.types import Update
from typing import Callable, Dict, Any, Awaitable
import logging
import time

logger = logging.getLogger(__name__)

class AntiSpamMiddleware:
    def __init__(self):
        self.user_requests = {}
        
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()
        
        # Проверяем частоту запросов
        if user_id in self.user_requests:
            last_request = self.user_requests[user_id]
            if current_time - last_request < 0.5:  # 2 запроса в секунду
                logger.warning(f"Spam detected from user {user_id}")
                return
        
        self.user_requests[user_id] = current_time
        return await handler(event, data)

class LoggingMiddleware:
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        logger.info(f"Processing update from user {user_id}")
        
        try:
            result = await handler(event, data)
            logger.info(f"Successfully processed update from user {user_id}")
            return result
        except Exception as e:
            logger.error(f"Error processing update from user {user_id}: {e}")
            raise

def register_middlewares(dp: Dispatcher):
    """Регистрация middleware"""
    
    # Анти-спам
    dp.update.outer_middleware(AntiSpamMiddleware())
    
    # Логирование
    dp.update.outer_middleware(LoggingMiddleware())
    
    logger.info("✅ Middlewares registered")