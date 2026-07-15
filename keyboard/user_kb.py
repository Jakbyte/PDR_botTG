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

SECTIONS_ADR = [
    "Перевізні документи",
    "Письмова інструкція",
    "Національний дозвіл (маршрут руху)",
    "Копія договору обов’язкового страхування відповідальності суб’єктів перевезення небезпечних вантажів на випадок настання негативних наслідків под час перевезення небезпечних вантажів",
    "Свідоцтво про допущення транспортних засобів до перевезення визначених небезпечних вантажів",
    "Свідоцтво ДОПНВ про підготовку водія",
    "Вантаж допущено до перевезення вантажу",
    "Транспортні засоби є придатними до перевезення небезпечних вантажів",
    "Положення з перевезення (навалом, в упаковках, у цистернах)",
    "Навантаження, розміщення і кріплення вантажу",
    "Маркування та знаки небезпеки",
    "Додаткове обладнання та засоби індивідуального захисту"
]

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

    for section in SECTIONS_ADR[start_idx:end_idx]:
        idx = SECTIONS_ADR.index(section)

        display_name = section if len(section) <= 35 else section[:32] + "..."
        buttons.append([InlineKeyboardButton(text=f"{display_name}", callback_data=f"adr_sect:{idx}")])

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


        replacements = [
            "Невірно заповнена ТТН:",
            "Невірно заповнена ТТН",
            "Невірно заповнений",
            "Невірно заповнені",
            "Порушення правил"
        ]
        
        if category_name:
            replacements.insert(0, f"{category_name}:")
            replacements.insert(1, category_name)

        for r in replacements:
            if cleaned_title.startswith(r):
                cleaned_title = cleaned_title.replace(r, "", 1).strip()
        
        cleaned_title = cleaned_title.lstrip(":- ").strip()
        if cleaned_title:
            cleaned_title = cleaned_title[0].upper() + cleaned_title[1:]
        else:
            cleaned_title = title 
            
        max_length = 38
        if len(cleaned_title) > max_length:
            button_text = f"{cleaned_title[:max_length-3].strip()}..."
        else:
            button_text = f"{cleaned_title}"
            
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