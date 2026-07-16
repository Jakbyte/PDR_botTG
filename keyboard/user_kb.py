from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- КЛАВІАТУРИ ГОЛОВНОГО МЕНЮ ТА НАВІГАЦІЇ ---

# Клавіатура головного меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📘 ПДР України'),
            KeyboardButton(text="⚖️ Фабули"),
            KeyboardButton(text="ℹ Про бота")
        ]
    ],
    resize_keyboard=True
)

# Опції всередині ПДР
pdr_options_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔢 Пошук за номером пункту")],
        [KeyboardButton(text="📚 Розділи ПДР")],
        [KeyboardButton(text="⬅ Назад")]
    ],
    resize_keyboard=True
)

# Меню вибору типу фабул
fabula_type_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚦 Фабули ПДР"),
            KeyboardButton(text="🛡️ Фабули ГБ")
        ],
        [
            KeyboardButton(text="🚗 Фабули ДТП")
        ],
        [
            KeyboardButton(text="⬅ Назад до головного")
        ]
    ],
    resize_keyboard=True
)

# Підменю для розділу "Фабули ПДР"
pdr_fabula_submenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☣️ Небезпечні вантажі"),
            KeyboardButton(text="🚦 Інші порушення ПДР")
        ],
        [
            KeyboardButton(text="⬅ Назад")
        ]
    ],
    resize_keyboard=True
)

# Кнопка повернення під час ручного пошуку пункту
pdr_search_back_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='⬅ Назад до menu ПДР')]
    ],
    resize_keyboard=True
)


# --- СПИСКИ ДАНИХ ДЛЯ ІНЛАЙН-КЛАВІАТУР ---

SECTIONS = [
    "1. Загальні положення",
    "2. Обов'язки і права водіїв механічних ТЗ",
    "3. Рух ТЗ із спеціальними сигналами",
    "4. Обов'язки і права пішоходів",
    "5. Обов'язки і права пасажирів",
    "6. Вимоги до велосипедистів",
    "7. Вимоги до осіб, які керують гужовим транспортом",
    "8. Регулювання дорожнього руху",
    "9. Попереджувальні сигнали",
    "10. Початок руху та зміна його напрямку",
    "11. Розташування ТЗ на дорозі",
    "12. Швидкість руху",
    "13. Дистанція, інтервал, зустрічний роз'їзд",
    "14. Обгін",
    "15. Зупинка і стоянка",
    "16. Проїзд перехресть",
    "17. Переваги маршрутних ТЗ",
    "18. Проїзд пішохідних переходів і зупинок ТЗ",
    "19. Користування зовнішніми світловими приладами",
    "20. Рух через залізничні переїзди",
    "21. Перевезення пасажирів",
    "22. Перевезення вантажу",
    "23. Буксирування та експлуатація транспортних составів",
    "24. Навчальна їзда",
    "25. Рух транспортних засобів у колонах",
    "26. Рух у житловій та пішохідній зоні",
    "27. Рух по автомагістралях і дорогах для автомобілів",
    "28. Рух по гірських дорогах і на крутих спусках",
    "29. Міжнародний рух",
    "30. Номерні, розпізнавальні знаки, написи і позначення",
    "31. Технічний стан ТЗ та їх обладнання",
    "32. Окремі питання дорожнього руху, що потребують узгодження"
]

