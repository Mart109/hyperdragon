import asyncio
from typing import Dict, Callable, Coroutine, Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from ..monitoring.metrics import track_task_execution
from ..utils.logger import logger

class TaskScheduler:
    """Управление периодическими и отложенными задачами"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.jobs: Dict[str, str] = {}  # name: job_id
        
    async def start(self):
        """Запуск планировщика"""
        try:
            self.scheduler.start()
            logger.info("Task scheduler started")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
            raise

    async def shutdown(self):
        """Корректное завершение работы"""
        try:
            self.scheduler.shutdown()
            logger.info("Task scheduler stopped")
        except Exception as e:
            logger.error(f"Failed to shutdown scheduler: {str(e)}")
            raise

    def add_cron_job(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        name: str,
        cron_expr: str,
        *args, **kwargs
    ) -> str:
        """Добавление периодической задачи по cron-расписанию"""
        try:
            job = self.scheduler.add_job(
                self._wrap_task(func, name),
                trigger=CronTrigger.from_crontab(cron_expr),
                *args, **kwargs
            )
            self.jobs[name] = job.id
            return job.id
        except Exception as e:
            logger.error(f"Failed to add cron job {name}: {str(e)}")
            raise

    def add_interval_job(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        name: str,
        minutes: int = 0,
        seconds: int = 0,
        *args, **kwargs
    ) -> str:
        """Добавление задачи с интервальным выполнением"""
        try:
            job = self.scheduler.add_job(
                self._wrap_task(func, name),
                trigger=IntervalTrigger(
                    minutes=minutes,
                    seconds=seconds
                ),
                *args, **kwargs
            )
            self.jobs[name] = job.id
            return job.id
        except Exception as e:
            logger.error(f"Failed to add interval job {name}: {str(e)}")
            raise

    async def _wrap_task(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        name: str
    ) -> None:
        """Обертка для задач с обработкой ошибок и метриками"""
        try:
            logger.info(f"Starting task: {name}")
            start_time = asyncio.get_event_loop().time()
            
            await func()
            
            duration = asyncio.get_event_loop().time() - start_time
            track_task_execution(name, "success", duration)
            logger.info(f"Task completed: {name}")
            
        except Exception as e:
            track_task_execution(name, "failed", 0)
            logger.error(f"Task failed {name}: {str(e)}", exc_info=True)