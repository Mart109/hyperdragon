from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()

@router.errors()
async def error_handler(event: ErrorEvent):
    logger.error(f"Error: {event.exception}")
    await event.update.message.answer("⚠️ Произошла ошибка. Попробуйте позже.")