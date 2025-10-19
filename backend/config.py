import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Загрузка .env из корня проекта
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

class DragonType(str, Enum):
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"
    ICE = "ice"
    STORM = "storm"

@dataclass
class DatabaseConfig:
    """Конфигурация базы данных"""
    URL: str = os.getenv("DATABASE_URL", "sqlite:///./game.db")
    ECHO: bool = os.getenv("DB_ECHO", "False").lower() == "true"
    POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))

@dataclass
class RedisConfig:
    """Конфигурация Redis"""
    HOST: str = os.getenv("REDIS_HOST", "localhost")
    PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    DB: int = int(os.getenv("REDIS_DB", "0"))
    URL: str = f"redis://{HOST}:{PORT}/{DB}"

@dataclass
class TelegramConfig:
    """Конфигурация Telegram бота"""
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "")
    ADMINS: List[int] = None
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")
    
    def __post_init__(self):
        if self.ADMINS is None:
            admins_str = os.getenv("ADMINS", "")
            self.ADMINS = [int(id.strip()) for id in admins_str.split(",") if id.strip()]

@dataclass
class GameEconomyConfig:
    """Конфигурация игровой экономики"""
    BASE_DAMAGE: int = int(os.getenv("BASE_DAMAGE", "10"))
    CRIT_CHANCE: float = float(os.getenv("CRIT_CHANCE", "0.1"))
    CRIT_MULTIPLIER: float = float(os.getenv("CRIT_MULTIPLIER", "2.0"))
    
    # Награды
    REFERRAL_BONUS: int = int(os.getenv("REFERRAL_BONUS", "100"))
    PVP_WIN_REWARD: int = int(os.getenv("PVP_WIN_REWARD", "50"))
    PVP_DRAW_REWARD: int = int(os.getenv("PVP_DRAW_REWARD", "10"))
    DAILY_BONUS: int = int(os.getenv("DAILY_BONUS", "200"))
    
    # Лимиты
    MAX_COINS_TRANSFER: int = int(os.getenv("MAX_COINS_TRANSFER", "10000"))
    TRANSACTION_FEE: float = float(os.getenv("TRANSACTION_FEE", "0.05"))
    MAX_TAPS_PER_MINUTE: int = int(os.getenv("MAX_TAPS_PER_MINUTE", "60"))

@dataclass
class DragonConfig:
    """Конфигурация драконов"""
    BASE_ATTACK: int = int(os.getenv("DRAGON_BASE_ATTACK", "10"))
    BASE_DEFENSE: int = int(os.getenv("DRAGON_BASE_DEFENSE", "5"))
    BASE_HEALTH: int = int(os.getenv("DRAGON_BASE_HEALTH", "100"))
    BASE_PRICE: int = int(os.getenv("DRAGON_BASE_PRICE", "500"))
    
    # Множители типов
    TYPE_MULTIPLIERS: Dict[str, Dict[str, float]] = None
    
    def __post_init__(self):
        if self.TYPE_MULTIPLIERS is None:
            self.TYPE_MULTIPLIERS = {
                DragonType.FIRE: {"attack": 1.2, "defense": 0.9, "health": 0.8},
                DragonType.WATER: {"attack": 0.9, "defense": 1.1, "health": 1.2},
                DragonType.EARTH: {"attack": 0.8, "defense": 1.3, "health": 1.1},
                DragonType.AIR: {"attack": 1.1, "defense": 0.8, "health": 0.9},
                DragonType.ICE: {"attack": 1.0, "defense": 1.0, "health": 1.0},
                DragonType.STORM: {"attack": 1.3, "defense": 0.7, "health": 0.8},
            }

