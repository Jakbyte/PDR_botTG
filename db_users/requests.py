import sqlite3
from datetime import datetime
from .connect import get_connection

# Додає нового користувача або активує його знову, якщо він повернувся
def add_user(user_id: int, username: str | None, first_name: str) -> bool:
    joined_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (user_id, username, first_name, joined_at, is_active)
                VALUES (?, ?, ?, ?, 1)
                ON CONFLICT(user_id) DO UPDATE SET 
                    username = excluded.username,
                    first_name = excluded.first_name,
                    is_active = 1
            ''', (user_id, username, first_name, joined_at))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"❌ Помилка при додаванні користувача {user_id}: {e}")
        return False

# Позначає користувача як неактивного (якщо він заблокував бота)
def set_user_inactive(user_id: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET is_active = 0 WHERE user_id = ?', (user_id,))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"❌ Помилка при деактивації користувача {user_id}: {e}")
        return False
    
# Повертає загальну кількість користувачів та кількість активних
def get_stats() -> tuple[int, int]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM users")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            active = cursor.fetchone()[0]
            
            return total, active
    except sqlite3.Error as e:
        print(f"❌ Помилка при отриманні статистики: {e}")
        return 0, 0
    
# Повертає список ID всіх активних користувачів для розсилки
def get_active_users() -> list[int]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE is_active = 1")
            return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"❌ Помилка при отриманні списку активних користувачів: {e}")
        return []