# frontend/screens/shop/main.py
from ..base import InteractiveScreen, ScreenResult

class ShopScreen(InteractiveScreen):
    ITEMS = [
        {"id": "damage_boost", "name": "Улучшение урона", "price": 100},
        {"id": "auto_clicker", "name": "Автокликер", "price": 500}
    ]
    
    def render(self) -> ScreenResult:
        items_text = "\n".join(
            f"{item['name']} - {item['price']} монет"
            for item in self.ITEMS
        )
        
        return ScreenResult(
            text=self.localization.get('shop.title') + "\n\n" + items_text,
            buttons=[
                [{"text": item["name"], "data": f"buy_{item['id']}"}]
                for item in self.ITEMS
            ] + [
                [{"text": self.localization.get('btn_back'), "data": "back"}]
            ]
        )
    
    def handle_action(self, action: str) -> Tuple[Optional[str], Optional[BaseScreen]]:
        if action.startswith("buy_"):
            item_id = action[4:]
            return None, ConfirmPurchaseScreen(
                self.assets, 
                self.localization,
                self.user_data,
                item_id
            )
        return None, MainGameScreen(...)