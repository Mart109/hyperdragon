import pytest
import asyncio
from game.pvp import PVPSystem
from game.economy import EconomySystem
from game.dragons import DragonSystem
from game.boosts import BoostSystem

class TestPVPSystem:
    """Расширенные тесты PvP системы"""
    
    @pytest.fixture
    def pvp_systems(self):
        return {
            'pvp': PVPSystem(),
            'economy': EconomySystem(),
            'dragons': DragonSystem(),
            'boosts': BoostSystem()
        }
    
    @pytest.fixture
    async def prepared_players(self, pvp_systems):
        player1 = 111
        player2 = 222
        
        # Инициализация игроков
        for player in [player1, player2]:
            pvp_systems['dragons'].unlock_dragon(player, 'fire')
            pvp_systems['dragons'].unlock_dragon(player, 'ice')
            for _ in range(100):
                pvp_systems['economy'].process_tap(player, 1)
        
        return (player1, player2, pvp_systems)
    
    async def test_matchmaking(self, pvp_systems):
        """Тест системы подбора соперников"""
        player1 = 111
        player2 = 222
        
        # Регистрируем игроков в очереди
        await pvp_systems['pvp'].join_queue(player1)
        await pvp_systems['pvp'].join_queue(player2)
        
        # Проверяем создание боя
        await asyncio.sleep(0.1)  # Даем время на обработку
        battle = pvp_systems['pvp'].find_player_battle(player1)
        assert battle is not None
        assert player2 in [battle.player1, battle.player2]
    
    async def test_dragon_advantages(self, prepared_players):
        """Тест преимуществ разных типов драконов"""
        player1, player2, systems = prepared_players
        
        # Настраиваем разных драконов
        systems['dragons'].set_dragon(player1, 'fire')
        systems['dragons'].set_dragon(player2, 'ice')
        
        # Создаем бой
        battle_id = systems['pvp'].create_battle(player1, player2)
        
        # Симулируем несколько раундов
        for _ in range(3):
            systems['pvp'].process_attack(battle_id, player1)
            systems['pvp'].process_attack(battle_id, player2)
        
        # Проверяем, что ice дракон имеет преимущество
        battle = systems['pvp'].get_battle(battle_id)
        assert battle.player1_hp < battle.player2_hp
    
    async def test_boosts_in_pvp(self, prepared_players):
        """Тест влияния бустов на PvP"""
        player1, player2, systems = prepared_players
        
        # Применяем буст к первому игроку
        systems['boosts'].apply_boost(player1, 'pvp_damage_boost', duration=300)
        
        battle_id = systems['pvp'].create_battle(player1, player2)
        
        # Оба игрока атакуют
        systems['pvp'].process_attack(battle_id, player1)
        systems['pvp'].process_attack(battle_id, player2)
        
        # Проверяем, что урон первого игрока выше
        battle = systems['pvp'].get_battle(battle_id)
        damage1 = 100 - battle.player2_hp
        damage2 = 100 - battle.player1_hp
        assert damage1 > damage2
    
    async def test_pvp_rewards(self, prepared_players):
        """Тест системы наград за PvP"""
        player1, player2, systems = prepared_players
        
        # Создаем и завершаем бой
        battle_id = systems['pvp'].create_battle(player1, player2)
        systems['pvp'].force_finish(battle_id, player1)
        
        # Проверяем награды
        coins1, _ = systems['economy'].get_balance(player1)
        coins2, _ = systems['economy'].get_balance(player2)
        
        assert coins1 == 100 + systems['pvp'].WIN_REWARD
        assert coins2 == 100 - systems['pvp'].LOSS_PENALTY
    
    async def test_concurrent_battles(self, pvp_systems):
        """Тест на обработку нескольких одновременных боев"""
        players = [i for i in range(10)]
        
        # Создаем 5 одновременных боев
        battle_ids = []
        for i in range(0, 10, 2):
            battle_id = pvp_systems['pvp'].create_battle(players[i], players[i+1])
            battle_ids.append(battle_id)
        
        # Симулируем атаки во всех боях
        for bid in battle_ids:
            battle = pvp_systems['pvp'].get_battle(bid)
            pvp_systems['pvp'].process_attack(bid, battle.player1)
            pvp_systems['pvp'].process_attack(bid, battle.player2)
        
        # Проверяем состояние всех боев
        for bid in battle_ids:
            battle = pvp_systems['pvp'].get_battle(bid)
            assert battle.player1_hp < 100
            assert battle.player2_hp < 100