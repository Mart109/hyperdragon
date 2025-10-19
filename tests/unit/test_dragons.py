import pytest
from game.dragons import DragonSystem

class TestDragonSystem:
    """Тесты системы драконов"""
    
    @pytest.fixture
    def dragon_system(self):
        return DragonSystem()
    
    def test_initial_dragon(self, dragon_system):
        """Проверка начального дракона"""
        user_id = 123
        dragon = dragon_system.get_user_dragon(user_id)
        assert dragon.type == 'fire'
        assert dragon.damage == 1
    
    def test_dragon_unlock(self, dragon_system):
        """Тест разблокировки нового дракона"""
        user_id = 123
        # Разблокируем ice дракона
        dragon_system.unlock_dragon(user_id, 'ice')
        
        dragon = dragon_system.get_user_dragon(user_id)
        assert dragon.type == 'ice'
        assert dragon.damage == 1.2  # ice имеет +20% урона
    
    def test_dragon_abilities(self, dragon_system):
        """Тест способностей драконов"""
        user_id = 123
        # Проверяем способности fire дракона
        dragon_system.set_dragon(user_id, 'fire')
        assert dragon_system.get_ability(user_id) == 'burn'
        
        # Переключаемся на electric
        dragon_system.unlock_dragon(user_id, 'electric')
        dragon_system.set_dragon(user_id, 'electric')
        assert dragon_system.get_ability(user_id) == 'stun'
    
    def test_dragon_switch(self, dragon_system):
        """Тест переключения между драконами"""
        user_id = 123
        # Разблокируем два дракона
        dragon_system.unlock_dragon(user_id, 'ice')
        dragon_system.unlock_dragon(user_id, 'electric')
        
        # Переключаемся и проверяем
        dragon_system.set_dragon(user_id, 'electric')
        assert dragon_system.get_user_dragon(user_id).type == 'electric'
        
        dragon_system.set_dragon(user_id, 'ice')
        assert dragon_system.get_user_dragon(user_id).type == 'ice'