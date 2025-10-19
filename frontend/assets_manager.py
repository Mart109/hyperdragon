from pathlib import Path
from enum import Enum
import logging

class AssetType(Enum):
    DRAGON = "dragons"
    UI = "ui"
    SOUND = "sounds"

class AssetsManager:
    def __init__(self, base_path: str = "frontend/assets"):
        self.base_path = Path(base_path)
        
    def get_asset(self, asset_type: AssetType, name: str) -> Path:
        """Получение пути к ассету"""
        path = self.base_path / asset_type.value / name
        if not path.exists():
            logging.error(f"Asset not found: {path}")
            raise FileNotFoundError(f"Missing asset: {path}")
        return path

    # Пример специализированных методов
    def get_dragon(self, dragon_type: str) -> Path:
        return self.get_asset(AssetType.DRAGON, f"{dragon_type}.png")
    
    def get_button(self, button_name: str) -> Path:
        return self.get_asset(AssetType.UI, f"buttons/{button_name}.png")