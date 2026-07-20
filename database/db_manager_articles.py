import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _get_connection(db_filename: str) -> sqlite3.Connection:
    return sqlite3.connect(os.path.join(BASE_DIR, 'data', db_filename))

# Повертає статтю (номер, назва, текст) за номером з вказаної бази
def get_article_by_number(db_filename: str, number: str) -> dict | None:
    try:
        with _get_connection(db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT number, title, body FROM articles WHERE number = ?',
                (number,)
            )
            row = cursor.fetchone()
            if row:
                return {"number": row[0], "title": row[1], "body": row[2]}
            return None
    except sqlite3.Error as e:
        print(f"Помилка пошуку статті {number} у {db_filename}: {e}")
        return None
    
def get_adjacent_article_number(db_filename: str, number: str, direction: str) -> str | None:
    try:
        with _get_connection(db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT rowid, number FROM articles ORDER BY rowid")
            numbers = [row[1] for row in cursor.fetchall()]
            if number not in numbers:
                return None
            idx = numbers.index(number)
            if direction == "next" and idx + 1 < len(numbers):
                return numbers[idx + 1]
            if direction == "prev" and idx - 1 >= 0:
                return numbers[idx - 1]
            return None
    except sqlite3.Error as e:
        print(f"Помилка навігації у {db_filename}: {e}")
        return None