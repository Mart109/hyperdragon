#!/usr/bin/env python3
import asyncio
import signal
import logging
import sys
from contextlib import asynccontextmanager
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties

from backend.config import Config, load_config, setup_logging
from backend.database.db import Database
from backend.game.combat import Combat
from backend.telegram.bot import setup_bot
from backend.telegram.middlewares import register_middlewares
from backend.cache.redis_manager import RedisManager
from backend.monitoring.metrics import setup_metrics
from backend.monitoring.health_check import HealthChecker
from backend.utils.task_scheduler import TaskScheduler

logger = logging.getLogger(__name__)

class Application:
    def __init__(self):
        self.config: Optional[Config] = None
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.db: Optional[Database] = None
        self.redis: Optional[RedisManager] = None
        self.combat: Optional[Combat] = None
        self.scheduler: Optional[TaskScheduler] = None
        self.health_checker: Optional[HealthChecker] = None
        self._shutdown_event = asyncio.Event()

    @asynccontextmanager
    async def lifespan(self):
        """Управление жизненным циклом приложения"""
        await self.startup()
        try:
            yield
        finally:
            await self.shutdown()

    async def startup(self):
        """Инициализация всех компонентов"""
        logger.info("🚀 Starting Hype Drakon application...")
        
        try:
            # 1. Загрузка конфигурации
            self.config = load_config()
            logger.info(f"📍 Environment: {self.config.ENVIRONMENT.value}")
            
            # 2. Инициализация Redis
            logger.info("🔗 Connecting to Redis...")
            self.redis = RedisManager(self.config.REDIS.URL)
            await self.redis.connect()
            storage = RedisStorage(self.redis.connection)
            logger.info("✅ Redis connected successfully")
            
            # 3. Инициализация базы данных
            logger.info("🗄️ Initializing database...")
            self.db = Database()
            # Проверяем соединение с БД
            test_connection = self.db.fetch_one("SELECT 1 as test")
            if test_connection:
                logger.info("✅ Database connected successfully")
            else:
                raise Exception("Failed to connect to database")
            
            # 4. Инициализация игровых систем
            logger.info("⚔️ Initializing combat system...")
            self.combat = Combat(self.db)
            logger.info("✅ Combat system initialized")
            
            # 5. Настройка бота
            logger.info("🤖 Setting up Telegram bot...")
            default = DefaultBotProperties(parse_mode="HTML")
            self.bot = Bot(
                token=self.config.TELEGRAM.BOT_TOKEN,
                default=default
            )
            self.dp = Dispatcher(storage=storage)
            
            # 6. Регистрация middleware и обработчиков
            logger.info("🔧 Registering middlewares...")
            register_middlewares(self.dp, self.db, self.redis, self.config)
            
            logger.info("🔄 Setting up bot handlers...")
            setup_bot(self.dp, self.db, self.combat, self.config)
            logger.info("✅ Bot setup completed")
            
            # 7. Настройка мониторинга
            if self.config.MONITORING.ENABLE_METRICS:
                logger.info("📊 Setting up metrics...")
                setup_metrics()
                logger.info("✅ Metrics setup completed")
            
            # 8. Инициализация планировщика задач
            logger.info("⏰ Starting task scheduler...")
            self.scheduler = TaskScheduler()
            await self.scheduler.start()
            
            # 9. Настройка health checks
            self.health_checker = HealthChecker(self.db, self.redis)
            await self.scheduler.add_interval_job(
                self.health_checker.full_check,
                name="health_check",
                minutes=5
            )
            logger.info("✅ Health checks configured")
            
            # 10. Обработка сигналов завершения
            self._setup_signal_handlers()
            
            logger.info("🎉 Application started successfully!")
            logger.info(f"👤 Bot username: @{self.config.TELEGRAM.BOT_USERNAME}")
            logger.info(f"📍 Environment: {self.config.ENVIRONMENT.value}")
            
        except Exception as e:
            logger.critical(f"❌ Application startup failed: {e}", exc_info=True)
            await self.shutdown()
            sys.exit(1)

    async def shutdown(self):
        """Корректное завершение работы"""
        logger.info("🛑 Shutting down application...")
        
        shutdown_tasks = []
        
        # 1. Остановка планировщика задач
        if self.scheduler:
            logger.info("⏰ Stopping task scheduler...")
            shutdown_tasks.append(self.scheduler.stop())
        
        # 2. Остановка бота
        if self.bot:
            logger.info("🤖 Stopping bot...")
            await self.bot.session.close()
        
        # 3. Закрытие Redis
        if self.redis:
            logger.info("🔗 Closing Redis connection...")
            shutdown_tasks.append(self.redis.disconnect())
        
        # 4. Закрытие соединений с БД
        if self.db:
            logger.info("🗄️ Closing database connections...")
            self.db.conn.close()
        
        # Ждем завершения всех асинхронных задач
        if shutdown_tasks:
            await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        
        logger.info("✅ Application shutdown complete")

    def _setup_signal_handlers(self):
        """Настройка обработчиков сигналов"""
        loop = asyncio.get_running_loop()
        
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self._handle_shutdown_signal, sig)

    def _handle_shutdown_signal(self, signum):
        """Обработчик сигналов завершения"""
        signal_name = signal.Signals(signum).name
        logger.info(f"📡 Received signal: {signal_name}")
        self._shutdown_event.set()

    async def _run_webhook(self):
        """Запуск в webhook режиме (для production)"""
        if not self.config.TELEGRAM.WEBHOOK_URL:
            raise ValueError("WEBHOOK_URL is required for production mode")
        
        webhook_url = f"{self.config.TELEGRAM.WEBHOOK_URL}{self.config.TELEGRAM.WEBHOOK_PATH}"
        
        # Устанавливаем webhook
        await self.bot.set_webhook(
            url=webhook_url,
            secret_token=self.config.TELEGRAM.WEBHOOK_SECRET if hasattr(self.config.TELEGRAM, 'WEBHOOK_SECRET') else None
        )
        
        logger.info(f"🌐 Webhook set to: {webhook_url}")
        
        # Здесь должна быть интеграция с ASGI сервером (FastAPI, etc.)
        # Для простоты пока используем polling в production
        logger.warning("⚠️ Webhook mode not fully implemented, falling back to polling")
        await self._run_polling()

    async def _run_polling(self):
        """Запуск в polling режиме"""
        logger.info("🔄 Starting bot in polling mode...")
        
        # Очищаем webhook если он был установлен
        await self.bot.delete_webhook(drop_pending_updates=True)
        
        await self.dp.start_polling(
            self.bot,
            allowed_updates=self.dp.resolve_used_update_types(),
            handle_signals=False
        )

    async def run(self):
        """Основной цикл приложения"""
        async with self.lifespan():
            try:
                if self.config.is_production:
                    await self._run_webhook()
                else:
                    await self._run_polling()
                
                # Ждем сигнала завершения
                await self._shutdown_event.wait()
                
            except Exception as e:
                logger.critical(f"💥 Fatal error in main loop: {e}", exc_info=True)
                raise


async def main():
    """Точка входа в приложение"""
    app = Application()
    
    try:
        await app.run()
    except KeyboardInterrupt:
        logger.info("👋 Application interrupted by user")
    except Exception as e:
        logger.critical(f"💥 Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("👋 Application stopped")


if __name__ == "__main__":
    # Настройка логирования перед запуском
    config = load_config()
    setup_logging(config)
    
    # Запуск приложения
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Application stopped by user")
    except Exception as e:
        logger.critical(f"💥 Failed to start application: {e}", exc_info=True)
        sys.exit(1)