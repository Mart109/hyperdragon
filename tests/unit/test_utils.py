import pytest
from game.utils import (
    calculate_level,
    format_time,
    generate_loot,
    cooldown_manager,
    validate_username
)

class TestGameUtils:
    """Тесты вспомогательных утилит игры"""
    
    @pytest.mark.parametrize("xp,expected_level", [
        (0, 1),
        (100, 2),
        (500, 5),
        (1000, 10),
        (2500, 15),
        (5000, 20)
    ])
    def test_level_calculation(self, xp, expected_level):
        """Тест расчета уровня игрока"""
        assert calculate_level(xp) == expected_level
    
    @pytest.mark.parametrize("seconds,expected_string", [
        (30, "30 сек"),
        (60, "1 мин"),
        (90, "1 мин 30 сек"),
        (3600, "1 ч"),
        (3660, "1 ч 1 мин"),
        (86400, "1 д")
    ])
    def test_time_formatting(self, seconds, expected_string):
        """Тест форматирования времени"""
        assert format_time(seconds) == expected_string
    
    def test_loot_generation(self):
        """Тест генерации лута"""
        # Тестируем несколько вариантов
        for _ in range(10):
            loot = generate_loot(level=5)
            assert 'coins' in loot
            assert 10 <= loot['coins'] <= 50
            assert 'items' in loot
        
        # Тест с повышеным уровнем
        loot = generate_loot(level=20)
        assert 50 <= loot['coins'] <= 250
    
    def test_cooldown_manager(self):
        """Тест менеджера кулдаунов"""
        user_id = 123
        
        # Проверяем первый вызов
        assert cooldown_manager.check_cooldown(user_id, 'action1') is True
        
        # Устанавливаем кулдаун
        cooldown_manager.set_cooldown(user_id, 'action1', 60)
        
        # Проверяем кулдаун
        assert cooldown_manager.check_cooldown(user_id, 'action1') is False
        
        # Симулируем истечение времени
        cooldown_manager._cooldowns[user_id]['action1'] = 0
        assert cooldown_manager.check_cooldown(user_id, 'action1') is True
    
    @pytest.mark.parametrize("username,expected", [
        ("Player1", True),
        ("DragonSlayer", True),
        ("Игрок123", True),
        ("", False),
        ("X"*21, False),
        ("Invalid@Name", False),
        (" space ", False)
    ])
    def test_username_validation(self, username, expected):
        """Тест валидации имен игроков"""
        assert validate_username(username) == expected
    
    def test_random_utils(self):
        """Тест дополнительных случайных утилит"""
        from game.utils import random_chance, weighted_choice
        
        # Тест random_chance
        true_count = sum(1 for _ in range(1000) if random_chance(0.3))
        assert 250 <= true_count <= 350  # ~30% из 1000
        
        # Тест weighted_choice
        items = [('common', 70), ('rare', 25), ('epic', 5)]
        choices = [weighted_choice(items) for _ in range(1000)]
        common_count = choices.count('common')
        assert 650 <= common_count <= 750  # ~70%