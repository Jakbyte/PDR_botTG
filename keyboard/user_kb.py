from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Клавиатура главного меню
main_menu = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='ПДР України'),
            KeyboardButton(text="ℹ Про бота")
        ]
    ],
    resize_keyboard = True
)

pdr_options_menu = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text = "🔢 Пошук за номером пункту")],
        [KeyboardButton( text = "📚 Розділи ПДР")],
        [KeyboardButton(text = "⬅ Назад")]
    ],
    resize_keyboard = True
)


pdr_search_back_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='⬅ Назад до меню ПДР')]
    ],
    resize_keyboard = True
)

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

def get_sections_keyboard(page: int = 1):
    per_page = 7
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_sections = SECTIONS[start_idx:end_idx]
    buttons = []
    for idx, section in enumerate(page_sections):
        # Реальний номер розділу в загальному списку
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