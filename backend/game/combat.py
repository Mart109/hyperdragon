import random
from datetime import datetime
from functools import wraps
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class Combat:
    def __init__(self, db):
        self.db = db
        self.cache = {}
        self.rate_limits = {}
        
        # Система преимуществ типов драконов
        self.type_advantages = {
            "fire": ["air", "ice"],
            "water": ["fire", "earth"], 
            "earth": ["water", "storm"],
            "air": ["earth", "storm"],
            "ice": ["air", "water"],
            "storm": ["fire", "ice"]
        }

    def calculate_damage(self, attacker_id: int, defender_id: int = None):
        """Расчет урона с учетом драконов и их типов"""
        try:
            # Получаем драконов участников
            attacker_dragon = self.db.get_active_dragon(attacker_id)
            defender_dragon = self.db.get_active_dragon(defender_id) if defender_id else None
            
            if not attacker_dragon:
                return 1  # Минимальный урон если нет дракона
            
            base_damage = attacker_dragon.get("attack", 10)
            attacker_type = attacker_dragon.get("type", "fire")
            
            # Бонус типа против защитника
            type_multiplier = 1.0
            if defender_dragon:
                defender_type = defender_dragon.get("type", "fire")
                if defender_type in self.type_advantages.get(attacker_type, []):
                    type_multiplier = 1.5  # +50% урона при преимуществе
                    advantage_text = " (преимущество типа!)"
                elif attacker_type in self.type_advantages.get(defender_type, []):
                    type_multiplier = 0.7  # -30% урона при слабости
                    advantage_text = " (слабость типа!)"
                else:
                    advantage_text = ""
            
            # Учет бустов
            try:
                boosts = self.db.get_active_boosts(attacker_id)
                boost_multiplier = 1.0
                for boost in boosts:
                    if boost.get("type") == "damage":
                        boost_multiplier *= (1 + boost.get("value", 0))
            except Exception as e:
                logger.warning(f"Boost calculation error: {e}")
                boost_multiplier = 1.0
            
            # Критический удар
            is_critical = random.random() < 0.1
            critical_multiplier = 2.0 if is_critical else 1.0
            
            final_damage = round(base_damage * type_multiplier * boost_multiplier * critical_multiplier)
            
            logger.info(f"Damage: {final_damage} (player: {attacker_id}, base: {base_damage}, type: {type_multiplier}, critical: {is_critical})")
            return final_damage
            
        except Exception as e:
            logger.error(f"Damage calculation error: {e}")
            return 1

    def pvp_battle(self, player1_id: int, player2_id: int):
        """Улучшенный PvP бой с несколькими раундами"""
        try:
            battle_log = []
            
            # Получаем драконов
            dragon1 = self.db.get_active_dragon(player1_id)
            dragon2 = self.db.get_active_dragon(player2_id)
            
            if not dragon1 or not dragon2:
                return {"error": "У одного из игроков нет дракона"}
            
            # Несколько раундов боя
            p1_health = dragon1.get("health", 100)
            p2_health = dragon2.get("health", 100)
            
            for round_num in range(1, 6):  # Макс 5 раундов
                # Игрок 1 атакует
                p1_damage = self.calculate_damage(player1_id, player2_id)
                p2_health -= p1_damage
                
                # Игрок 2 атакует  
                p2_damage = self.calculate_damage(player2_id, player1_id)
                p1_health -= p2_damage
                
                battle_log.append({
                    "round": round_num,
                    "player1_damage": p1_damage,
                    "player2_damage": p2_damage, 
                    "player1_health": max(0, p1_health),
                    "player2_health": max(0, p2_health)
                })
                
                # Проверяем окончание боя
                if p1_health <= 0 or p2_health <= 0:
                    break
            
            # Определяем победителя
            if p1_health > p2_health:
                winner = player1_id
            elif p2_health > p1_health:
                winner = player2_id
            else:
                winner = None  # Ничья
            
            result = {
                "winner": winner,
                "battle_log": battle_log,
                "player1_dragon": dragon1,
                "player2_dragon": dragon2,
                "final_health": {
                    "player1": max(0, p1_health),
                    "player2": max(0, p2_health)
                }
            }
            
            logger.info(f"PvP battle completed: {player1_id} vs {player2_id}, winner: {winner}")
            return result
            
        except Exception as e:
            logger.error(f"PvP battle error: {e}")
            return {"error": str(e)}

    # Остальные методы остаются без изменений
    def cache_battle(func):
        @wraps(func)
        def wrapper(self, player1_id, player2_id):
            cache_key = f"battle_{player1_id}_{player2_id}"
            if cache_key in self.cache:
                return self.cache[cache_key]
            result = func(self, player1_id, player2_id)
            self.cache[cache_key] = result
            return result
        return wrapper

    def check_rate_limit(func):
        @wraps(func)
        def wrapper(self, player_id, *args, **kwargs):
            LIMIT = 5
            PERIOD = 60
            now = datetime.now()
            if player_id not in self.rate_limits:
                self.rate_limits[player_id] = []
            self.rate_limits[player_id] = [
                t for t in self.rate_limits[player_id] 
                if (now - t).total_seconds() < PERIOD
            ]
            if len(self.rate_limits[player_id]) >= LIMIT:
                raise Exception("Rate limit exceeded")
            self.rate_limits[player_id].append(now)
            return func(self, player_id, *args, **kwargs)
        return wrapper

    def clear_cache_for_player(self, player_id: int):
        keys_to_delete = [
            key for key in self.cache 
            if f"_{player_id}_" in key or key.endswith(f"_{player_id}")
        ]
        for key in keys_to_delete:
            del self.cache[key]