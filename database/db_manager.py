import os
import re
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'pdr.db') 

# Ищет пункт ПДД в базе данных по его ID
def get_rule_by_id(rule_id: str) -> str | None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT text FROM rules WHERE id = ?', (rule_id,))
            result = cursor.fetchone()
            return result[0] if result and result[0] else None
    except sqlite3.Error as e:
        print(f"Помилка роботи з базою даних: {e}")
        return None

def get_points_by_section(section_num: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, text FROM rules WHERE id LIKE ? ORDER BY CAST(REPLACE(id, ?, '') AS INTEGER)", 
            (f"{section_num}.%", f"{section_num}.")
        )
        results = cursor.fetchall()
        points_data = []
        for row in results:
            p_id = row[0]
            p_text = row[1]
            clean_text = re.sub(r'<[^>]+>', '', p_text)
            first_line = clean_text.split('\n')[0].strip()
            if len(first_line) > 35:
                first_line = first_line[:32] + "..."
            points_data.append({
                "id": p_id,
                "title": first_line
            })
        return points_data
    except Exception as e:
        print(f"Помилка отримання пунктів: {e}")
        return []
    finally:
        conn.close()