SECTIONS_DTP = [
    "КРІПЛЕННЯ ВАНТАЖУ", "ТЕХНІЧНО СПРАВНИЙ СТАН", "ВІДВОЛІКСЯ, ДИСТАНЦІЯ",
    "ВІДВОЛІКСЯ НА ПЕРЕШКОДУ", "ПРОЇЗД НА ЧЕРВОНИЙ", "ВИМКНУТИЙ СИГНАЛ ДОДАТКОВОЇ СЕКЦІЇ",
    "ПРОЇЗД НА ЖОВТИЙ", "РУХ ЗАДНІМ ХОДОМ НА ПЕРЕХРЕСТІ", "ЗМІНА НАПРЯМКУ РУХУ, БОКОВИЙ ІНТЕРВАЛ",
    "ЗМІНА НАПРЯМКУ РУХУ", "ЗМІНА НАПРЯМКУ, НЕБЕЗПЕКА ДЛЯ РУХУ", "ПОЧАТОК РУХУ (ЗЛАМАВ ПІСТОЛЕТ НА АЗС)",
    "ПОЧАТОК ТА ЗМІНА НАПРЯМКУ РУХУ", "ПОЧАТОК РУХУ НА ПЕРЕШКОДУ", "ОДНОЧАСНЕ ПЕРЕСТРОЮВАННЯ",
    "ПЕРЕСТРОЮВАННЯ", "KRAЙНЄ ПОЛОЖЕННЯ ПОВОРОТ ЛІВОРУЧ", "ВИЇЗД З ПРИЛЕГЛОЇ ТЕРИТОРІЇ",
    "KRAЙНЄ ПОЛОЖЕННЯ ПОВОРОТ ПРАВОРУЧ", "ПОВОРОТ ЛІВОРУЧ, ЗУСТРІЧНИЙ ТРАНСПОРТ",
    "РОЗВОРОТ, ЗУСТРІЧНИЙ ТРАНСПОРТ", "РОЗВОРОТ, ПОПУТНИЙ ТРАНСПОРТ", "ВИЇЗД НА ЗУСТРІЧНУ СМУГУ ПРИ ПОВОРОТІ",
    "РУХ ЗАДНІМ ХОДОМ, БОКОВИЙ ІНТЕРВАЛ", "РУХ ЗАДНІМ ХОДОМ", "ПЕРЕШКОДА З ПРАВА (ПОЗА ПЕРЕХРЕСТЯМ)",
    "БЕЗПЕЧНА ШВИДКІСТЬ, ЗУСТРІЧНИЙ РОЗ'ЇЗД", "БЕЗПЕЧНА ШВИДКІСТЬ ПРИ ПОВОРОТІ НА ПРАВО",
    "БЕЗПЕЧНА ШВИДКІСТЬ, НЕБЕЗПЕКА ДЛЯ РУХУ", "НАЇЗД НА ПЕРЕШКОДУ (ПАРКАН)", "НАЇЗД НА ТВАРИНУ (СОБАКА)",
    "ДИСТАНЦІЯ (ТРИ МАШИНИ)", "БЕЗПЕЧНА ШВИДКІСТЬ, ДИСТАНЦІЯ", "ОБГІН ТРИ МАШИНИ",
    "БЕЗПЕЧНА ШВИДКІСТЬ, ВІДВОЛІКСЯ", "НА ЗУСТРІЧНУ СМУГУ", "БЕЗПЕЧНА ШВИДКІСТЬ (ОЖЕЛЕДЬ)",
    "НЕБЕЗПЕКА ДЛЯ РУХУ, БОКОВИЙ ІНТЕРВАЛ", "НЕБЕЗПЕКА ДЛЯ РУХУ", "НЕБЕЗПЕКА, СТАН ПРОЇЗНОЇ ЧАСТИНИ",
    "БОКОВИЙ ІНТЕРВАЛ (НА ПЕРЕШКОДУ)", "БОКОВИЙ ІНТЕРВАЛ", "ДИСТАНЦІЯ, СТАН ПРОЇЗНОЇ ЧАСТИНИ",
    "ДИСТАНЦІЯ (ЗА КЕРМОМ УЧЕНЬ)", "БЕЗПЕЧНА ДИСТАНЦІЯ", "ЗУСТРІЧНИЙ РОЗ'ЇЗД, НА ЗУСТРІЧНУ СМУГУ",
    "ЗУСТРІЧНИЙ РОЗ'ЇЗД", "ОБГІН В ЗОНІ ДІЇ ЗНАКУ 'ОБГІН ЗАБОРОНЕНО'", "ОБГІН ПРИ ЛІВОМУ ПОВОРОТІ ПОПЕРЕДУ",
    "ОБГІН НА ПЕРЕХРЕСТІ", "ОБГІН БІЛЯ ПІШОХІДНОГО ПЕРЕХОДУ", "САМОВІЛЬНИЙ РУХ ТРАНСПОРТУ",
    "ВІДКРИВАННЯ ДВЕРЕЙ", "ПОВОРОТ ЛІВОРУЧ НА ЗЕЛЕНЕ СВІТЛОФОРА", "РІВНОЗНАЧНЕ ПЕРЕХРЕСТЯ (ПЕРЕШКОДА ПРАВОРУЧ)",
    "ПОВОРОТ НА ЛІВО ПРИ ЖОВТОМУ МИГОТІННІ СВІТЛОФОРА", "ПЕРЕХРЕСТЯ ЗАКІНЧЕННЯ МАНЕВРУ",
    "ВИТВОРЕННЯ ЗАТОРУ НА ПЕРЕХРЕСТІ", "ВИЇЗД З ДРУГОРАДНОЇ ДОРОГИ", "ВИЇЗД НА ЗУСТРІЧНУ СМУГУ ДЛЯ МАРШРУТОК",
    "ПЕРЕШКОДА АВТОБУСУ ВІД ЗАЇЗНОЇ КИШЕНІ", "НЕ НАДАВ ПЕРЕВАГИ ПІШОХОДУ НА ПЕРЕХОДІ"
]

