# frontend/screens/shop/confirm.py
from ..base import InteractiveScreen, ScreenResult

class ConfirmPurchaseScreen(InteractiveScreen):
    def __init__(self, assets, localization, user_data, item_id):
        super().__init__(assets, localization, user_data)
        self.item_id = item_id
        self.item = next(i for i in ShopScreen.ITEMS if i["id"] == item_id)
    
    def render(self) -> ScreenResult:
        return ScreenResult(
            text=self.localization.get(
                'shop.confirm',
                item=self.item["name"],
                price=self.item["price"],
                balance=self.user_data['coins']
            ),
            buttons=[
                [
                    {"text": "✅ Подтвердить", "data": "confirm"},
                    {"text": "❌ Отмена", "data": "cancel"}
                ]
            ]
        )
    
    def handle_action(self, action: str) -> Tuple[Optional[str], Optional[BaseScreen]]:
        if action == "confirm":
            if self.user_data['coins'] >= self.item["price"]:
                self.user_data['coins'] -= self.item["price"]
                return (
                    self.localization.get('shop.purchased'),
                    MainGameScreen(...)
                )
            return (
                self.localization.get('error.not_enough_coins'),
                None
            )
        return None, ShopScreen(...)