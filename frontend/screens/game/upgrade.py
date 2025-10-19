# frontend/screens/game/upgrade.py
from ..base import InteractiveScreen, ScreenResult
from typing import Optional, Tuple

class UpgradeScreen(InteractiveScreen):
    UPGRADES = {
        'damage': {
            'name': 'Урон',
            'cost_func': lambda level: 100 * (level + 1),
            'effect_func': lambda level: 5 + level * 2
        },
        'auto_click': {
            'name': 'Автоклик',
            'cost_func': lambda level: 200 * (level + 1),
            'effect_func': lambda level: 1 + level * 0.5
        }
    }

    def __init__(self, assets, localization, user_data):
        super().__init__(assets, localization, user_data)
        self.user_upgrades = user_data.setdefault('upgrades', {
            'damage': {'level': 0, 'value': 5},
            'auto_click': {'level': 0, 'value': 0}
        })

    def render(self) -> ScreenResult:
        upgrades_text = []
        for upgrade_id, config in self.UPGRADES.items():
            current = self.user_upgrades[upgrade_id]
            next_level = current['level'] + 1
            cost = config['cost_func'](current['level'])
            effect = config['effect_func'](next_level)
            
            upgrades_text.append(
                f"{config['name']} (Ур. {current['level']}) → "
                f"Ур. {next_level}: +{effect - current['value']:.1f}\n"
                f"Стоимость: {cost} монет"
            )

        return ScreenResult(
            text=self.localization.get(
                'upgrade.title',
                coins=self.user_data['coins']
            ) + "\n\n" + "\n\n".join(upgrades_text),
            buttons=[
                [{
                    "text": f"🔼 Улучшить {upgrade}",
                    "data": f"upgrade_{upgrade}"
                }] for upgrade in self.UPGRADES.keys()
            ] + [
                [{"text": "◀️ Назад", "data": "back"}]
            ]
        )

    def handle_action(self, action: str) -> Tuple[Optional[str], Optional[BaseScreen]]:
        if action.startswith("upgrade_"):
            upgrade_id = action[8:]
            config = self.UPGRADES[upgrade_id]
            current = self.user_upgrades[upgrade_id]
            cost = config['cost_func'](current['level'])
            
            if self.user_data['coins'] >= cost:
                self.user_data['coins'] -= cost
                current['level'] += 1
                current['value'] = config['effect_func'](current['level'])
                
                return (
                    self.localization.get(
                        'upgrade.success',
                        upgrade=config['name'],
                        level=current['level']
                    ),
                    None
                )
            return (
                self.localization.get('error.not_enough_coins'),
                None
            )
        return None, MainGameScreen(self.assets, self.localization, self.user_data)