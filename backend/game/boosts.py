from datetime import datetime, timedelta

BOOSTS = {
    # Монетные бусты
    "coin_10p": {"type": "income", "value": 0.1, "duration": 1800, "price": 50},
    "coin_2x": {"type": "income", "value": 2.0, "duration": 3600, "price": 100},
    
    # Боевые бусты
    "damage_30p": {"type": "damage", "value": 0.3, "uses_left": 10, "price": 80},
    "auto_attack": {"type": "auto", "duration": 20, "price": 120},
    
    # Способности драконов
    "fire_storm": {"type": "ability", "damage": 50, "cooldown": 60},
    "ice_shield": {"type": "ability", "block": 0.5, "duration": 15},
}

class BoostManager:
    def __init__(self, db):
        self.db = db
    
    def apply_boost(self, user_id: int, boost_id: str):
        boost = BOOSTS[boost_id]
        expires_at = datetime.now() + timedelta(seconds=boost.get("duration", 0))
        
        self.db.execute(
            "INSERT INTO boosts (user_id, boost_id, expires_at, uses_left) VALUES (?, ?, ?, ?)",
            (user_id, boost_id, expires_at, boost.get("uses_left", None))
        )
    
    def get_active_boosts(self, user_id: int):
        return self.db.fetch_all(
            "SELECT * FROM boosts WHERE user_id = ? AND (expires_at > ? OR uses_left > 0)",
            (user_id, datetime.now())
        )