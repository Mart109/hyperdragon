# frontend/screens/admin/broadcast.py
from ..base import InteractiveScreen, ScreenResult
from typing import Optional, Tuple, List

class BroadcastScreen(InteractiveScreen):
    MODES = {
        'all': 'Всем игрокам',
        'active': 'Активным (7 дней)',
        'inactive': 'Неактивным (30+ дней)'
    }

    def __init__(self, assets, localization, user_data, db_connection):
        super().__init__(assets, localization, user_data)
        self.db = db_connection
        self.message = ""
        self.selected_mode = "all"
        self.confirmation = False

    def render(self) -> ScreenResult:
        if self.confirmation:
            return ScreenResult(
                text=self.localization.get(
                    'broadcast.confirm',
                    mode=self.MODES[self.selected_mode],
                    count=self._get_recipient_count(),
                    message=self.message
                ),
                buttons=[
                    [{"text": "✅ Отправить", "data": "confirm"}],
                    [{"text": "✏️ Изменить", "data": "edit"}]
                ]
            )
        
        return ScreenResult(
            text=self.localization.get(
                'broadcast.create',
                current_mode=self.MODES[self.selected_mode]
            ),
            buttons=[
                [{"text": mode_name, "data": f"mode_{mode_id}"}]
                for mode_id, mode_name in self.MODES.items()
            ] + [
                [{"text": "📝 Ввести текст", "data": "input"}],
                [{"text": "◀️ Назад", "data": "back"}]
            ]
        )

    def _get_recipient_count(self) -> int:
        """Получение количества получателей"""
        if self.selected_mode == 'all':
            return self.db.get_total_users()
        elif self.selected_mode == 'active':
            return self.db.get_active_users(days=7)
        return self.db.get_inactive_users(days=30)

    def handle_action(self, action: str) -> Tuple[Optional[str], Optional[BaseScreen]]:
        if action.startswith("mode_"):
            self.selected_mode = action[5:]
            return None, None
            
        elif action == "input":
            return (
                self.localization.get('broadcast.enter_text'),
                BroadcastInputScreen(
                    self.assets, 
                    self.localization,
                    self.user_data,
                    self
                )
            )
            
        elif action == "edit":
            self.confirmation = False
            return None, None
            
        elif action == "confirm":
            recipients = self._get_recipient_list()
            self.db.create_broadcast_task(
                message=self.message,
                recipient_ids=recipients
            )
            return (
                self.localization.get(
                    'broadcast.sent',
                    count=len(recipients)
                ),
                AdminMainScreen(...)
            )
            
        return None, AdminMainScreen(...)

class BroadcastInputScreen(InteractiveScreen):
    """Экран ввода текста рассылки"""
    def __init__(self, assets, localization, user_data, parent_screen):
        super().__init__(assets, localization, user_data)
        self.parent = parent_screen

    def render(self) -> ScreenResult:
        return ScreenResult(
            text=self.localization.get('broadcast.enter_text'),
            buttons=[[{"text": "◀️ Отмена", "data": "cancel"}]]
        )

    def handle_action(self, action: str) -> Tuple[Optional[str], Optional[BaseScreen]]:
        if action == "cancel":
            return None, self.parent
        
        # В реальном боте здесь обработка ввода текста
        if action.startswith("text:"):
            self.parent.message = action[5:]
            self.parent.confirmation = True
            return None, self.parent
            
        return None, self.parent