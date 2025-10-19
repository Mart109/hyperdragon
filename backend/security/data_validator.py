import re
from typing import Any, Dict, Optional, Type, TypeVar
from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
import html
from enum import Enum

T = TypeVar('T')

class SanitizationError(Exception):
    pass

class InputValidationError(Exception):
    pass

class ValidatorTypes(Enum):
    USERNAME = "username"
    EMAIL = "email"
    PHONE = "phone"
    INTEGER = "integer"
    FLOAT = "float"
    JSON = "json"

class BaseValidator:
    @staticmethod
    def sanitize_input(data: Any) -> Any:
        if isinstance(data, str):
            return html.escape(data.strip())
        elif isinstance(data, dict):
            return {k: BaseValidator.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [BaseValidator.sanitize_input(item) for item in data]
        return data

    @staticmethod
    def validate_by_type(value: str, val_type: ValidatorTypes) -> Any:
        try:
            if val_type == ValidatorTypes.USERNAME:
                if not re.match(r'^[a-zA-Z0-9_]{3,20}$', value):
                    raise ValueError("Invalid username format")
                return value
            elif val_type == ValidatorTypes.EMAIL:
                if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
                    raise ValueError("Invalid email format")
                return value.lower()
            elif val_type == ValidatorTypes.PHONE:
                cleaned = re.sub(r'[^\d+]', '', value)
                if not re.match(r'^\+?[\d\s-]{7,15}$', cleaned):
                    raise ValueError("Invalid phone format")
                return cleaned
            elif val_type == ValidatorTypes.INTEGER:
                return int(value)
            elif val_type == ValidatorTypes.FLOAT:
                return float(value)
            elif val_type == ValidatorTypes.JSON:
                import json
                return json.loads(value)
        except ValueError as e:
            raise InputValidationError(str(e))

    @staticmethod
    def validate_model(data: Dict[str, Any], model: Type[BaseModel]) -> BaseModel:
        try:
            sanitized = BaseValidator.sanitize_input(data)
            return model(**sanitized)
        except ValidationError as e:
            errors = []
            for error in e.errors():
                field = ".".join(str(loc) for loc in error['loc'])
                errors.append(f"{field}: {error['msg']}")
            raise InputValidationError("; ".join(errors))

class TelegramUpdateValidator:
    @staticmethod
    def validate_message(update: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ['message_id', 'from', 'chat', 'date']
        if not all(field in update for field in required_fields):
            raise InputValidationError("Missing required message fields")
        
        if len(update.get('text', '')) > 4096:
            raise InputValidationError("Message text too long")
        
        return {
            'message_id': update['message_id'],
            'user_id': update['from']['id'],
            'chat_id': update['chat']['id'],
            'text': update.get('text', ''),
            'date': datetime.fromtimestamp(update['date'])
        }

class GameDataValidator:
    ITEM_NAME_REGEX = r'^[\w\s-]{1,50}$'
    DRAGON_TYPES = {'fire', 'ice', 'storm', 'earth'}

    @staticmethod
    def validate_dragon_data(data: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        if 'type' not in data or data['type'] not in GameDataValidator.DRAGON_TYPES:
            errors.append("Invalid dragon type")
        
        if 'name' not in data or not re.match(GameDataValidator.ITEM_NAME_REGEX, data['name']):
            errors.append("Invalid dragon name")
        
        if errors:
            raise InputValidationError("; ".join(errors))
        
        return data