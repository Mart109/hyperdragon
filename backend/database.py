import json
import redis
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timezone
from models import UserProfile


class RedisDB:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
            encoding='utf-8'
        )

    def ping(self):
        return self.redis.ping()

    def close(self):
        self.redis.close()


class UserRepository:
    def __init__(self, redis_db: RedisDB):
        self.db = redis_db
        self.user_key_prefix = "user:"
        self.user_index_key = "users:index"
        self.username_to_id_key = "username_to_id"  # Новый индекс для уникальных username

    def _get_user_key(self, user_id: int) -> str:  # Изменено на int
        return f"{self.user_key_prefix}{user_id}"

    def is_username_taken(self, username: str) -> bool:
        """Проверяет, занят ли username"""
        if not username:  # Если username пустой
            return False
        return self.db.redis.hexists(self.username_to_id_key, username.lower())

    def get_user_by_username(self, username: str) -> Optional[UserProfile]:
        """Находит пользователя по username"""
        if not username:
            return None

        user_id = self.db.redis.hget(self.username_to_id_key, username.lower())
        if user_id:
            return self.get_user(int(user_id))
        return None

    def create_user(self, user: UserProfile) -> bool:
        """Создание нового пользователя с проверкой уникальности username"""
        user_key = self._get_user_key(user.user_id)  # Используем user_id вместо id

        # Проверяем, существует ли пользователь
        if self.db.redis.exists(user_key):
            return False

        # Проверяем, занят ли username (если он не пустой)
        if user.username and self.is_username_taken(user.username):
            return False

        # Сохраняем данные пользователя как Hash
        user_data = user.model_dump()
        user_data['created_at'] = user_data['created_at'].isoformat()
        user_data['last_login'] = user_data['last_login'].isoformat()

        # Сохраняем в Redis Hash
        self.db.redis.hset(user_key, mapping=user_data)

        # Добавляем в индекс пользователей
        self.db.redis.sadd(self.user_index_key, user.user_id)

        # Добавляем в индекс username -> user_id (если username не пустой)
        if user.username:
            self.db.redis.hset(self.username_to_id_key, user.username.lower(), user.user_id)

        return True

    def get_user(self, user_id: int) -> Optional[UserProfile]:  # Изменено на int
        """Получение пользователя по ID"""
        user_key = self._get_user_key(user_id)

        if not self.db.redis.exists(user_key):
            return None

        user_data = self.db.redis.hgetall(user_key)

        # Преобразуем строки обратно в datetime
        user_data['created_at'] = datetime.fromisoformat(user_data['created_at'])
        user_data['last_login'] = datetime.fromisoformat(user_data['last_login'])

        return UserProfile(**user_data)

    def update_user(self, user_id: int, **updates) -> bool:  # Изменено на int
        """Обновление данных пользователя"""
        user_key = self._get_user_key(user_id)

        if not self.db.redis.exists(user_key):
            return False

        # Обрабатываем специальные поля
        if 'last_login' in updates:
            updates['last_login'] = updates['last_login'].isoformat()

        # Обновляем поля
        for field, value in updates.items():
            self.db.redis.hset(user_key, field, str(value))

        return True

    def update_username(self, user_id: int, new_username: str) -> bool:
        """Обновляет username пользователя с проверкой уникальности"""
        user_key = self._get_user_key(user_id)

        if not self.db.redis.exists(user_key):
            return False

        # Проверяем, занят ли новый username
        if self.is_username_taken(new_username):
            return False

        # Получаем старый username
        old_username = self.db.redis.hget(user_key, 'username')

        # Удаляем старый username из индекса
        if old_username:
            self.db.redis.hdel(self.username_to_id_key, old_username.lower())

        # Обновляем username в данных пользователя
        self.db.redis.hset(user_key, 'username', new_username)

        # Добавляем новый username в индекс
        if new_username:
            self.db.redis.hset(self.username_to_id_key, new_username.lower(), user_id)

        return True

    def delete_user(self, user_id: int) -> bool:  # Изменено на int
        """Удаление пользователя"""
        user_key = self._get_user_key(user_id)

        if not self.db.redis.exists(user_key):
            return False

        # Удаляем username из индекса
        username = self.db.redis.hget(user_key, 'username')
        if username:
            self.db.redis.hdel(self.username_to_id_key, username.lower())

        # Удаляем из индекса пользователей
        self.db.redis.srem(self.user_index_key, user_id)
        # Удаляем данные пользователя
        self.db.redis.delete(user_key)

        return True

    def get_all_users(self) -> List[UserProfile]:
        """Получение всех пользователей"""
        user_ids = self.db.redis.smembers(self.user_index_key)
        users = []

        for user_id in user_ids:
            user = self.get_user(int(user_id))  # Конвертируем в int
            if user:
                users.append(user)

        return users

    def add_experience(self, user_id: int, exp: int) -> bool:  # Изменено на int
        """Добавление опыта пользователю"""
        user_key = self._get_user_key(user_id)

        if not self.db.redis.exists(user_key):
            return False

        # Используем HINCRBY для атомарного увеличения
        new_exp = self.db.redis.hincrby(user_key, 'experience', exp)

        # Проверяем уровень (пример: каждые 100 опыта - новый уровень)
        current_level = int(self.db.redis.hget(user_key, 'level'))
        new_level = current_level + (new_exp // 100) - (current_level * 100 // 100)

        if new_level > current_level:
            self.db.redis.hset(user_key, 'level', new_level)

        return True

    def add_coins(self, user_id: int, coins: int) -> bool:  # Изменено на int
        """Добавление/уменьшение монет"""
        user_key = self._get_user_key(user_id)

        if not self.db.redis.exists(user_key):
            return False

        self.db.redis.hincrby(user_key, 'coins', coins)
        return True

    def update_last_login(self, user_id: int) -> bool:  # Изменено на int
        """Обновление времени последнего входа"""
        return self.update_user(
            user_id,
            last_login=datetime.now(timezone.utc)
        )


class TelegramUserService:
    def __init__(self):
        self.redis_db = RedisDB()
        self.user_repo = UserRepository(self.redis_db)

    def register_telegram_user(self, telegram_user_id: int, username: str, first_name: str) -> Optional[UserProfile]:
        """Регистрация пользователя из Telegram"""
        now = datetime.now(timezone.utc)

        # Если username уже занят - используем пустую строку
        if username and self.user_repo.is_username_taken(username):
            username = ""

        user = UserProfile(
            user_id=telegram_user_id,  # Используем Telegram ID
            username=username or "",
            first_name=first_name,
            level=1,
            experience=0,
            coins=100,
            created_at=now,
            last_login=now
        )

        if self.user_repo.create_user(user):
            return user
        return None

    def get_or_create_user(self, telegram_user_id: int, username: str, first_name: str) -> Optional[UserProfile]:
        """Автоматическая регистрация/вход для Telegram"""
        user = self.user_repo.get_user(telegram_user_id)

        if user:
            # Если username изменился и не занят - обновляем
            if (username and
                    username != user.username and
                    not self.user_repo.is_username_taken(username)):
                self.user_repo.update_username(telegram_user_id, username)

            # Обновляем последний вход
            self.user_repo.update_last_login(telegram_user_id)
            return user
        else:
            # Создаем нового пользователя
            return self.register_telegram_user(telegram_user_id, username, first_name)

    def set_custom_username(self, user_id: int, desired_username: str) -> bool:
        """Установка кастомного username"""
        # Проверяем формат
        if not desired_username or len(desired_username) < 3:
            return False

        # Проверяем, что содержит только буквы, цифры и _
        if not desired_username.replace('_', '').isalnum():
            return False

        return self.user_repo.update_username(user_id, desired_username)

    def get_user_stats(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение статистики пользователя"""
        user = self.user_repo.get_user(user_id)
        if not user:
            return None

        return {
            'username': user.username,
            'first_name': user.first_name,
            'level': user.level,
            'experience': user.experience,
            'coins': user.coins,
            'next_level_exp': (user.level * 100) - user.experience
        }

    def find_user_by_username(self, username: str) -> Optional[UserProfile]:
        """Поиск пользователя по username"""
        return self.user_repo.get_user_by_username(username)


# Старый UserService оставлен для обратной совместимости
class UserService:
    def __init__(self):
        self.redis_db = RedisDB()
        self.user_repo = UserRepository(self.redis_db)

    def register_user(self, username: str) -> Optional[UserProfile]:
        """Регистрация нового пользователя (для не-Telegram использования)"""
        import uuid

        user_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        user = UserProfile(
            user_id=int(user_id[:8], 16),  # Генерируем числовой ID из UUID
            username=username,
            first_name="User",  # Заглушка
            level=1,
            experience=0,
            coins=100,
            created_at=now,
            last_login=now
        )

        if self.user_repo.create_user(user):
            return user
        return None

    def login_user(self, user_id: int) -> Optional[UserProfile]:
        """Вход пользователя"""
        user = self.user_repo.get_user(user_id)
        if user:
            self.user_repo.update_last_login(user_id)
            return user
        return None

    def get_user_stats(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение статистики пользователя"""
        user = self.user_repo.get_user(user_id)
        if not user:
            return None

        return {
            'username': user.username,
            'level': user.level,
            'experience': user.experience,
            'coins': user.coins,
            'next_level_exp': (user.level * 100) - user.experience
        }


