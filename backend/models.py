from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum
import uuid
from datetime import datetime

# Enums для типов данных
class CardType(str, Enum):
    DRAGON = "dragon"
    SPELL = "spell"
    ITEM = "item"
    SUPPORT = "support"

class CardRarity(str, Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class BattleStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

class UpgradeType(str, Enum):
    HEALTH = "health"
    ATTACK = "attack"
    DEFENSE = "defense"
    SPEED = "speed"

# Основные модели данных
class UserProfile(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    level: int = 1
    experience: int = 0
    coins: int = 100
    gems: int = 0
    created_at: datetime
    last_login: datetime

class Card(BaseModel):
    id: str
    name: str
    type: CardType
    rarity: CardRarity
    attack: int
    defense: int
    health: int
    speed: int
    price: int
    description: Optional[str] = None
    image_url: Optional[str] = None
    abilities: List[str] = []

class UserCard(BaseModel):
    card: Card
    quantity: int = 1
    is_equipped: bool = False
    acquired_at: datetime

class Dragon(BaseModel):
    id: str
    name: str
    level: int = 1
    experience: int = 0
    health: int = 100
    max_health: int = 100
    attack_power: int = 10
    defense: int = 5
    speed: int = 8
    element: str  # fire, water, earth, etc.
    equipped_cards: List[str] = []  # IDs of equipped cards
    upgrades: Dict[UpgradeType, int] = {}  # Upgrade levels

class Battle(BaseModel):
    id: str
    player_dragon_id: str
    opponent_dragon_id: str
    status: BattleStatus
    player_health: int
    opponent_health: int
    turns: List[Dict] = []  # History of turns
    created_at: datetime
    completed_at: Optional[datetime] = None
    winner: Optional[str] = None  # player or opponent

class BattleAction(BaseModel):
    battle_id: str
    action_type: str  # attack, defend, use_card
    card_id: Optional[str] = None
    target: str  # opponent or player

class UpgradeRequest(BaseModel):
    dragon_id: str
    upgrade_type: UpgradeType
    cost: int

class PurchaseRequest(BaseModel):
    card_id: str
    quantity: int = 1

class ClickResponse(BaseModel):
    clicks_count: int
    coins_earned: int
    experience_earned: int

# Response models для стандартизации ответов
class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None

class CardsResponse(BaseModel):
    cards: List[Card]
    total: int
    page: int
    page_size: int

class DragonResponse(BaseModel):
    dragon: Dragon
    equipped_cards: List[Card]