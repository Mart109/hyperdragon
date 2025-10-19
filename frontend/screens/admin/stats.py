# frontend/screens/admin/stats.py
from ..base import BaseScreen, ScreenResult

class AdminStatsScreen(BaseScreen):
    def __init__(self, assets, localization, user_data, db_connection):
        super().__init__(assets, localization, user_data)
        self.db = db_connection
    
    def render(self) -> ScreenResult:
        stats = self.db.get_game_stats()
        return ScreenResult(
            text=self.localization.get(
                'admin.stats',
                users=stats['total_users'],
                active=stats['active_today'],
                battles=stats['battles']
            ),
            buttons=[
                [{"text": "📊 Обновить", "data": "refresh"}],
                [{"text": "◀️ Назад", "data": "back"}]
            ]
        )