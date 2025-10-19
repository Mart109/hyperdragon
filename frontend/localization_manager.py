# frontend/localization_manager.py

import json
from pathlib import Path
from typing import Dict, Any
from enum import Enum
import logging

class Language(str, Enum):
    RU = "ru"
    EN = "en"
    ES = "es"  # Пример добавления нового языка

class LocalizationManager:
    def __init__(self, base_path: str = "frontend/localization"):
        self.base_path = Path(base_path)
        self._translations: Dict[str, Dict[str, str]] = {}
        self._load_all_translations()
        self._validate_languages()

    def _load_all_translations(self) -> None:
        """Загрузка всех языковых файлов при инициализации"""
        for lang_file in self.base_path.glob("*.json"):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    lang = lang_file.stem
                    self._translations[lang] = json.load(f)
            except Exception as e:
                logging.error(f"Failed to load {lang_file}: {e}")

    def _validate_languages(self) -> None:
        """Проверка наличия обязательных языков"""
        required_langs = {Language.RU, Language.EN}
        available_langs = set(self._translations.keys())
        
        for lang in required_langs:
            if lang.value not in available_langs:
                raise ValueError(f"Required language {lang} is missing")

    def get(self, key: str, language: Language = Language.RU, **kwargs: Any) -> str:
        """
        Получение локализованного текста с подстановкой параметров
        
        Args:
            key: Ключ перевода
            language: Язык перевода
            kwargs: Параметры для подстановки в текст
            
        Returns:
            Локализованный текст или ключ в фигурных скобках, если перевод отсутствует
        """
        translations = self._translations.get(language.value, {})
        fallback = self._translations.get("fallback", {})
        
        template = translations.get(key, fallback.get(key, f"{{{key}}}"))
        
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logging.warning(f"Missing parameter {e} in translation for key '{key}'")
            return template

    def get_available_languages(self) -> list[Language]:
        """Получение списка доступных языков"""
        return [Language(lang) for lang in self._translations.keys() if lang != "fallback"]