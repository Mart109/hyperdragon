import pytest
from game.shop import ShopSystem
from game.economy import EconomySystem
from game.dragons import DragonSystem
from game.boosts import BoostSystem

class TestShopSystem:
    """Комплексные тесты магазина"""
    
    @pytest.fixture
    def shop_systems(self):
        return {
            'shop': ShopSystem(),
            'economy': EconomySystem(),
            'dragons': DragonSystem(),
            'boosts': BoostSystem()
        }
    
    @pytest.fixture
    def rich_player(self, shop_systems):
        player_id = 123
        # Даем игроку много валюты
        shop_systems['economy'].add_coins(player_id, 10000)
        shop_systems['economy'].add_crystals(player_id, 1000)
        return player_id
    
    def test_item_purchases(self, shop_systems, rich_player):
        """Тест покупки различных предметов"""
        player_id = rich_player
        
        # Покупка улучшения урона
        result, _ = shop_systems['shop'].purchase_item(player_id, 'damage_upgrade')
        assert result is True
        
        # Покупка нового дракона
        result, _ = shop_systems['shop'].purchase_item(player_id, 'ice_dragon')
        assert result is True
        assert 'ice' in shop_systems['dragons'].get_unlocked_dragons(player_id)
        
        # Покупка буста
        result, _ = shop_systems['shop'].purchase_item(player_id, '2x_coins_boost')
        assert result is True
        assert len(shop_systems['boosts'].get_inventory(player_id)) == 1
    
    def test_insufficient_funds(self, shop_systems):
        """Тест обработки недостатка средств"""
        player_id = 456  # новый игрок без денег
        
        # Попытка купить без денег
        result, msg = shop_systems['shop'].purchase_item(player_id, 'damage_upgrade')
        assert result is False
        assert "Not enough coins" in msg
    
    def test_inventory_management(self, shop_systems, rich_player):
        """Тест управления инвентарем"""
        player_id = rich_player
        
        # Покупаем несколько бустов
        shop_systems['shop'].purchase_item(player_id, '2x_coins_boost')
        shop_systems['shop'].purchase_item(player_id, 'critical_hit_boost')
        
        # Проверяем инвентарь
        inventory = shop_systems['shop'].get_player_inventory(player_id)
        assert len(inventory['boosts']) == 2
        assert inventory['dragons'] == ['fire']  # начальный дракон
    
    def test_limited_offers(self, shop_systems, rich_player):
        """Тест ограниченных предложений"""
        player_id = rich_player
        
        # Добавляем ограниченное предложение
        shop_systems['shop'].add_special_offer(
            'limited_dragon', 
            cost=500, 
            is_crystal=True, 
            limit=1
        )
        
        # Покупаем предложение
        result, _ = shop_systems['shop'].purchase_item(player_id, 'limited_dragon')
        assert result is True
        
        # Пытаемся купить еще раз
        result, msg = shop_systems['shop'].purchase_item(player_id, 'limited_dragon')
        assert result is False
        assert "out of stock" in msg.lower()
    
    def test_shop_rotation(self, shop_systems):
        """Тест ротации товаров в магазине"""
        initial_items = len(shop_systems['shop'].get_available_items())
        
        # Добавляем временный товар
        shop_systems['shop'].add_timed_item(
            'weekend_special', 
            cost=300, 
            duration=60*60*48  # 48 часов
        )
        
        # Проверяем добавление
        assert len(shop_systems['shop'].get_available_items()) == initial_items + 1
        
        # Симулируем истечение времени
        shop_systems['shop']._timed_items['weekend_special']['expires_at'] = 0
        shop_systems['shop'].cleanup_expired_items()
        
        # Проверяем удаление
        assert len(shop_systems['shop'].get_available_items()) == initial_items