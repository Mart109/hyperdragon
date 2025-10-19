from typing import Any, Callable, Coroutine, Optional
from functools import wraps
from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError
import asyncio
from ..monitoring.metrics import track_error

class ErrorHandler:
    """Комплексный обработчик ошибок для разных сценариев"""
    
    @staticmethod
    def database_retry(max_retries: int = 3, delay: float = 1.0):
        def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                last_error = None
                for attempt in range(1, max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_error = e
                        track_error("database", str(e))
                        if attempt < max_retries:
                            await asyncio.sleep(delay * attempt)
                        continue
                raise last_error if last_error else Exception("Unknown error")
            return wrapper
        return decorator

    @staticmethod
    async def telegram_error_handler(
        update: Optional[types.Update],
        context: types.ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Централизованный обработчик ошибок Telegram"""
        error = context.error
        chat_id = update.effective_chat.id if update else None
        
        error_messages = {
            "TimeoutError": "Превышено время ожидания ответа",
            "NetworkError": "Проблемы с сетью, попробуйте позже",
            "DatabaseError": "Ошибка доступа к данным",
            "PermissionError": "Недостаточно прав",
            "TelegramAPIError": "Ошибка Telegram API"
        }
        
        message = error_messages.get(
            error.__class__.__name__,
            "Произошла непредвиденная ошибка"
        )
        
        if chat_id:
            try:
                await context.bot.send_message(chat_id, message)
            except Exception as e:
                track_error("telegram", f"Failed to send error message: {str(e)}")
        
        track_error("application", f"{error.__class__.__name__}: {str(error)}")

    @staticmethod
    def graceful_shutdown(
        signals: tuple = (SIGINT, SIGTERM)
    ) -> Callable:
        """Декоратор для graceful shutdown обработчиков"""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                loop = asyncio.get_running_loop()
                
                for sig in signals:
                    loop.add_signal_handler(
                        sig,
                        lambda: asyncio.create_task(
                            shutdown_handler(sig, func)
                        )
                    )
                
                try:
                    return await func(*args, **kwargs)
                finally:
                    # Cleanup logic
                    pass
            
            async def shutdown_handler(sig, func):
                logger.info(f"Received exit signal {sig.name}...")
                # Добавить логику завершения
                await func.close()  # Предполагаем что у func есть close()
                
            return wrapper
        return decorator