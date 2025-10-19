from typing import Dict, List
from backend.config import Config
from backend.security.data_validator import validate_currency

class Economy:
    def __init__(self, db):
        self.db = db
    
    def add_coins(self, user_id: int, amount: int) -> int:
        """
        Добавляет монеты с учетом бустов доходов
        Args:
            user_id: ID пользователя
            amount: Количество монет (должно быть > 0)
        Returns:
            Итоговое количество добавленных монет
        """
        validate_currency(amount)  # Проверка что amount > 0
        
        boosts = self.db.get_active_boosts(user_id)
        multiplier = 1.0 + sum(
            boost["value"] for boost in boosts 
            if boost["type"] == "income"
        )
        
        total = int(amount * multiplier)
        self.db.update_user(user_id, {"$inc": {"coins": total}})
        return total
    
    def buy_item(self, user_id: int, item_id: str, price: int) -> bool:
        """
        Безопасная покупка предмета
        Args:
            price: Должен быть > 0
        Returns:
            True если покупка успешна
        """
        if price <= 0:
            return False
            
        user = self.db.get_user(user_id)
        if user["coins"] < price:
            return False
            
        # Атомарное обновление
        success = self.db.update_user(
            user_id,
            updates={
                "$inc": {"coins": -price},
                "$push": {"inventory": item_id}
            },
            conditions={"coins": {"$gte": price}}
        )
        return bool(success)
    
    def transfer_coins(self, sender_id: int, receiver_id: int, amount: int) -> bool:
        """Внешний интерфейс для перевода"""
        return self.db.transfer_coins(
            sender_id=sender_id,
            receiver_id=receiver_id,
            amount=amount,
            fee=Config.TRANSACTION_FEE  # Берем комиссию из конфига
        )
            
        # Используем атомарные операции
        return bool(
            self.db.transfer_coins(
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=amount,
                fee=Config.TRANSACTION_FEE
            )
        )