@dataclass
class CombatConfig:
    """Конфигурация боевой системы"""
    MAX_ROUNDS: int = int(os.getenv("COMBAT_MAX_ROUNDS", "5"))
    TYPE_ADVANTAGE_MULTIPLIER: float = float(os.getenv("TYPE_ADVANTAGE_MULTIPLIER", "1.5"))
    TYPE_DISADVANTAGE_MULTIPLIER: float = float(os.getenv("TYPE_DISADVANTAGE_MULTIPLIER", "0.7"))
    
    # Преимущества типов
    TYPE_ADVANTAGES: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.TYPE_ADVANTAGES is None:
            self.TYPE_ADVANTAGES = {
                DragonType.FIRE: [DragonType.AIR, DragonType.ICE],
                DragonType.WATER: [DragonType.FIRE, DragonType.EARTH],
                DragonType.EARTH: [DragonType.WATER, DragonType.STORM],
                DragonType.AIR: [DragonType.EARTH, DragonType.STORM],
                DragonType.ICE: [DragonType.AIR, DragonType.WATER],
                DragonType.STORM: [DragonType.FIRE, DragonType.ICE],
            }

@dataclass
class ShopConfig:
    """Конфигурация магазина"""
    # Цены на драконов
    DRAGON_PRICES: Dict[str, int] = None
    
    # Бусты
    BOOSTS: Dict[str, Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.DRAGON_PRICES is None:
            self.DRAGON_PRICES = {
                DragonType.FIRE: 500,
                DragonType.WATER: 600,
                DragonType.EARTH: 550,
                DragonType.AIR: 520,
                DragonType.ICE: 700,
                DragonType.STORM: 800,
            }
        
        if self.BOOSTS is None:
            self.BOOSTS = {
                "damage_boost": {
                    "name": "Усиление атаки",
                    "price": 200,
                    "duration": 3600,  # 1 час
                    "multiplier": 1.3
                },
                "critical_boost": {
                    "name": "Усиление крита", 
                    "price": 300,
                    "duration": 1800,  # 30 минут
                    "chance_bonus": 0.15
                },
                "coin_boost": {
                    "name": "Удвоение монет",
                    "price": 500,
                    "duration": 7200,  # 2 часа
                    "multiplier": 2.0
                }
            }

@dataclass
class MonitoringConfig:
    """Конфигурация мониторинга"""
    METRICS_PORT: int = int(os.getenv("METRICS_PORT", "8000"))
    HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "300"))
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

@dataclass
class SecurityConfig:
    """Конфигурация безопасности"""
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))
    MAX_BATTLES_PER_HOUR: int = int(os.getenv("MAX_BATTLES_PER_HOUR", "20"))
    ANTI_CHEAT_ENABLED: bool = os.getenv("ANTI_CHEAT_ENABLED", "True").lower() == "true"
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))

class Config:
    """Главный класс конфигурации"""
    
    def __init__(self):
        self.ENVIRONMENT: Environment = Environment(os.getenv("ENVIRONMENT", "development"))
        
        # Подконфиги
        self.DATABASE = DatabaseConfig()
        self.REDIS = RedisConfig()
        self.TELEGRAM = TelegramConfig()
        self.ECONOMY = GameEconomyConfig()
        self.DRAGONS = DragonConfig()
        self.COMBAT = CombatConfig()
        self.SHOP = ShopConfig()
        self.MONITORING = MonitoringConfig()
        self.SECURITY = SecurityConfig()
        
        # Валидация
        self._validate()

    def _validate(self):
        """Проверка обязательных параметров"""
        errors = []
        
        if not self.TELEGRAM.BOT_TOKEN:
            errors.append("BOT_TOKEN не установлен")
        
        if not self.TELEGRAM.BOT_USERNAME:
            errors.append("BOT_USERNAME не установлен")
        
        if self.ENVIRONMENT == Environment.PRODUCTION and not self.TELEGRAM.WEBHOOK_URL:
            errors.append("WEBHOOK_URL обязателен для production")
        
        if errors:
            raise ValueError(f"Ошибки конфигурации: {', '.join(errors)}")

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == Environment.PRODUCTION

    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == Environment.TESTING

def setup_logging(config: Config):
    """Настройка логирования"""
    logging_level = getattr(logging, config.MONITORING.LOG_LEVEL.upper())
    
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("game.log") if config.is_production else logging.NullHandler()
        ]
    )
    
    # Уменьшаем логирование для сторонних библиотек
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)

def load_config() -> Config:
    """Загрузка конфигурации"""
    return Config()

# Глобальный экземпляр конфигурации
config = load_config()

# Настройка логирования при импорте
setup_logging(config)