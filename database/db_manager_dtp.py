import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'fabula_dtp.db')

def get_accidents_by_violation(violation_name: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, pdr_rule, violation_title 
            FROM accident_cases 
            WHERE violation_title = ?
        """, (violation_name,))
        
        rows = cursor.fetchall()
        return [{"id": r[0], "pdr_rule": r[1], "title": r[2]} for r in rows]
    except sqlite3.Error as e:
        print(f"Помилка пошуку фабул за категорією: {e}")
        return []
    finally:
        conn.close()

def get_accidents_by_rule(rule_query: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        rule_clean = rule_query.strip()
        cursor.execute("""
            SELECT id, pdr_rule, violation_title 
            FROM accident_cases 
            WHERE pdr_rule LIKE ? 
               OR pdr_rule LIKE ? 
               OR pdr_rule LIKE ?
               OR pdr_rule = ?
        """, (f"{rule_clean},%", f"%, {rule_clean}%", f"% {rule_clean}%", rule_clean))
        
        rows = cursor.fetchall()
        return [{"id": r[0], "pdr_rule": r[1], "title": r[2]} for r in rows]
    except sqlite3.Error as e:
        print(f"Помилка пошуку фабул за пунктом ПДР: {e}")
        return []
    finally:
        conn.close()

def get_accidents_by_section(section_number: int) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, pdr_rule, violation_title 
            FROM accident_cases 
            WHERE pdr_rule LIKE ? 
               OR pdr_rule LIKE ?
        """, (f"{section_number}.%", f"%, {section_number}.%"))
        
        rows = cursor.fetchall()
        return [{"id": r[0], "pdr_rule": r[1], "title": r[2]} for r in rows]
    except sqlite3.Error as e:
        print(f"Помилка пошуку фабул за номером розділу: {e}")
        return []
    finally:
        conn.close()

def get_accident_by_id(accident_id: int) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT pdr_rule, violation_title, fabula 
            FROM accident_cases 
            WHERE id = ?
        """, (accident_id,))
        
        row = cursor.fetchone()
        if row:
            return {
                "pdr_rule": row[0],
                "violation_title": row[1],
                "fabula": row[2]
            }
        return None
    except sqlite3.Error as e:
        print(f"Помилка отримання фабули за ID: {e}")
        return None
    finally:
        conn.close()