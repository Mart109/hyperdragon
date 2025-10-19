import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties

from backend.config import Config
from backend.database.db import Database
from backend.game.combat import Combat

# Импорты из твоей структуры
from backend.telegram.handlers import register_handlers
from backend.telegram.middlewares import register_middlewares

logger = logging.getLogger(__name__)

def setup_bot(dp: Dispatcher, db: Database, combat: Combat, config: Config):
    """Настройка бота"""
    try:
        # Регистрация middleware
        register_middlewares(dp)
        
        # Регистрация обработчиков (из твоего __init__.py)
        register_handlers(dp)
        
        logger.info("✅ Bot setup completed")
        
    except Exception as e:
        logger.error(f"Bot setup failed: {e}")
        raise

async def start_bot():
    """Запуск бота"""
    try:
        config = Config()
        
        # Создаем бота
        bot = Bot(
            token=config.TELEGRAM.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML")
        )
        
        # Создаем хранилище и диспетчер
        storage = RedisStorage.from_url(config.REDIS.URL)
        dp = Dispatcher(storage=storage)
        
        # Инициализация компонентов
        db = Database()
        combat = Combat(db)
        
        # Настройка бота
        setup_bot(dp, db, combat, config)
        
        # Запуск
        logger.info("Bot starting...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.critical(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_bot())