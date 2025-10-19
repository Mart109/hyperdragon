import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path
from typing import Optional
import json
from datetime import datetime
import traceback

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if record.exc_info:
            log_data["exception"] = traceback.format_exc()
        
        return json.dumps(log_data)

def setup_logger(
    name: str = "hype_drakon",
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5
) -> logging.Logger:
    """Настройка комплексного логгера с консольным и файловым выводом"""
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Очистка существующих обработчиков
    logger.handlers.clear()
    
    # Форматтер для консоли
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Файловый обработчик с ротацией
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    # Перехват uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        logger.critical(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_traceback)
    
    sys.excepthook = handle_exception
    
    return logger

# Инициализация глобального логгера
logger = setup_logger()