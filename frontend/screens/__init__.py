# frontend/screens/__init__.py
from importlib import import_module
from pathlib import Path
from typing import Type, Dict, TypeVar
from ..base import BaseScreen, InteractiveScreen
import logging

# Тип для экранов
ScreenType = TypeVar('ScreenType', bound=BaseScreen)

class ScreenManager:
    """Менеджер для динамической загрузки и управления экранами"""
    _screens: Dict[str, Type[BaseScreen]] = {}
    
    def __init__(self, assets, localization, db_connection=None):
        self.assets = assets
        self.localization = localization
        self.db = db_connection
        self._load_all_screens()
    
    def _load_all_screens(self) -> None:
        """Автоматическая загрузка всех экранов из подпапок"""
        screens_dir = Path(__file__).parent
        for item in screens_dir.glob('**/*.py'):
            if item.name.startswith('_') or item.name == 'base.py':
                continue
            
            # Преобразование пути в модуль (например: screens/game/main.py -> screens.game.main)
            module_path = '.'.join(
                ['frontend'] + 
                list(item.relative_to(screens_dir.parent).with_suffix('').parts)
            )
            
            try:
                module = import_module(module_path)
                for name, obj in module.__dict__.items():
                    if (
                        isinstance(obj, type) and 
                        issubclass(obj, BaseScreen) and 
                        obj not in (BaseScreen, InteractiveScreen)
                    ):
                        self.register_screen(name, obj)
            except ImportError as e:
                logging.warning(f"Failed to load screen from {item}: {e}")
    
    def register_screen(self, name: str, screen_class: Type[ScreenType]) -> None:
        """Ручная регистрация экрана"""
        if not issubclass(screen_class, BaseScreen):
            raise ValueError(f"{screen_class} must be a subclass of BaseScreen")
        self._screens[name] = screen_class
    
    def create_screen(
        self,
        screen_name: str,
        user_data: dict,
        **kwargs
    ) -> BaseScreen:
        """Создание экрана с инъекцией зависимостей"""
        if screen_name not in self._screens:
            raise ValueError(f"Unknown screen: {screen_name}")
        
        return self._screens[screen_name](
            assets=self.assets,
            localization=self.localization,
            user_data=user_data,
            db_connection=self.db,
            **kwargs
        )

# Автоматическая регистрация часто используемых экранов для удобного импорта
from .game.main import MainGameScreen
from .game.battle import BattleScreen
from .shop.main import ShopScreen
from .pvp.lobby import PvPLobbyScreen

__all__ = [
    'ScreenManager',
    'MainGameScreen',
    'BattleScreen',
    'ShopScreen',
    'PvPLobbyScreen',
    'BaseScreen',
    'InteractiveScreen'
]