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

    def _get_user_key(self, user_id: str) -> str:
        return f"{self.user_key_prefix}{user_id}"

    def create_user(self, user: UserProfile) -> bool:
        """Создание нового пользователя"""
        user_key = self._get_user_key(user.id)

        # Проверяем, существует ли пользователь
        if self.db.redis.exists(user_key):
            return False

        # Сохраняем данные пользователя как Hash
        user_data = user.model_dump()
        user_data['created_at'] = user_data['created_at'].isoformat()
        user_data['last_login'] = user_data['last_login'].isoformat()

        # Сохраняем в Redis Hash
        self.db.redis.hset(user_key, mapping=user_data)

        # Добавляем в индекс пользователей
        self.db.redis.sadd(self.user_index_key, user.id)

        return True

    def get_user(self, user_id: str) -> Optional[UserProfile]:
        """Получение пользователя по ID"""
        user_key = self._get_user_key(user_id)

        if not self.db.redis.exists(user_key):
            return None

        user_data = self.db.redis.hgetall(user_key)

        # Преобразуем строки обратно в datetime
        user_data['created_at'] = datetime.fromisoformat(user_data['created_at'])
        user_data['last_login'] = datetime.fromisoformat(user_data['last_login'])

        return UserProfile(**user_data)

    def update_user(self, user_id: str, **updates) -> bool:
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

    def delete_user(self, user_id: str) -> bool:
        """Удаление пользователя"""
        user_key = self._get_user_key(user_id)

        if not self.db.redis.exists(user_key):
            return False

        # Удаляем из индекса
        self.db.redis.srem(self.user_index_key, user_id)
        # Удаляем данные пользователя
        self.db.redis.delete(user_key)

        return True

    def get_all_users(self) -> List[UserProfile]:
        """Получение всех пользователей"""
        user_ids = self.db.redis.smembers(self.user_index_key)
        users = []

        for user_id in user_ids:
            user = self.get_user(user_id)
            if user:
                users.append(user)

        return users

    def add_experience(self, user_id: str, exp: int) -> bool:
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

    def add_coins(self, user_id: str, coins: int) -> bool:
        """Добавление/уменьшение монет"""
        user_key = self._get_user_key(user_id)

        if not self.db.redis.exists(user_key):
            return False

        self.db.redis.hincrby(user_key, 'coins', coins)
        return True

    def update_last_login(self, user_id: str) -> bool:
        """Обновление времени последнего входа"""
        return self.update_user(
            user_id,
            last_login=datetime.now(timezone.utc)
        )


class UserService:
    def __init__(self):
        self.redis_db = RedisDB()
        self.user_repo = UserRepository(self.redis_db)

    def register_user(self, username: str) -> Optional[UserProfile]:
        """Регистрация нового пользователя"""
        import uuid

        user_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        user = UserProfile(
            id=user_id,
            username=username,
            level=1,
            experience=0,
            coins=100,
            created_at=now,
            last_login=now
        )

        if self.user_repo.create_user(user):
            return user
        return None

    def login_user(self, user_id: str) -> Optional[UserProfile]:
        """Вход пользователя"""
        user = self.user_repo.get_user(user_id)
        if user:
            self.user_repo.update_last_login(user_id)
            return user
        return None

    def get_user_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
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

