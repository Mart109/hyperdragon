import pytest
from datetime import datetime, timedelta
from game.boosts import BoostSystem
from unittest.mock import MagicMock

class TestBoostSystem:
    """Тесты системы бустов"""
    
    @pytest.fixture
    def boost_system(self):
        system = BoostSystem()
        system.db = MagicMock()  # Мокаем базу данных
        return system
    
    def test_boost_application(self, boost_system):
        """Тест применения буста"""
        player_id = 123
        boost_type = '2x_coins'
        duration = 300
        
        # Настраиваем мок
        boost_system.db.get_active_boosts.return_value = []
        
        # Применяем буст
        result = boost_system.apply_boost(player_id, boost_type, duration)
        assert result is True
        
        # Проверяем вызовы
        boost_system.db.add_boost.assert_called_once()
    
    def test_boost_stacking(self, boost_system):
        """Тест наложения бустов"""
        player_id = 123
        boost_type = '2x_coins'
        
        # Настраиваем мок (уже есть активный буст)
        boost_system.db.get_active_boosts.return_value = [{'type': boost_type}]
        
        # Пытаемся применить еще один
        result = boost_system.apply_boost(player_id, boost_type, 300)
        assert result is False  # Не должно позволить наложить
        
    def test_multiple_boost_types(self, boost_system):
        """Тест разных типов бустов"""
        player_id = 123
        
        # Настраиваем мок
        boost_system.db.get_active_boosts.return_value = []
        
        # Применяем несколько разных бустов
        result1 = boost_system.apply_boost(player_id, '2x_coins', 300)
        result2 = boost_system.apply_boost(player_id, 'critical_hit', 200)
        
        assert result1 is True
        assert result2 is True
        assert boost_system.db.add_boost.call_count == 2
    
    def test_boost_expiration(self, boost_system):
        """Тест истечения срока буста"""
        player_id = 123
        expired_boost = {
            'type': '2x_coins',
            'expires_at': datetime.now() - timedelta(minutes=1)
        }
        active_boost = {
            'type': 'critical_hit',
            'expires_at': datetime.now() + timedelta(minutes=30)
        }
        
        # Настраиваем мок
        boost_system.db.get_active_boosts.return_value = [expired_boost, active_boost]
        
        # Получаем активные бусты (должен автоматически очистить истекший)
        boosts = boost_system.get_active_boosts(player_id)
        
        assert len(boosts) == 1
        assert boosts[0]['type'] == 'critical_hit'
        boost_system.db.remove_boost.assert_called_once_with(player_id, '2x_coins')
    
    def test_boost_effects(self, boost_system):
        """Тест эффектов различных бустов"""
        player_id = 123
        
        # Тестируем эффект умножения монет
        coins = boost_system.apply_effect('2x_coins', 'coins', 10)
        assert coins == 20
        
        # Тестируем эффект увеличения урона
        damage = boost_system.apply_effect('50p_damage', 'damage', 100)
        assert damage == 150
        
        # Тестируем неизвестный буст
        original = boost_system.apply_effect('unknown', 'value', 100)
        assert original == 100
    
    def test_boost_duration_calculation(self, boost_system):
        """Тест расчета длительности бустов"""
        # Стандартная длительность
        duration = boost_system.calculate_duration('2x_coins')
        assert duration == 300  # 5 минут
        
        # Увеличенная длительность для премиум бустов
        duration = boost_system.calculate_duration('premium_boost')
        assert duration == 1800  # 30 минут
        
        # Неизвестный буст
        duration = boost_system.calculate_duration('unknown')
        assert duration == 0