# frontend/enums.py
from enum import Enum

class Language(str, Enum):
    """Поддерживаемые языки игры"""
    RU = "ru"
    EN = "en"
    ES = "es"  # Пример добавления нового языка

class DragonType(str, Enum):
    """Типы драконов в игре"""
    FIRE = "fire"
    ICE = "ice"
    STORM = "storm"
    EARTH = "earth"
    POISON = "poison"  # Пример расширения

class ScreenType(str, Enum):
    """Типы экранов игры"""
    MAIN = "main"
    SHOP = "shop"
    BATTLE = "battle"
    INVENTORY = "inventory"