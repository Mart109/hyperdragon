import sqlite3
from pathlib import Path
from typing import Optional, Dict, List
from backend.config import BackendConfig
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn = self._create_connection()
        self._run_migrations()

    def _create_connection(self) -> sqlite3.Connection:
        """Устанавливает соединение с БД"""
        db_path = Path(BackendConfig.DB_PATH)
        db_path.parent.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Возвращает dict вместо tuple
        return conn

    def _run_migrations(self):
        """Применяет миграции из папки migrations/"""
        with self.conn:
            cursor = self.conn.cursor()
            
            # Создаем таблицу миграций если ее нет
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    name TEXT PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Применяем все непримененные миграции
            applied = {row['name'] for row in cursor.execute("SELECT name FROM migrations")}
            migrations_dir = Path(__file__).parent / "migrations"
            
            for migration_file in sorted(migrations_dir.glob("*.sql")):
                if migration_file.name not in applied:
                    with open(migration_file) as f:
                        cursor.executescript(f.read())
                    cursor.execute("INSERT INTO migrations (name) VALUES (?)", (migration_file.name,))
                    logger.info(f"Applied migration: {migration_file.name}")

    def execute(self, query: str, params=()) -> sqlite3.Cursor:
        """Выполняет SQL-запрос с параметрами"""
        try:
            return self.conn.execute(query, params)
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}\nQuery: {query}")
            raise

    def fetch_one(self, query: str, params=()) -> Optional[Dict]:
        """Возвращает одну строку"""
        return self.execute(query, params).fetchone()

    def fetch_all(self, query: str, params=()) -> List[Dict]:
        """Возвращает все строки"""
        return self.execute(query, params).fetchall()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    # Примеры методов для работы с игроками
    def get_player(self, user_id: int) -> Optional[Dict]:
        return self.fetch_one("SELECT * FROM players WHERE user_id = ?", (user_id,))
        
    def create_dragon(self, owner_id: int, name: str, dragon_type: str) -> bool:
        """Создает нового дракона для игрока"""
        try:
            dragon_id = f"dragon_{owner_id}_{name}"
            self.execute(
                """
                INSERT INTO dragons (id, owner_id, name, type)
                VALUES (?, ?, ?, ?)
                """,
                (dragon_id, owner_id, name, dragon_type)
            )
            
            # Если это первый дракон, делаем его активным
            if not self.get_player(owner_id).get('active_dragon_id'):
                self.execute(
                    "UPDATE players SET active_dragon_id = ? WHERE user_id = ?",
                    (dragon_id, owner_id)
                )
                
            return True
        except sqlite3.Error as e:
            logger.error(f"Create dragon error: {e}")
            return False

    def get_dragon(self, dragon_id: str) -> Optional[Dict]:
        """Получает дракона по ID"""
        return self.fetch_one("SELECT * FROM dragons WHERE id = ?", (dragon_id,))

    def get_player_dragons(self, owner_id: int) -> List[Dict]:
        """Получает всех драконов игрока"""
        return self.fetch_all(
            "SELECT * FROM dragons WHERE owner_id = ? ORDER BY level DESC",
            (owner_id,)
        )

    def get_active_dragon(self, player_id: int) -> Optional[Dict]:
        """Получает активного дракона игрока"""
        player = self.get_player(player_id)
        if not player or not player.get('active_dragon_id'):
            return None
        
        return self.get_dragon(player['active_dragon_id'])

    def set_active_dragon(self, player_id: int, dragon_id: str) -> bool:
        """Устанавливает активного дракона"""
        try:
            # Проверяем, что дракон принадлежит игроку
            dragon = self.get_dragon(dragon_id)
            if not dragon or dragon['owner_id'] != player_id:
                return False
                
            self.execute(
                "UPDATE players SET active_dragon_id = ? WHERE user_id = ?",
                (dragon_id, player_id)
            )
            return True
        except sqlite3.Error as e:
            logger.error(f"Set active dragon error: {e}")
            return False

    def register_player(self, user_id: int, username: str, referrer_id: Optional[int] = None):
    """Регистрация игрока с созданием первого дракона"""    
    try:
        with self.conn:
            # Регистрируем игрока
            self.execute(
                "INSERT OR IGNORE INTO players (user_id, username, referrer_id) VALUES (?, ?, ?)",
                (user_id, username, referrer_id)
            )
            
            # Создаем первого дракона (огненного)
            dragon_id = f"dragon_{user_id}_fire"
            self.execute(
                """
                INSERT OR IGNORE INTO dragons (id, owner_id, name, type)
                VALUES (?, ?, ?, ?)
                """,
                (dragon_id, user_id, "Огненный дракон", "fire")
            )
            
            # Устанавливаем его активным
            self.execute(
                "UPDATE players SET active_dragon_id = ? WHERE user_id = ?",
                (dragon_id, user_id)
            )
    except sqlite3.Error as e:
        logger.error(f"Registration error: {e}")
        raise

     def get_user(self, user_id: int) -> Optional[Dict]:
        """Алиас для get_player (для совместимости с combat.py)"""
        return self.get_player(user_id)

    def get_active_boosts(self, user_id: int) -> List[Dict]:
        """Получает активные бусты игрока (заглушка)"""
        # ⚠️ Временная заглушка - вернет пустой список
        return []

    def update_stats(self, user_id: int, stats: Dict) -> bool:
        """Обновляет статистику игрока (заглушка)"""
        try:
            # ⚠️ Временная заглушка - просто возвращает True
            return True
        except:
            return False

    def transfer_coins(self, sender_id: int, receiver_id: int, amount: int, fee: float = 0.05) -> bool:
      """
      Атомарный перевод монет между пользователями с комиссией
      Args:
          sender_id: ID отправителя
          receiver_id: ID получателя
          amount: Сумма перевода (должна быть > 0)
          fee: Комиссия в долях (0.05 = 5%)
      Returns:
          True если перевод успешен, False при ошибке
      """
      if amount <= 0 or sender_id == receiver_id:
          return False

      total_debit = amount + int(amount * fee)
    
      try:
          with self.conn:  # Используем транзакцию
              # Проверяем баланс отправителя
              sender = self.fetch_one(
                  "SELECT coins FROM players WHERE user_id = ?", 
                  (sender_id,)
              )
              if not sender or sender['coins'] < total_debit:
                  return False
            
              # Списание у отправителя
              self.execute(
                  "UPDATE players SET coins = coins - ? WHERE user_id = ?",
                  (total_debit, sender_id)
              )
            
              # Зачисление получателю
              self.execute(
                  "UPDATE players SET coins = coins + ? WHERE user_id = ?",
                  (amount, receiver_id)
              )
            
              # Логируем операцию (если есть таблица transactions)
              self.execute(
                  """INSERT INTO transactions 
                  (sender_id, receiver_id, amount, fee, timestamp) 
                  VALUES (?, ?, ?, ?, datetime('now'))""",
                  (sender_id, receiver_id, amount, fee)
              )
            
              return True
            
      except sqlite3.Error as e:
          logger.error(f"Transfer failed: {str(e)}")
          return False

    def get_transactions(self, user_id: int, limit: int = 10) -> List[Transaction]:
    """Получает историю переводов пользователя"""    
    rows = self.fetch_all(
        """
        SELECT * FROM transactions 
        WHERE sender_id = ? OR receiver_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (user_id, user_id, limit)
    )
    return [Transaction.from_db_row(row) for row in rows]
    
    def register_user(
        self,
        user_id: int,
        username: str,
        referrer_id: Optional[int] = None
    ) -> bool:
        """Регистрация с проверкой реферера"""    
        try:
            with self.conn:
                # Проверяем, не пытается ли пользователь пригласить сам себя
                if referrer_id == user_id:
                    return False
                
                # Проверяем существование реферера
                if referrer_id and not self.get_player(referrer_id):
                    return False
                
                # Регистрируем пользователя
                self.execute(
                    """
                    INSERT INTO players (user_id, username, referrer_id)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id) DO NOTHING
                    """,
                    (user_id, username, referrer_id)
                )
                
                # Начисляем бонус рефереру
                if referrer_id:
                    self.execute(
                        """
                        UPDATE players 
                        SET 
                            coins = coins + 100,
                            referrals_count = referrals_count + 1
                        WHERE user_id = ?
                        """,
                        (referrer_id,)
                    )
                
                return True
        except sqlite3.Error as e:
            logger.error(f"Registration error: {e}")
            return False

    def get_referral_stats(self, user_id: int) -> Dict:
        """Статистика по рефералам: кол-во и суммарный доход"""
        return self.fetch_one(
            """
            SELECT 
                referrals_count,
                (SELECT SUM(coins) FROM players WHERE referrer_id = ?) AS total_income
            FROM players 
            WHERE user_id = ?
            """,
            (user_id, user_id)
        )

    