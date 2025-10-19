from prometheus_client import (
    start_http_server,
    Counter,
    Gauge,
    Histogram,
    Summary,
    Enum
)
import time
from typing import Optional, Literal
from ..utils.logger import logger

class GameMetrics:
    """Класс для сбора игровых метрик"""
    
    def __init__(self, port: int = 8000):
        self.port = port
        
        # Инициализация метрик
        self.requests_total = Counter(
            'game_requests_total',
            'Total game API requests',
            ['endpoint', 'method']
        )
        
        self.errors_total = Counter(
            'game_errors_total',
            'Total errors',
            ['error_type']
        )
        
        self.active_users = Gauge(
            'game_active_users',
            'Currently active users'
        )
        
        self.request_latency = Histogram(
            'game_request_latency_seconds',
            'Request latency',
            ['endpoint'],
            buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
        )
        
        self.task_duration = Summary(
            'game_task_duration_seconds',
            'Background task duration',
            ['task_name']
        )
        
        self.game_state = Enum(
            'game_state',
            'Current game state',
            states=['normal', 'maintenance', 'degraded']
        )
        
    def start_exporter(self):
        """Запуск HTTP сервера для экспорта метрик"""
        try:
            start_http_server(self.port)
            logger.info(f"Metrics server started on port {self.port}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {str(e)}")
            raise

    def track_error(self, error_type: str):
        """Регистрация ошибки"""
        self.errors_total.labels(error_type=error_type).inc()

    def track_request(self, endpoint: str, method: str = "GET"):
        """Регистрация запроса"""
        self.requests_total.labels(endpoint=endpoint, method=method).inc()

    def track_latency(self, endpoint: str, latency: float):
        """Регистрация времени выполнения"""
        self.request_latency.labels(endpoint=endpoint).observe(latency)

    def track_task_execution(
        self,
        task_name: str,
        status: Literal["success", "failed"],
        duration: float
    ):
        """Регистрация выполнения фоновой задачи"""
        if status == "success":
            self.task_duration.labels(task_name=task_name).observe(duration)
        self.errors_total.labels(error_type=f"task_{task_name}_{status}").inc()

    def set_active_users(self, count: int):
        """Установка количества активных пользователей"""
        self.active_users.set(count)

    def set_game_state(self, state: Literal["normal", "maintenance", "degraded"]):
        """Установка состояния игры"""
        self.game_state.state(state)

# Глобальный экземпляр метрик
metrics = GameMetrics()
track_error = metrics.track_error
track_task_execution = metrics.track_task_execution