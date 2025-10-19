import pytest
import sqlite3
from game.database import Database
from datetime import datetime, timedelta

class TestDatabase:
    """Тесты работы с базой данных"""
    
    @pytest.fixture
    def test_db(self):
        """Фикстура тестовой БД в памяти"""
        db = Database(':memory:')
        yield db
        db.close()
    
    def test_player_creation(self, test_db):
        """Тест создания записи о игроке"""
        player_id = 123
        test_db.create_player(player_id)
        
        player = test_db.get_player(player_id)
        assert player is not None
        assert player['coins'] == 0
        assert player['crystals'] == 0
    
    def test_coin_operations(self, test_db):
        """Тест операций с монетами"""
        player_id = 123
        test_db.create_player(player_id)
        
        # Добавляем монеты
        test_db.update_coins(player_id, 100)
        assert test_db.get_player(player_id)['coins'] == 100
        
        # Убираем монеты
        test_db.update_coins(player_id, -50)
        assert test_db.get_player(player_id)['coins'] == 50
    
    def test_dragon_unlocking(self, test_db):
        """Тест разблокировки драконов"""
        player_id = 123
        test_db.create_player(player_id)
        
        # Разблокируем дракона
        test_db.unlock_dragon(player_id, 'ice')
        
        # Проверяем
        dragons = test_db.get_unlocked_dragons(player_id)
        assert 'ice' in dragons
        assert len(dragons) == 2  # fire + ice
    
    def test_boost_management(self, test_db):
        """Тест управления бустами"""
        player_id = 123
        test_db.create_player(player_id)
        expires_at = datetime.now() + timedelta(hours=1)
        
        # Добавляем буст
        test_db.add_boost(player_id, '2x_coins', expires_at)
        
        # Проверяем
        boosts = test_db.get_active_boosts(player_id)
        assert len(boosts) == 1
        assert boosts[0]['type'] == '2x_coins'
        
        # Удаляем буст
        test_db.remove_boost(player_id, '2x_coins')
        assert len(test_db.get_active_boosts(player_id)) == 0
    
    def test_battle_recording(self, test_db):
        """Тест записи PvP боев"""
        player1 = 111
        player2 = 222
        test_db.create_player(player1)
        test_db.create_player(player2)
        
        # Создаем запись о бое
        battle_id = test_db.record_battle(
            player1=player1,
            player2=player2,
            winner=player1,
            duration=120
        )
        
        # Проверяем
        battle = test_db.get_battle(battle_id)
        assert battle['winner'] == player1
        assert battle['duration'] == 120
        
        # Проверяем историю
        history = test_db.get_battle_history(player1)
        assert len(history) == 1
        assert history[0]['battle_id'] == battle_id
    
    def test_concurrent_access(self, test_db):
        """Тест на конкурентный доступ к БД"""
        import threading
        
        player_id = 123
        test_db.create_player(player_id)
        
        def update_coins_thread():
            for _ in range(100):
                test_db.update_coins(player_id, 1)
        
        threads = []
        for _ in range(5):
            t = threading.Thread(target=update_coins_thread)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Проверяем итоговое количество
        assert test_db.get_player(player_id)['coins'] == 500