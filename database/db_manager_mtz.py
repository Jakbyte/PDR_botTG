import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "fabula_mtz.db")


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)



def get_mtz_by_article(article_number: str) -> list[dict]:
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, code, article_number, part_number, name, legal_norm, fine, fabula_text "
                "FROM mtz_fabulas WHERE article_number = ? "
                "ORDER BY CAST(part_number AS INTEGER), id",
                (article_number,)
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": r[0], "code": r[1], "article_number": r[2], "part_number": r[3],
                    "name": r[4], "legal_norm": r[5], "fine": r[6], "fabula_text": r[7]
                }
                for r in rows
            ]
    except sqlite3.Error as e:
        print(f"Помилка пошуку фабул МТЗ за статтею {article_number}: {e}")
        return []


# Повертає одну фабулу за id (для показу повного тексту після вибору зі списку)
def get_mtz_fabula_by_id(fabula_id: int) -> dict | None:
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, code, article_number, part_number, name, legal_norm, fine, fabula_text "
                "FROM mtz_fabulas WHERE id = ?",
                (fabula_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0], "code": row[1], "article_number": row[2], "part_number": row[3],
                    "name": row[4], "legal_norm": row[5], "fine": row[6], "fabula_text": row[7]
                }
            return None
    except sqlite3.Error as e:
        print(f"Помилка пошуку фабули МТЗ id={fabula_id}: {e}")
        return None


# Список усіх статей КУпАП, охоплених базою МТЗ (для побудови клавіатури категорій)
def get_mtz_article_list() -> list[str]:
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT article_number FROM mtz_fabulas")
            rows = cursor.fetchall()
            return sorted(
                (r[0] for r in rows),
                key=lambda x: [int(p) if p.isdigit() else p for p in x.split("-")]
            )
    except sqlite3.Error as e:
        print(f"Помилка отримання списку статей МТЗ: {e}")
        return []
    
# Повертає всі фабули МТЗ одним списком (для плаского вибору за назвою)
def get_all_mtz_fabulas() -> list[dict]:
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, code, article_number, part_number, name, legal_norm, fine, fabula_text "
                "FROM mtz_fabulas ORDER BY name"
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": r[0], "code": r[1], "article_number": r[2], "part_number": r[3],
                    "name": r[4], "legal_norm": r[5], "fine": r[6], "fabula_text": r[7]
                }
                for r in rows
            ]
    except sqlite3.Error as e:
        print(f"Помилка отримання всіх фабул МТЗ: {e}")
        return []