ADR_MAP = {
    "Перевізні документи": "📄 Перевізні документи",
    "Письмова інструкція": "ℹ️ Письмова інструкція",
    "Національний дозвіл (маршрут руху)": "🗺️ Дозвіл (маршрут руху)",
    "Копія договору обов’язкового страхування відповідальності суб’єктів перевезення небезпечних вантажів на випадок настання негативних наслідків під час перевезення небезпечних вантажів": "🛡️ Страховий договір",
    "Свідоцтво про допущення транспортних засобів до перевезення визначених небезпечних вантажів": "🚚 Свідоцтво допуску ТЗ",
    "Свідоцтво ДОПНВ про підготовку водія": "🪪 Свідоцтво ДОПНВ водія",
    "Вантаж допущено до перевезення вантажу": "📦 Допуск вантажу",
    "Транспортні засоби є придатними до перевезення небезпечних вантажів": "🛠️ Придатність ТЗ",
    "Положення з перевезення (навалом, в упаковках, у цистернах)": "⚖️ Режими перевезення",
    "Навантаження, розміщення і кріплення вантажу": "🏗️ Кріплення вантажу",
    "Маркування та знаки небезпеки": "⚠️ Маркування & знаки",
    "Додаткове обладнання та засоби індивідуального захисту": "🧰 Обладнання та ЗІЗ"
}
SECTIONS_ADR = list(ADR_MAP.keys())
# --- ФУНКЦІЇ ДИНАМІЧНИХ ІНЛАЙН-КЛАВІАТУР (З ПАГІНАЦІЄЮ) ---

