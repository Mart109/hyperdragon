# frontend/template_loader.py

import json
from pathlib import Path
from typing import Dict, Any
from enum import Enum
import re

class Language(str, Enum):
    RU = "ru"
    EN = "en"

class TemplateManager:
    def __init__(self, base_path: str = "frontend/templates"):
        self.base_path = Path(base_path)
        self._validate_structure()
        self._cache = {}  # Кэш загруженных шаблонов

    def _validate_structure(self) -> None:
        """Проверка базовой структуры папок"""
        required_folders = ["battle", "shop", "dragons", "system"]
        for folder in required_folders:
            if not (self.base_path / folder).exists():
                (self.base_path / folder).mkdir(parents=True)

    def _get_template_path(self, category: str, template_name: str, language: Language) -> Path:
        """Генерация пути к файлу шаблона"""
        return self.base_path / category / f"{template_name}_{language.value}.txt"

    def load_template(self, category: str, template_name: str, language: Language = Language.RU) -> str:
        """Загрузка шаблона из файла с кэшированием"""
        cache_key = f"{category}/{template_name}_{language.value}"
        
        if cache_key not in self._cache:
            template_path = self._get_template_path(category, template_name, language)
            
            try:
                with open(template_path, 'r', encoding='utf-8') as file:
                    self._cache[cache_key] = file.read()
            except FileNotFoundError:
                fallback_path = self._get_template_path(category, template_name, Language.RU)
                try:
                    with open(fallback_path, 'r', encoding='utf-8') as file:
                        self._cache[cache_key] = file.read()
                except FileNotFoundError:
                    self._cache[cache_key] = f"[[Template {category}/{template_name} not found]]"
        
        return self._cache[cache_key]

    def render(self, category: str, template_name: str, context: Dict[str, Any], language: Language = Language.RU) -> str:
        """Рендеринг шаблона с подстановкой переменных"""
        template = self.load_template(category, template_name, language)
        
        # Безопасная подстановка переменных вида {var}
        def replace_match(match):
            var_name = match.group(1)
            return str(context.get(var_name, f"[[{var_name}]]"))
        
        return re.sub(r'\{(\w+)\}', replace_match, template)

    def clear_cache(self) -> None:
        """Очистка кэша шаблонов"""
        self._cache = {}