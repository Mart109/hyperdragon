from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class DragonType(str, Enum):
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"

@dataclass
class Dragon:
    id: str
    owner_id: int
    name: str
    type: DragonType
    level: int = 1
    attack: int = 10
    defense: int = 5
    health: int = 100
    experience: int = 0

@dataclass
class Player:
    """ЕДИНСТВЕННЫЙ класс Player"""
    user_id: int
    username: str
    coins: int = 0
    active_dragon_id: Optional[str] = None  # ID активного дракона
    referrer_id: Optional[int] = None
    referrals_count: int = 0
    is_banned: bool = False
    last_active: Optional[datetime] = None
    они теперь у дракона!

@dataclass
class Boost:
    boost_id: str
    name: str
    effect: str
    duration: int
    price: int

@dataclass
class Transaction:
    id: int
    sender_id: int
    receiver_id: int
    amount: int
    fee: int
    timestamp: datetime