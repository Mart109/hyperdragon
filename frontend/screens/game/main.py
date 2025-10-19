# frontend/screens/game/main.py
from ..base import BaseScreen, ScreenResult
from ...enums import DragonType, Language
from pathlib import Path

class MainGameScreen(BaseScreen):
    def render(self) -> ScreenResult:
        lang = Language(self.user_data.get('language', 'ru'))
        dragon = DragonType(self.user_data.get('dragon', 'fire'))
        
        return ScreenResult(
            text=self.localization.get(
                'main_screen',
                coins=self.user_data['coins'],
                damage=self.user_data['damage'],
                language=lang
            ),
            image_path=self.assets.get_dragon_image(dragon, lang),
            buttons=[
                [
                    {"text": self.localization.get('btn_tap'), "data": "tap"},
                    {"text": self.localization.get('btn_shop'), "data": "open_shop"}
                ],
                [
                    {"text": self.localization.get('btn_pvp'), "data": "pvp_lobby"},
                    {"text": self.localization.get('btn_stats'), "data": "stats"}
                ]
            ]
        )