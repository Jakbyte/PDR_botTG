import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'neb_fabulas.db')

# 1. Отримати список унікальних головних категорій
def get_adr_categories():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM fabulas WHERE category != 'Скорочення'")
        return [row[0] for row in cursor.fetchall()]

# 2. Отримати список фабул для конкретної категорії
def get_adr_fabulas_by_category(category_name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM fabulas WHERE category = ?", (category_name,))
        return cursor.fetchall() 

# 3. Отримати текст фабули за її ID
def get_adr_fabula_text(fabula_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, fabula_text FROM fabulas WHERE id = ?", (fabula_id,))
        return cursor.fetchone() 