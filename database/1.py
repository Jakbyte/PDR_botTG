import sqlite3

# Імпортуємо правильну назву словника з вашого файлу
from fabula_neb import adrs_dictionary 

def create_and_fill_neb_db():
    # 1. Створюємо підключення до нової бази даних
    conn = sqlite3.connect("neb_fabulas.db")
    cursor = conn.cursor()

    # 2. Створюємо таблицю для фабул
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fabulas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        subcategory TEXT,
        title TEXT,
        fabula_text TEXT
    )
    ''')

    # Очищаємо таблицю перед записом (якщо скрипт запускається не вперше)
    cursor.execute('DELETE FROM fabulas')

    # 3. Парсимо словник і записуємо в БД
    # Використовуємо правильну змінну: adrs_dictionary
    for cat_name, cat_content in adrs_dictionary.items():
        if isinstance(cat_content, dict):
            for subcat_name, subcat_content in cat_content.items():
                if isinstance(subcat_content, dict):
                    for title_key, text_val in subcat_content.items():
                        if isinstance(text_val, dict):
                            # Глибока вкладеність (4 рівні)
                            for item_title, item_text in text_val.items():
                                full_title = f"{title_key} {item_title}"
                                cursor.execute(
                                    'INSERT INTO fabulas (category, subcategory, title, fabula_text) VALUES (?, ?, ?, ?)',
                                    (cat_name, subcat_name, full_title, item_text)
                                )
                        else:
                            # 3 рівні вкладеності
                            cursor.execute(
                                'INSERT INTO fabulas (category, subcategory, title, fabula_text) VALUES (?, ?, ?, ?)',
                                (cat_name, subcat_name, title_key, text_val)
                            )
                else:
                    # 2 рівні вкладеності
                    cursor.execute(
                        'INSERT INTO fabulas (category, subcategory, title, fabula_text) VALUES (?, ?, ?, ?)',
                        (cat_name, cat_name, subcat_name, subcat_content)
                    )
        else:
            # 1 рівень (простий список ключ-значення)
            cursor.execute(
                'INSERT INTO fabulas (category, subcategory, title, fabula_text) VALUES (?, ?, ?, ?)',
                ("Загальне", "Загальне", cat_name, cat_content)
            )

    # Зберігаємо зміни та закриваємо з'єднання
    conn.commit()
    conn.close()
    print("✅ База даних 'neb_fabulas.db' успішно створена та наповнена!")

if __name__ == "__main__":
    create_and_fill_neb_db()