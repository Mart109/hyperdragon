# frontend/screens/pvp/lobby.py
from ..base import InteractiveScreen, ScreenResult
import asyncio

class PvPLobbyScreen(InteractiveScreen):
    def __init__(self, assets, localization, user_data, pvp_manager):
        super().__init__(assets, localization, user_data)
        self.pvp_manager = pvp_manager
        self.search_task = None
    
    def render(self) -> ScreenResult:
        return ScreenResult(
            text=self.localization.get('pvp.searching'),
            buttons=[
                [{"text": "🔍 Поиск соперника", "data": "search"}],
                [{"text": "◀️ Назад", "data": "back"}]
            ]
        )
    
    async def search_opponent(self):
        opponent = await self.pvp_manager.find_opponent()
        return PvPBattleScreen(...)
    
    def handle_action(self, action: str) -> Tuple[Optional[str], Optional[BaseScreen]]:
        if action == "search":
            self.search_task = asyncio.create_task(self.search_opponent())
            return (self.localization.get('pvp.waiting'), None)
        return None, MainGameScreen(...)