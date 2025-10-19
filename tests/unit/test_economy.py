import pytest
from unittest.mock import MagicMock
from game.economy import EconomySystem

class TestEconomySystem:
    """Тесты системы игровой экономики"""
    
    @pytest.fixture
    def economy(self):
        return EconomySystem()
    
    def test_initial_balance(self, economy):
        """Проверка начального баланса игрока"""
        assert economy.get_balance(123) == (0, 0)  # (coins, crystals)
    
    def test_coin_earning(self, economy):
        """Тест начисления монет за клики"""
        user_id = 123
        tap_power = 1
        
        # 10 кликов с базовой силой
        for _ in range(10):
            economy.process_tap(user_id, tap_power)
        
        assert economy.get_balance(user_id) == (10, 0)
    
    def test_boosted_earnings(self, economy):
        """Тест начисления с множителем"""
        user_id = 123
        economy.apply_boost(user_id, '2x_coins', duration=60)
        
        # 5 кликов с множителем
        for _ in range(5):
            economy.process_tap(user_id, 1)
        
        assert economy.get_balance(user_id) == (10, 0)  # 5*2=10
    
    def test_insufficient_funds(self, economy):
        """Тест проверки недостатка средств"""
        user_id = 123
        with pytest.raises(ValueError):
            economy.make_purchase(user_id, 'dragon', 500)
    
    def test_successful_purchase(self, economy):
        """Тест успешной покупки"""
        user_id = 123
        economy.process_tap(user_id, 1)  # +1 coin
        economy.process_tap(user_id, 499)  # +499 coins
        
        # Покупка улучшения за 100 монет
        economy.make_purchase(user_id, 'damage_upgrade', 100)
        assert economy.get_balance(user_id) == (400, 0)