def get_dtp_sections_keyboard(page: int = 1, per_page: int = 6) -> InlineKeyboardMarkup:
    total_pages = (len(SECTIONS_DTP) + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    buttons = []

    for section in SECTIONS_DTP[start_idx:end_idx]:
        idx = SECTIONS_DTP.index(section)
        display_name = section if len(section) <= 35 else section[:32] + "..."
        buttons.append([InlineKeyboardButton(text=f"📂 {display_name}", callback_data=f"dtp_sect:{idx}")])

    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"dtp_page:{page - 1}"))
    else:
        nav_row.append(InlineKeyboardButton(text="❌ Перша", callback_data="noop"))
        
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
    
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"dtp_page:{page + 1}"))
    else:
        nav_row.append(InlineKeyboardButton(text="❌ Остання", callback_data="noop"))
        
    buttons.append(nav_row)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_sections_keyboard(page: int = 1) -> InlineKeyboardMarkup:
    per_page = 7
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_sections = SECTIONS[start_idx:end_idx]
    
    buttons = []
    for idx, section in enumerate(page_sections):
        actual_num = start_idx + idx + 1
        buttons.append([InlineKeyboardButton(text=section, callback_data=f"section:{actual_num}")])
        
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page:{page-1}"))
        
    nav_row.append(InlineKeyboardButton(text=f" сторінка {page}/5 ", callback_data="noop"))
    
    if end_idx < len(SECTIONS):
        nav_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page:{page+1}"))
        
    buttons.append(nav_row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- ФУНКЦІЇ ДИНАМІЧНИХ ІНЛАЙН-КЛАВІАТУР ДЛЯ ADR ---

def get_adr_sections_keyboard(page: int = 1, per_page: int = 6) -> InlineKeyboardMarkup:
    total_pages = (len(SECTIONS_ADR) + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    buttons = []

    # Беремо зріз категорій для поточної сторінки
    for idx in range(start_idx, min(end_idx, len(SECTIONS_ADR))):
        db_name = SECTIONS_ADR[idx]
        # Отримуємо коротку назву зі словника (якщо раптом немає — лишаємо оригінал)
        display_name = ADR_MAP.get(db_name, db_name)
        
        buttons.append([InlineKeyboardButton(text=display_name, callback_data=f"adr_sect:{idx}")])

    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"adr_page:{page - 1}"))
    else:
        nav_row.append(InlineKeyboardButton(text="❌ Перша", callback_data="noop"))
        
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
    
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"adr_page:{page + 1}"))
    else:
        nav_row.append(InlineKeyboardButton(text="❌ Остання", callback_data="noop"))
        
    buttons.append(nav_row)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_adr_fabulas_keyboard(fabulas, category_idx: int, page: int = 1):
    builder = InlineKeyboardBuilder()
    start_idx = (page - 1) * 5
    end_idx = start_idx + 5
    page_fabulas = fabulas[start_idx:end_idx]
    
    category_name = ""
    if 0 <= category_idx < len(SECTIONS_ADR):
        category_name = SECTIONS_ADR[category_idx]

    for f in page_fabulas:
        title = f[1] if isinstance(f, tuple) else f['title']
        fabula_id = f[0] if isinstance(f, tuple) else f['id']
        cleaned_title = title

        # 1. Вирізаємо назву категорії та загальні шаблони з початку
        if category_name:
            cleaned_title = cleaned_title.replace(f"{category_name}:", "").replace(category_name, "")
        
        replacements_to_remove = [
            "Невірно заповнена ТТН:", "Невірно заповнена ТТН",
            "Невірно заповнений", "Невірно заповнені", "Порушення правил"
        ]
        for r in replacements_to_remove:
            if cleaned_title.startswith(r):
                cleaned_title = cleaned_title.replace(r, "", 1).strip()
        
        cleaned_title = cleaned_title.strip().lstrip(",:- ").strip()

        exact_replacements = {
            # Категорія ТТН та Інструкції
            "немає: номер ООН з передуючими літерами UN": "Немає номера ООН (UN)",
            "немає: належне вантажне найменування відповідно до таблиці А глави 3.2 ДОПНВ": "Немає назви вантажу",
            "немає: номер зразка небезпеки, який вказаний в колонці 5 чи спеціальних положеннях колонці 6 таблиці А Глави 3.2. ДОПНВ": "Немає № зразка небезпеки",
            "немає: групу пакування даної позиції з колонки 4 таблиці А Глави 3.2": "Немає групи пакування",
            "немає: об’єм, масу нетто чи брутто, в залежності від вантажу": "Немає об'єму або маси",
            "немає: код обмеження проїзду через тунель (якщо він назначений)": "Немає коду тунелю",
            "Відсутній класифікаційний код вантажу в ТТН (наприклад: 1.1D, 1.4G, 1.6N і т.д.)": "Відсутній клас-код вантажу",
            "В ТТН не вказано кількість, вид та опис упаковок": "Не вказано кількість/опис упаковок",
            "Письмова інструкція старого зразку від ДОПНВ 2015, 2013 років": "Інструкція старого зразка",
            "Письмова інструкція не відповідає вимогам ДОПНВ 2019 року": "Інструкція не відповідає ДОПНВ",
            
            # Категорія Маршрути та Страховка
            "Відсутній маршрут для вантажів підвищеної небезпеки": "Відсутній маршрут для НВ",
            "Відсутній маршрут на транспортній одиниці (ТО) для вантажів підвищеної небезпеки": "Відсутній маршрут на ТО",
            "Перевантаження НВ відповідно до маршруту (більше ніж м маршруті)": "Перевантаження НВ по маршруту",
            "Відхилення від маршруту руху при перевезення НВ підвищенної небезпеки": "Відхилення від маршруту",
            "Не було на ТО страховки на вантаж": "Відсутня страховка на вантаж",
            "В страховці на вантаж не визначено днз ТЗ": "В страховці не вказано ДНЗ ТЗ",
            "В страховці на вантаж не визначено номер ООН вантажу": "В страховці відсутній № ООН",
            
            # Свідоцтва та ТЗ
            "Не було відкрито категорії для перевезення НВ 1 класу": "Немає категорії НВ 1 класу",
            "Заборона перевезення НВ відповідно до таблиці А Глави 3.2 ДОПНВ": "Заборона перевезення НВ",
            "Відсутнє буквене позначення ТЗ (EXII, EX III, FL, AT, MEMU) передбачене колонкою 14 таблиці А Глави 3.2 та підрозділом 9.1.1.2 ДОПНВ": "Відсутнє маркування ТЗ",
            "Перевантаження вибухової речовини відповідно до таблиці 7.5.5.2.1 ДОПНВ": "Перевантаження вибухівки",
            
            # Цистерни та Таблички
            "На цистерні відсутня корозієстійка металева табличка (сертифікація)": "Відсутня табличка цистерни",
            "Відсутня табличка Оператора на автоцистерні передбачена п.6.8.2.5.2 ДОПНВ": "Немає табл. Оператора автоцистерни",
            "Відсутня табличка Оператора на контейнер-цистерні передбачена п.6.8.2.5.2 ДОПНВ": "Немає табл. Оператора контейнера",
            "Відсутня табличка Оператора на ТЗБ передбачена п.6.8.2.5.2 ДОПНВ": "Немає табл. Оператора ТЗБ",
            "Відсутня табличка Оператора на БЕГК передбачена п.6.8.2.5.2 ДОПНВ": "Немає табл. Оператора БЕГК",
            "Залишки НВ на КСМБ відкриті вентилі, не закрита наливна кришка": "Залишки на КСМ / відкриті вентилі",
            
            # Знаки небезпеки та Обладнання
            "Знаки небезпеки нанесені на упаковках не відповідають вантажу що перевозиться": "Знаки небезпеки не відпов. НВ",
            "Великі знаки небезпеки на автоцистерні не витримали погодніх умов (відклеїлися)": "Знаки небезпеки відклеїлись",
            "Невірне нанесення на ТОК ІНН та UN номеру": "Невірно нанесені ІНН та UN",
            "Порожня неочищена автоцистерна: зняв ТОК, без очистки": "Порожня неочищена цистерна без ТОК",
            "Цифри на ТОК не відповідають вимогам ДОПНВ, ржаві не чорного кольору": "Нечитабельні цифри на ТОК",
            "Відсутні знаки аварійної зупинки (мигаючи ліхтарі жовтого кольору чи конуси)": "Відсутні знаки аварійної зупинки",
            "Відсутні захисні рукавички та засіб захисту очей": "Немає рукавичок/захисту очей",
            "Відсутня рідина для промивання очей (очіпромивочна рідина)": "Немає рідини для промивання очей",
            "Відсутня лопата та дренажна пастка (покриття для каналізаційних колекторів)": "Немає лопати / дренажної пастки"
        }

        for original, short in exact_replacements.items():
            if cleaned_title.lower() == original.lower() or cleaned_title.lower().startswith(original.lower()[:30]):
                cleaned_title = short
                break
        adr_glossary = {
            "транспортного засобу": "ТЗ",
            "транспортних засобів": "ТЗ",
            "транспортний засіб": "ТЗ",
            "транспортної одиниці": "ТО",
            "транспортна одиниця": "ТО",
            "транспортній одиниці": "ТО",
            "транспортний документ": "ТД",
            "небезпечного вантажу": "НВ",
            "небезпечних вантажів": "НВ",
            "небезпечний вантаж": "НВ",
            "державного номерного знака": "ДНЗ",
            "державний номерний знак": "ДНЗ",
            "індивідуального захисту": "ІЗ",
            "письмова інструкція": "Інструкція",
            "письмової інструкції": "Інструкції",
            "відсутній": "немає",
            "відсутність": "немає",
            "автоцистерні": "цистерні",
            "автоцистерна": "цистерна",
            "таблички оранжевого кольору": "ТОК"
        }
        for long_word, short_word in adr_glossary.items():
            cleaned_title = cleaned_title.replace(long_word, short_word)
            cleaned_title = cleaned_title.replace(long_word.capitalize(), short_word)

        if cleaned_title:
            cleaned_title = cleaned_title[0].upper() + cleaned_title[1:]
        else:
            cleaned_title = title

        cleaned_title = cleaned_title.rstrip(",.- ")
        max_length = 34
        if len(cleaned_title) > max_length:
            button_text = f"⚖️ {cleaned_title[:max_length-3].strip()}..."
        else:
            button_text = f"⚖️ {cleaned_title}"
            
        builder.row(InlineKeyboardButton(
            text=button_text, 
            callback_data=f"adrfab_{fabula_id}"
        ))
        
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"adr_fpage:{category_idx}:{page-1}"))
    if end_idx < len(fabulas):
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"adr_fpage:{category_idx}:{page+1}"))
        
    if nav_buttons:
        builder.row(*nav_buttons)
    builder.row(InlineKeyboardButton(text="🔙 До категорій", callback_data="adr_page:1"))
    
    return builder.as_markup()