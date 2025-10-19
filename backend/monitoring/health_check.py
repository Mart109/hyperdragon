from typing import Dict, Any, Tuple
import asyncio
import aiohttp
from dataclasses import dataclass
from ..utils.logger import logger
from ..database.db import Database
from ..config import settings

@dataclass
class HealthStatus:
    """Статус компонента системы"""
    name: str
    status: bool
    details: Dict[str, Any]
    critical: bool = True

class HealthChecker:
    """Комплексная проверка состояния системы"""
    
    def __init__(self, db: Database):
        self.db = db
        self.components = [
            ("database", self.check_database),
            ("cache", self.check_cache),
            ("external_api", self.check_external_apis),
            ("storage", self.check_storage)
        ]
    
    async def check_database(self) -> HealthStatus:
        """Проверка подключения к БД"""
        try:
            start = asyncio.get_event_loop().time()
            await self.db.execute("SELECT 1")
            latency = asyncio.get_event_loop().time() - start
            
            return HealthStatus(
                name="database",
                status=True,
                details={"latency": latency},
                critical=True
            )
        except Exception as e:
            return HealthStatus(
                name="database",
                status=False,
                details={"error": str(e)},
                critical=True
            )
    
    async def check_cache(self) -> HealthStatus:
        """Проверка кэша (если используется)"""
        # Реализация зависит от используемого кэша
        return HealthStatus(
            name="cache",
            status=True,
            details={},
            critical=False
        )
    
    async def check_external_apis(self) -> HealthStatus:
        """Проверка доступности внешних API"""
        apis = {
            "telegram": settings.TELEGRAM_API_URL,
            "payment": settings.PAYMENT_API_URL
        }
        
        results = {}
        async with aiohttp.ClientSession() as session:
            for name, url in apis.items():
                try:
                    async with session.get(url, timeout=2) as resp:
                        results[name] = resp.status == 200
                except Exception as e:
                    results[name] = False
        
        return HealthStatus(
            name="external_apis",
            status=all(results.values()),
            details=results,
            critical=True
        )
    
    async def check_storage(self) -> HealthStatus:
        """Проверка доступности хранилища"""
        # Проверка дискового пространства и т.д.
        return HealthStatus(
            name="storage",
            status=True,
            details={"free_space": "100GB"},  # Пример
            critical=True
        )
    
    async def full_check(self) -> Tuple[bool, Dict[str, HealthStatus]]:
        """Полная проверка всех компонентов"""
        results = {}
        
        for name, checker in self.components:
            try:
                status = await checker()
                results[name] = status
            except Exception as e:
                logger.error(f"Health check failed for {name}: {str(e)}")
                results[name] = HealthStatus(
                    name=name,
                    status=False,
                    details={"error": str(e)},
                    critical=True
                )
        
        overall_status = all(
            status.status or not status.critical
            for status in results.values()
        )
        
        return overall_status, results

    async def get_status_page(self) -> Dict[str, Any]:
        """Генерация статусной страницы в формате JSON"""
        overall, details = await self.full_check()
        
        return {
            "status": "healthy" if overall else "degraded",
            "components": {
                name: {
                    "status": "up" if comp.status else "down",
                    "details": comp.details,
                    "critical": comp.critical
                }
                for name, comp in details.items()
            }
        }