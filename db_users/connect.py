import os
import sqlite3
from dotenv import load_dotenv


load_dotenv()

DB_FILE_NAME = os.getenv("DB_NAME")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_DB_PATH = os.path.join(BASE_DIR, DB_FILE_NAME)

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(USERS_DB_PATH)

def init_users_db():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    joined_at TEXT,
                    is_active INTEGER DEFAULT 1
                )
            ''')
            conn.commit()
        print(f"👥 База даних користувачів ({DB_FILE_NAME}) успішно перевірена/ініціалізована!")
    except sqlite3.Error as e:
        print(f"❌ Помилка ініціалізації бази даних користувачів: {e}")