import pytest
from unittest.mock import AsyncMock
from game.game_flow import GameFlow
from game.economy import EconomySystem
from game.dragons import DragonSystem
from game.boosts import BoostSystem

class TestGameFlow:
    """Интеграционные тесты основного игрового потока"""
    
    @pytest.fixture
    def game_systems(self):
        return {
            'economy': EconomySystem(),
            'dragons': DragonSystem(),
            'boosts': BoostSystem(),
            'game': GameFlow()
        }
    
    @pytest.fixture
    async def initialized_game(self, game_systems):
        user_id = 123
        await game_systems['game'].initialize_player(user_id)
        return user_id, game_systems
    
    async def test_initialization(self, game_systems):
        """Тест инициализации нового игрока"""
        user_id = 123
        result = await game_systems['game'].initialize_player(user_id)
        
        assert result is True
        assert game_systems['economy'].get_balance(user_id) == (0, 0)
        assert game_systems['dragons'].get_user_dragon(user_id).type == 'fire'
    
    async def test_tap_mechanic(self, initialized_game):
        """Тест механики кликов"""
        user_id, systems = initialized_game
        initial_coins, _ = systems['economy'].get_balance(user_id)
        
        # Симулируем 5 кликов
        for _ in range(5):
            await systems['game'].process_tap(user_id)
        
        new_coins, _ = systems['economy'].get_balance(user_id)
        assert new_coins == initial_coins + 5
    
    async def test_dragon_evolution(self, initialized_game):
        """Тест эволюции дракона"""
        user_id, systems = initialized_game
        
        # Добавляем монет для эволюции
        for _ in range(500):
            await systems['game'].process_tap(user_id)
        
        # Эволюционируем в ice дракона
        result = await systems['game'].evolve_dragon(user_id, 'ice')
        assert result is True
        assert systems['dragons'].get_user_dragon(user_id).type == 'ice'
    
    async def test_boost_application(self, initialized_game):
        """Тест применения бустов"""
        user_id, systems = initialized_game
        
        # Добавляем кристаллы
        systems['economy'].add_crystals(user_id, 10)
        
        # Применяем буст
        result = await systems['game'].apply_boost(user_id, '2x_coins')
        assert result is True
        
        # Проверяем активные бусты
        active_boosts = systems['boosts'].get_active_boosts(user_id)
        assert '2x_coins' in [b.type for b in active_boosts]
    
    async def test_full_game_session(self, initialized_game):
        """Комплексный тест игровой сессии"""
        user_id, systems = initialized_game
        
        # 1. Кликаем 10 раз
        for _ in range(10):
            await systems['game'].process_tap(user_id)
        
        # 2. Покупаем улучшение
        upgrade_result = await systems['game'].purchase_upgrade(user_id, 'damage')
        assert upgrade_result is True
        
        # 3. Проверяем увеличенный урон
        damage = systems['dragons'].calculate_damage(user_id)
        assert damage > 1.0
        
        # 4. Применяем буст
        systems['economy'].add_crystals(user_id, 5)
        await systems['game'].apply_boost(user_id, 'critical_hit')
        
        # 5. Проверяем комбинированный эффект
        boosted_damage = systems['dragons'].calculate_damage(user_id)
        assert boosted_damage > damage