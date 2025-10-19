# frontend/screens/game/battle.py
from ..base import InteractiveScreen, ScreenResult
from ...enums import DragonType
import random
from typing import Optional, Tuple

class BattleScreen(InteractiveScreen):
    DRAGON_STRENGTHS = {
        DragonType.FIRE: {'strong': DragonType.ICE, 'weak': DragonType.EARTH},
        DragonType.ICE: {'strong': DragonType.STORM, 'weak': DragonType.FIRE},
        DragonType.STORM: {'strong': DragonType.EARTH, 'weak': DragonType.ICE},
        DragonType.EARTH: {'strong': DragonType.FIRE, 'weak': DragonType.STORM}
    }

    def __init__(self, assets, localization, user_data, enemy_type: DragonType, is_pvp: bool = False):
        super().__init__(assets, localization, user_data)
        self.player_dragon = DragonType(user_data['dragon'])
        self.enemy_type = enemy_type
        self.is_pvp = is_pvp
        
        # Инициализация характеристик
        self.player_hp = 100 + user_data.get('upgrades', {}).get('health', {}).get('value', 0)
        self.enemy_hp = 100 if not is_pvp else 100  # В PvP берем из данных соперника
        
        self.player_attack = 10 + user_data.get('upgrades', {}).get('damage', {}).get('value', 0)
        self.enemy_attack = 8 if not is_pvp else 10  # В PvP берем из данных соперника
        
        self.special_charges = 3
        self.turn = 0

    def _calculate_damage(self, attacker: str, move_type: str) -> int:
        """Расчет урона с учетом типов драконов"""
        base_damage = self.player_attack if attacker == 'player' else self.enemy_attack
        multiplier = 1.0
        
        if move_type == 'special':
            multiplier *= 1.5
            if attacker == 'player':
                self.special_charges -= 1
        
        # Проверка преимуществ типов
        if attacker == 'player':
            if self.enemy_type == self.DRAGON_STRENGTHS[self.player_dragon]['strong']:
                multiplier *= 1.3
            elif self.enemy_type == self.DRAGON_STRENGTHS[self.player_dragon]['weak']:
                multiplier *= 0.7
        else:
            if self.player_dragon == self.DRAGON_STRENGTHS[self.enemy_type]['strong']:
                multiplier *= 1.3
            elif self.player_dragon == self.DRAGON_STRENGTHS[self.enemy_type]['weak']:
                multiplier *= 0.7
        
        return int(base_damage * multiplier * (0.9 + random.random() * 0.2))

    def render(self) -> ScreenResult:
        return ScreenResult(
            text=self.localization.get(
                'battle.status',
                player_hp=self.player_hp,
                enemy_hp=self.enemy_hp,
                turn=self.turn,
                special_charges=self.special_charges
            ),
            image_path=self.assets.get_battle_image(
                self.player_dragon, 
                self.enemy_type
            ),
            buttons=self._generate_buttons()
        )

    def _generate_buttons(self) -> List[List[Dict]]:
        buttons = [
            [{"text": "⚔️ Атака", "data": "attack"}],
            [{"text": "🛡️ Защита", "data": "defend"}]
        ]
        
        if self.special_charges > 0:
            buttons.append(
                [{"text": f"🌀 Способность ({self.special_charges})", "data": "special"}]
            )
            
        if self.is_pvp:
            buttons.append([{"text": "🏳️ Сдаться", "data": "surrender"}])
            
        return buttons

    def handle_action(self, action: str) -> Tuple[Optional[str], Optional[BaseScreen]]:
        self.turn += 1
        
        # Обработка действий игрока
        if action == "attack":
            damage = self._calculate_damage('player', 'normal')
            self.enemy_hp -= damage
            response = self.localization.get('battle.player_attack', damage=damage)
            
        elif action == "special" and self.special_charges > 0:
            damage = self._calculate_damage('player', 'special')
            self.enemy_hp -= damage
            response = self.localization.get('battle.player_special', damage=damage)
            
        elif action == "defend":
            # Уменьшает следующий полученный урон
            response = self.localization.get('battle.player_defend')
            # Здесь должна быть логика защиты
            return response, None
            
        elif action == "surrender":
            return self.localization.get('battle.surrender'), BattleResultScreen(
                self.assets, self.localization, self.user_data, False, is_pvp=True
            )
        
        # Проверка победы
        if self.enemy_hp <= 0:
            return None, BattleResultScreen(
                self.assets, self.localization, self.user_data, True, self.is_pvp
            )
        
        # Ход противника (для PvE)
        if not self.is_pvp:
            enemy_action = random.choice(['attack', 'attack', 'defend'])
            if enemy_action == "attack":
                damage = self._calculate_damage('enemy', 'normal')
                self.player_hp -= damage
                response += "\n\n" + self.localization.get(
                    'battle.enemy_attack', 
                    damage=damage
                )
        
        # Проверка поражения
        if self.player_hp <= 0:
            return None, BattleResultScreen(
                self.assets, self.localization, self.user_data, False, self.is_pvp
            )
        
        return response, None