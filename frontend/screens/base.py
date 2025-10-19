# frontend/screens/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass

@dataclass
class ScreenResult:
    text: str
    image_path: Optional[Path] = None
    buttons: Optional[List[List[Dict[str, str]]]] = None
    gif_animation: Optional[Path] = None

class BaseScreen(ABC):
    """Абстрактный базовый класс для всех экранов"""
    def __init__(self, assets, localization, user_data):
        self.assets = assets
        self.localization = localization
        self.user_data = user_data
    
    @abstractmethod
    def render(self) -> ScreenResult:
        """Основной метод рендеринга экрана"""
        pass

class InteractiveScreen(BaseScreen, ABC):
    """Экран с обработкой действий пользователя"""
    @abstractmethod
    def handle_action(self, action: str) -> Tuple[Optional[str], Optional[BaseScreen]]:
        """
        Обработка действия пользователя
        Возвращает: (response_message, new_screen)
        """
        pass