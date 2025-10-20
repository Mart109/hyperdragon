import sqlite3
from datetime import datetime
import asyncio

DB_PATH = "hyprdragon.db"

def init_database():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                coins INTEGER DEFAULT 100,
                created_at TIMESTAMP NOT NULL
            )
        ''')
        conn.commit()
        print("База данных hyprdragon.db инициализирована")

def user_exists(username: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
        return cursor.fetchone() is not None

def create_user_sync(username: str) -> dict:
    try:
        now = datetime.now()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, first_name, level, experience, coins, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, username, 1, 0, 100, now.isoformat()))
            conn.commit()
            user_id = cursor.lastrowid
        return {
            "success": True,
            "new_user": True,
            "user_id": user_id,
            "username": username,
            "coins": 100,
            "level": 1,
            "experience": 0
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_user_sync(username: str) -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id, username, level, experience, coins, created_at
            FROM users WHERE username = ?
        ''', (username,))
        result = cursor.fetchone()
        if result:
            return {
                "success": True,
                "new_user": False,
                "user_id": result[0],
                "username": result[1],
                "level": result[2],
                "experience": result[3],
                "coins": result[4],
                "created_at": result[5]
            }
        else:
            return {"success": False, "error": "Пользователь не найден"}

def login_or_register_sync(username: str) -> dict:
    if user_exists(username):
        return get_user_sync(username)
    else:
        return create_user_sync(username)

def add_coins_sync(username: str, amount: int) -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET coins = coins + ? WHERE username = ?', (amount, username))
        conn.commit()
        if cursor.rowcount > 0:
            return {"success": True}
        return {"success": False, "error": "Пользователь не найден"}

def add_experience_sync(username: str, amount: int) -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET experience = experience + ? WHERE username = ?', (amount, username))
        conn.commit()
        if cursor.rowcount > 0:
            return {"success": True}
        return {"success": False, "error": "Пользователь не найден"}

async def process_command():
    while True:
        cmd = input(">>> ").strip().split()
        if not cmd:
            continue
        command = cmd[0].lower()
        if command == "exit":
            print("Выход из системы.")
            break
        elif command == "login" and len(cmd) == 2:
            username = cmd[1]
            result = await asyncio.to_thread(login_or_register_sync, username)
            print(result)
        elif command == "coins" and len(cmd) == 3:
            username, amount = cmd[1], int(cmd[2])
            result = await asyncio.to_thread(add_coins_sync, username, amount)
            print(result)
        elif command == "exp" and len(cmd) == 3:
            username, amount = cmd[1], int(cmd[2])
            result = await asyncio.to_thread(add_experience_sync, username, amount)
            print(result)
        elif command == "get" and len(cmd) == 2:
            username = cmd[1]
            result = await asyncio.to_thread(get_user_sync, username)
            print(result)
        else:
            print("Команды:")
            print(" login <username>  — вход или регистрация")
            print(" coins <username> <amount> — изменить монеты")
            print(" exp <username> <amount> — изменить опыт")
            print(" get <username> — показать данные")
            print(" exit — выйти")

async def main():
    init_database()
    print("Система hyprdragon запущена. Введите команду:")
    await process_command()

if __name__ == "__main__":
    asyncio.run(main())
