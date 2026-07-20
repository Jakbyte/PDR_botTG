import re
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from html import escape

from database.db_manager import get_rule_by_id, get_points_by_section
from database.db_manager_dtp import get_accidents_by_violation, get_accident_by_id, get_accidents_by_rule
from db_users.requests import add_user
from database.db_manager_neb import get_adr_categories, get_adr_fabulas_by_category, get_adr_fabula_text
from database.db_manager_kupap import get_kupap_article, get_adjacent_kupap_number
from database.db_manager_npu import get_npu_article, get_adjacent_npu_number

from keyboard.user_kb import (
    main_menu, 
    pdr_options_menu, 
    pdr_search_back_menu, 
    fabula_type_menu, 
    SECTIONS_DTP,
    SECTIONS_ADR,               
    get_dtp_sections_keyboard,
    get_sections_keyboard,
    pdr_fabula_submenu,
    get_adr_fabulas_keyboard,
    get_adr_sections_keyboard,
    kupap_search_back_menu,
    npu_search_back_menu,
    codes_menu
)

router = Router()  

class SearchStates(StatesGroup):
    searching_fabula = State()
    searching_kupap_number = State()
    searching_npu_number = State()


# --- ХЕНДЛЕР ДЛЯ ВІДКРИТТЯ ПУНКТУ ---
@router.callback_query(F.data.startswith("view_point:"))
async def handle_view_point(callback: CallbackQuery):
    point_id = callback.data.split(":")[1]
    rule_text = get_rule_by_id(point_id)
    
    if rule_text:
        full_message = f"📌 <b>Пункт {point_id}:</b>\n\n{rule_text}"
        await send_long_message(callback.message, full_message, parse_mode="HTML")
    else:
        await callback.message.answer(f"❌ Текст для пункту {point_id} не знайдено.")
        
    await callback.answer()


# --- СТАРТ ТА ГОЛОВНЕ МЕНЮ ---
@router.message(F.text == "/start")
async def start(message: Message):
    add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    await message.answer(
        f"👋 Привіт, {message.from_user.first_name}!\n"
        "Я допоможу тобі швидко знайти ПДР України. Оберіть дію в меню нижче:", 
        reply_markup=main_menu
    )


@router.message(F.text == "📖 ПДР України")
async def pdr_ukrainy(message: Message):
    await message.answer(
        'Виберіть варіант навігації:\n\n'
        '🔢 <b>Пошук за номером:</b> інструкція, як викликати конкретний пункт.\n'
        '📚 <b>Розділи ПДР:</b> відкрити інтерактивний зміст правил.',
        reply_markup=pdr_options_menu,
        parse_mode="HTML"
    )

@router.message(F.text == "ℹ Про бота")
async def about(message: Message):
    text = (
        "ℹ️ <b>Про бота «ПДР України | Швидкий пошук»</b>\n\n"
        "Довідковий інструмент для поліцейських — швидкий доступ до нормативної "
        "бази.\n\n"
        "<b>📌 Розділи:</b>\n"
        "📘 <b>ПДР</b> — пошук пункту за номером (наприклад, <code>9.2</code>) або за розділами.\n"
        "📋 <b>КУпАП</b> — пошук статті за номером, санкція виділена окремо для швидкої перевірки.\n"
        "👮 <b>Закон України «Про Національну поліцію»</b> — за номером статті.\n"
        "⚖️ <b>Фабули</b> — приклади кваліфікації правопорушень по ДТП та небезпечних вантажах.\n\n"
        "💡 Гортайте статті кнопками «◀️ Попередня / Наступна ▶️» — не потрібно щоразу "
        "вводити номер заново.\n\n"
        "🔄 База регулярно оновлюється відповідно до змін у законодавстві.\n\n"
        "───────────────────\n"
        "👨‍💻 <b>Підтримка та пропозиції:</b>\n"
        "Якщо ви знайшли помилку або маєте ідею щодо покращення бота, пишіть розробнику: @jakbyte"
    )
    await message.answer(text, parse_mode="HTML")


# ==========================================
# --- ГІЛКА: ФАБУЛИ ---
# ==========================================

# 1. Головна кнопка "Фабули" з main_menu
@router.message(F.text == "⚖️ Фабули")
async def process_fabula_main_click(message: Message):
    await message.answer(
        "📂 Оберіть тип фабул, який вас цікавить:",
        reply_markup=fabula_type_menu
    )


# 2. Кнопка "Фабули ДТП" (ВМИКАЄ СТАН)
@router.message(F.text == "🚗 Фабули ДТП")
async def process_fabula_dtp_click(message: Message, state: FSMContext):
    await state.set_state(SearchStates.searching_fabula) 
    await message.answer(
        "🚗 Оберіть категорію порушення ПДР за допомогою кнопок нижче\n"
        "або <b>просто напишіть номер пункту</b> (наприклад, <code>12.3</code>), щоб отримати фабули за ним!",
        reply_markup=get_dtp_sections_keyboard(page=1),
        parse_mode="HTML"
    )


# 3. Обробка перемикання сторінок категорій ДТП
@router.callback_query(F.data.startswith("dtp_page:"))
async def handle_dtp_page_switch(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(reply_markup=get_dtp_sections_keyboard(page=page))
    await callback.answer()


# 4. Користувач натиснув на конкретну категорію ДТП
@router.callback_query(F.data.startswith("dtp_sect:"))
async def handle_dtp_section_click(callback: CallbackQuery):
    section_idx = int(callback.data.split(":")[1])
    db_violation_name = SECTIONS_DTP[section_idx]
    
    accidents = get_accidents_by_violation(db_violation_name)
    
    if not accidents:
        await callback.message.answer(f"❌ За категорією «{db_violation_name}» фабул не знайдено.")
        await callback.answer()
        return

    inline_kb = []
    for acc in accidents:
        btn_text = f"п. {acc['pdr_rule']} | {acc['title']}"
        if len(btn_text) > 40:
            btn_text = btn_text[:37] + "..."
            
        inline_kb.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"fabula_{acc['id']}")
        ])
        
    inline_kb.append([
        InlineKeyboardButton(text="⬅️ Назад до категорій", callback_data="dtp_page:1")
    ])
    
    markup = InlineKeyboardMarkup(inline_keyboard=inline_kb)
    await callback.message.edit_text(
        f"🔍 Знайдено випадків у категорії «{db_violation_name}»:",
        reply_markup=markup
    )
    await callback.answer()


# 5. Обробка натискання на конкретну судову фабулу ДТП
@router.callback_query(F.data.startswith("fabula_"))
async def show_full_fabula_dtp(callback: CallbackQuery):
    accident_id = int(callback.data.split("_")[1])
    accident = get_accident_by_id(accident_id)
    
    if accident:
        response_text = (
            f"📌 <b>Пункт ПДР:</b> {accident['pdr_rule']}\n"
            f"⚠️ <b>Порушення:</b> {accident['violation_title']}\n\n"
            f"📝 <b>Опис пригоди (Фабула):</b>\n<i>{accident['fabula']}</i>"
        )
        await send_long_message(callback.message, response_text, parse_mode="HTML")
    else:
        await callback.message.answer("❌ Помилка: Фабулу не знайдено.")
        
    await callback.answer()


# 6. Меню Фабули ПДР
@router.message(F.text == "🚦 Фабули ПДР")
async def process_fabula_pdr(message: Message):
    await message.answer(
        "🚦 <b>Фабули ПДР</b>\n\nОберіть потрібний підрозділ на клавіатурі нижче:",
        reply_markup=pdr_fabula_submenu,
        parse_mode="HTML"
    )


# 7. Обробка кнопки "🚦 Інші порушення ПДР" (ТЕПЕР ЦЕ ТЕКСТОВА КНОПКА)
@router.message(F.text == "🚦 Інші порушення ПДР")
async def show_other_pdr_fabulas(message: Message):
    await message.answer("📚 Розділ 'Інші фабули ПДР' знаходиться у розробці...")


# 6. Меню Фабули ГБ
@router.message(F.text == "🛡️ Фабули ГБ")
async def process_fabula_pdr(message: Message):
    await message.answer("🛡️ Розділ '🛡️ Фабули ГБ' знаходиться у розробці...")

# ==========================================
# --- НЕБЕЗПЕЧНІ ВАНТАЖІ  ---
# ==========================================

# 1. Відкриття головного меню категорій Небезпечні вантажі
@router.message(F.text == "☣️ Небезпечні вантажі")
async def show_adr_categories_message(message: Message):
    await message.answer(
        "☣️ <b>Оберіть категорію порушення:</b>", 
        reply_markup=get_adr_sections_keyboard(page=1), 
        parse_mode="HTML"
    )


# 2. Пагінація головних категорій Небезпечні вантажі
@router.callback_query(F.data.startswith("adr_page:"))
async def handle_adr_page_switch(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(reply_markup=get_adr_sections_keyboard(page=page))
    await callback.answer()


# 3. Натискання на конкретну категорію (завантаження списку фабул)
@router.callback_query(F.data.startswith("adr_sect:"))
async def handle_adr_section_click(callback: CallbackQuery):
    section_idx = int(callback.data.split(":")[1])
    db_category_name = SECTIONS_ADR[section_idx]
    
    fabulas = get_adr_fabulas_by_category(db_category_name)
    
    if not fabulas:
        await callback.message.answer(f"❌ За категорією «{db_category_name}» фабул не знайдено.")
        await callback.answer()
        return
        
    markup = get_adr_fabulas_keyboard(fabulas, category_idx=section_idx, page=1)
    
    await callback.message.edit_text(
        f"🔍 <b>Категорія:</b> {db_category_name}\nОберіть порушення:",
        reply_markup=markup,
        parse_mode="HTML"
    )
    await callback.answer()


# 4. Пагінація самих фабул всередині обраної категорії
@router.callback_query(F.data.startswith("adr_fpage:"))
async def handle_adr_fabulas_page_switch(callback: CallbackQuery):
    _, cat_idx_str, page_str = callback.data.split(":")
    cat_idx = int(cat_idx_str)
    page = int(page_str)
    
    db_category_name = SECTIONS_ADR[cat_idx]
    fabulas = get_adr_fabulas_by_category(db_category_name)
    
    markup = get_adr_fabulas_keyboard(fabulas, category_idx=cat_idx, page=page)
    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


# 5. Вивід повного тексту конкретної фабули
@router.callback_query(F.data.startswith("adrfab_"))
async def show_full_fabula_adr(callback: CallbackQuery):
    fabula_id = int(callback.data.split("_")[1])
    fabula_data = get_adr_fabula_text(fabula_id) 
    
    if fabula_data:
        title = fabula_data[0] if isinstance(fabula_data, tuple) else fabula_data['title']
        text = fabula_data[1] if isinstance(fabula_data, tuple) else fabula_data['fabula_text']
        
        response_text = f"📌 <b>{title}</b>\n\n📝 <b>Фабула:</b>\n<i>{text}</i>"
        
        back_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 До списку категорій", callback_data="adr_page:1")]
        ])
        
        await send_long_message(callback.message, response_text, parse_mode="HTML")
        await callback.message.answer("Оберіть дію:", reply_markup=back_kb)
    else:
        await callback.message.answer("❌ Помилка: Фабулу не знайдено.")
        
    await callback.answer()


# ==========================================
# --- РОЗДІЛИ ПДР (АКТИВНІ КНОПКИ) ---
# ==========================================
@router.message(F.text == "🔢 Пошук за номером пункту")
async def pdr_search_mode(message: Message):
    await message.answer(
        '📥 <b>Введення номера пункту правила</b>\n\n'
        'Просто надішліть мені номер пункту цифрами.\n'
        'Наприклад: <code>8.4</code>, <code>15.9</code> або <code>32.2</code>',
        reply_markup=pdr_search_back_menu,
        parse_mode="HTML"
    )


@router.message(F.text == "📚 Розділи ПДР")
async def pdr_sections_mode(message: Message):
    await message.answer(
        '📚 <b>Зміст ПДР України:</b>\nОберіть потрібний розділ:',
        reply_markup=get_sections_keyboard(page=1),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("page:"))
async def handle_page_switch(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(reply_markup=get_sections_keyboard(page=page))
    await callback.answer()


@router.callback_query(F.data == "noop")
async def handle_noop(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data.startswith("section:"))
async def handle_section_click(callback: CallbackQuery, page: int = 1):
    section_num = callback.data.split(":")[1]
    points = get_points_by_section(section_num)

    if not points:
        await callback.message.answer(f"ℹ️ У базі даних поки немає окремих пунктів для Розділу {section_num}.")
        await callback.answer()
        return

    await render_section_points(callback, section_num, points, page=1)
    await callback.answer()


async def render_section_points(callback: CallbackQuery, section_num: str, points: list, page: int):
    PER_PAGE = 8
    total_pages = (len(points) + PER_PAGE - 1) // PER_PAGE
    start_idx = (page - 1) * PER_PAGE
    end_idx = start_idx + PER_PAGE
    page_points = points[start_idx:end_idx]

    buttons = []
    for pt in page_points:
        button_text = f"📍 {pt['id']} — {pt['title']}"
        cb_data = f"view_point:{pt['id']}"
        if len(cb_data.encode('utf-8')) > 64:
            continue
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=cb_data)])

    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"section_page:{section_num}:{page-1}"))
    if total_pages > 1:
        nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"section_page:{section_num}:{page+1}"))
    if nav_row:
        buttons.append(nav_row)

    buttons.append([InlineKeyboardButton(text="⬅️ Назад до Розділів ПДР", callback_data="page:1")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        f"📚 <b>Розділ {section_num}</b>\n\nОберіть пункт правил, щоб прочитати його повністю:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("section_page:"))
async def handle_section_page_switch(callback: CallbackQuery):
    _, section_num, page_str = callback.data.split(":")
    page = int(page_str)
    points = get_points_by_section(section_num)
    await render_section_points(callback, section_num, points, page=page)
    await callback.answer()

# ==========================================
# --- КОДЕКСИ ТА ЗАКОНИ (розділ-контейнер) ---
# ==========================================
@router.message(F.text == "📚 Кодекси та закони")
async def codes_menu_handler(message: Message):
    await message.answer(
        "📚 <b>Кодекси та закони</b>\n\nОберіть потрібний документ:",
        reply_markup=codes_menu,
        parse_mode="HTML"
    )
    
# ==========================================
# --- КУпАП ---
# ==========================================
def format_article(article: dict) -> str:
    title = escape(article["title"])
    raw_paragraphs = [
        escape(re.sub(r"\s+", " ", p.strip()))
        for p in article["body"].split("\n\n") if p.strip()
    ]

    parts = []
    current_part = []
    notes = []      
    definitions = []  

    for p in raw_paragraphs:
        p_lower = p.lower()

        if p_lower.startswith("примітка"):
            notes.append(p)
            continue

        if p_lower.startswith("під ") and "слід розуміти" in p_lower:
            definitions.append(p)
            continue

        current_part.append(p)
        if p_lower.startswith(("тягне за собою", "тягнуть за собою")):
            parts.append(current_part)
            current_part = []

    if current_part:
        definitions.extend(current_part)

    blocks = []
    for i, part in enumerate(parts, start=1):
        lines = []
        for p in part:
            if p.lower().startswith(("тягне за собою", "тягнуть за собою")):
                lines.append(f"<blockquote>⚖️ {p}</blockquote>")
            else:
                lines.append(f"📝 {p}")
        block_text = "\n\n".join(lines)
        if len(parts) > 1:
            block_text = f"<b>▸ Частина {i}</b>\n\n{block_text}"
        blocks.append(block_text)

    body = "\n\n➖➖➖➖➖➖➖➖➖➖\n\n".join(blocks)

    extra_blocks = []
    if definitions:
        defs_text = "\n\n".join(f"📌 <i>{d}</i>" for d in definitions)
        extra_blocks.append(defs_text)
    if notes:
        notes_text = "\n\n".join(f"ℹ️ <i>{n}</i>" for n in notes)
        extra_blocks.append(notes_text)

    if extra_blocks:
        body += "\n\n➖➖➖➖➖➖➖➖➖➖\n\n" + "\n\n➖➖➖➖➖➖➖➖➖➖\n\n".join(extra_blocks)

    return (
        f"📖 <b>СТАТТЯ {article['number']}</b>\n"
        f"<i>{title}</i>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{body}"
    )

def build_kupap_nav_keyboard(number: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="◀️ Попередня", callback_data=f"kupap_nav:prev:{number}"),
        InlineKeyboardButton(text="Наступна ▶️", callback_data=f"kupap_nav:next:{number}")
    ]])


async def send_article(message: Message, article: dict, keyboard: InlineKeyboardMarkup):
    text = format_article(article)
    LIMIT = 4096

    if len(text) <= LIMIT:
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
        return

    parts = []
    current = ""
    for paragraph in text.split("\n\n"):
        if len(current) + len(paragraph) + 2 > LIMIT:
            parts.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        parts.append(current)

    total = len(parts)
    for i, part in enumerate(parts):
        is_last = (i == total - 1)
        if i > 0:
            part = f"<i>(продовження статті {article['number']}, частина {i + 1}/{total})</i>\n\n{part}"
        await message.answer(part, parse_mode="HTML", reply_markup=keyboard if is_last else None)

@router.message(F.text == "📘 КУпАП")
async def kupap_menu(message: Message, state: FSMContext):
    await state.set_state(SearchStates.searching_kupap_number)
    await message.answer(
        '📘 <b>КУпАП — Кодекс України про адміністративні правопорушення</b>\n\n'
        'Надішліть номер статті, наприклад: <code>185</code> або <code>185-1</code>',
        reply_markup=kupap_search_back_menu,
        parse_mode="HTML"
    )


@router.message(SearchStates.searching_kupap_number, F.text.contains("Назад до Меню"))
async def back_from_kupap(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📚 Кодекси та закони:", reply_markup=codes_menu)


@router.message(SearchStates.searching_kupap_number, F.text)
async def handle_kupap_number(message: Message):
    number = message.text.strip()
    article = get_kupap_article(number)

    if not article:
        await message.answer(f"❌ Статтю <code>{escape(number)}</code> не знайдено.", parse_mode="HTML")
        return

    keyboard = build_kupap_nav_keyboard(number)
    await send_article(message, article, keyboard)


@router.callback_query(F.data.startswith("kupap_nav:"))
async def handle_kupap_navigation(callback: CallbackQuery):
    _, direction, current_number = callback.data.split(":")
    new_number = get_adjacent_kupap_number(current_number, direction)

    if not new_number:
        await callback.answer("Це крайня стаття в списку", show_alert=True)
        return

    article = get_kupap_article(new_number)
    keyboard = build_kupap_nav_keyboard(new_number)
    text = format_article(article)

    if len(text) <= 4096:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await send_article(callback.message, article, keyboard)

    await callback.answer()

# ==========================================
# --- ЗАКОН ПРО НАЦІОНАЛЬНУ ПОЛІЦІЮ ---
# ==========================================
def format_npu_article(article: dict) -> str:
    title = escape(article["title"])
    raw_paragraphs = [
        re.sub(r"\s+", " ", p.strip())
        for p in article["body"].split("\n\n") if p.strip()
    ]

    part_pattern = re.compile(r'^(\d+)\.\s+(.*)$', re.S)
    subitem_pattern = re.compile(r'^(\d+)\)\s+(.*)$', re.S)

    groups = []
    current_group = None

    for p in raw_paragraphs:
        part_match = part_pattern.match(p)
        subitem_match = subitem_pattern.match(p)

        if part_match:
            if current_group:
                groups.append(current_group)
            num, text = part_match.groups()
            current_group = [f"<b>▸ Частина {num}</b>\n📝 {escape(text)}"]
        elif subitem_match and current_group is not None:
            num, text = subitem_match.groups()
            current_group.append(f"　<b>{num})</b> {escape(text)}")
        else:
            line = f"📝 {escape(p)}"
            if current_group is not None:
                current_group.append(line)
            else:
                current_group = [line]

    if current_group:
        groups.append(current_group)

    blocks = ["\n\n".join(g) for g in groups]
    body = "\n\n➖➖➖➖➖➖➖➖➖➖\n\n".join(blocks) if len(blocks) > 1 else (blocks[0] if blocks else "")

    return (
        f"👮 <b>СТАТТЯ {article['number']}</b>\n"
        f"<i>{title}</i>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{body}"
    )


def build_npu_nav_keyboard(number: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="◀️ Попередня", callback_data=f"npu_nav:prev:{number}"),
        InlineKeyboardButton(text="Наступна ▶️", callback_data=f"npu_nav:next:{number}")
    ]])


async def send_npu_article(message: Message, article: dict, keyboard: InlineKeyboardMarkup):
    text = format_npu_article(article)
    LIMIT = 4096

    if len(text) <= LIMIT:
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
        return

    parts = []
    current = ""
    for paragraph in text.split("\n\n"):
        if len(current) + len(paragraph) + 2 > LIMIT:
            parts.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        parts.append(current)

    total = len(parts)
    for i, part in enumerate(parts):
        is_last = (i == total - 1)
        if i > 0:
            part = f"<i>(продовження статті {article['number']}, частина {i + 1}/{total})</i>\n\n{part}"
        await message.answer(part, parse_mode="HTML", reply_markup=keyboard if is_last else None)


@router.message(F.text == "👮 ЗУ 'Про Національну поліцію'")
async def npu_menu(message: Message, state: FSMContext):
    await state.set_state(SearchStates.searching_npu_number)
    await message.answer(
        '👮 <b>Закон України «Про Національну поліцію»</b>\n\n'
        'Надішліть номер статті, наприклад: <code>1</code> або <code>23</code>',
        reply_markup=npu_search_back_menu,
        parse_mode="HTML"
    )


@router.message(SearchStates.searching_npu_number, F.text.contains("Назад до Меню"))
async def back_from_npu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📚 Кодекси та закони:", reply_markup=codes_menu)


@router.message(SearchStates.searching_npu_number, F.text)
async def handle_npu_number(message: Message):
    number = message.text.strip()
    article = get_npu_article(number)

    if not article:
        await message.answer(f"❌ Статтю <code>{escape(number)}</code> не знайдено.", parse_mode="HTML")
        return

    keyboard = build_npu_nav_keyboard(number)
    await send_npu_article(message, article, keyboard)


@router.callback_query(F.data.startswith("npu_nav:"))
async def handle_npu_navigation(callback: CallbackQuery):
    _, direction, current_number = callback.data.split(":")
    new_number = get_adjacent_npu_number(current_number, direction)

    if not new_number:
        await callback.answer("Це крайня стаття в списку", show_alert=True)
        return

    article = get_npu_article(new_number)
    keyboard = build_npu_nav_keyboard(new_number)
    text = format_npu_article(article)

    if len(text) <= 4096:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await send_npu_article(callback.message, article, keyboard)

    await callback.answer()

# --- КНОПКИ НАЗАД (СИСТЕМА ПОВЕРНЕНЬ) ---
@router.message(F.text == "⬅ Назад до головного")
async def back_to_main_from_fabula(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Головне меню:", reply_markup=main_menu)


@router.message(F.text == "⬅ Назад до menu ПДР")
async def back_to_pdr(message: Message):
    await pdr_ukrainy(message)


@router.message(F.text == "⬅ Назад")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Головне меню:", reply_markup=main_menu)
    await message.answer("Головне меню:", reply_markup=main_menu)


# --- ПОШУК ФАБУЛ ДТП --- 
@router.message(SearchStates.searching_fabula, F.text.regexp(r"^\d+\.\d+(\.\d+)?$"))
async def handle_dtp_fabula_by_number(message: Message):
    rule = message.text.strip()
    accidents = get_accidents_by_rule(rule)
    
    if not accidents:
        await message.answer(
            f"❌ Фабул ДТП за пунктом <code>{rule}</code> не знайдено.", 
            parse_mode="HTML"
        )
        return

    inline_kb = []
    for acc in accidents[:10]: 
        btn_text = f"⚖️ {acc['title']}"
        if len(btn_text) > 40:
            btn_text = btn_text[:37] + "..."
        inline_kb.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"fabula_{acc['id']}")
        ])
        
    markup = InlineKeyboardMarkup(inline_keyboard=inline_kb)
    await message.answer(
        f"⚖️ <b>Знайдені фабули за п. {rule}:</b>\n"
        f"Оберіть випадок нижче, щоб відкрити його фабулу:",
        reply_markup=markup,
        parse_mode="HTML"
    )


# --- СТАНДАРТНИЙ ПОШУК ПДР ---
@router.message(F.text.regexp(r"^\d+\.\d+(\.\d+)?$"))
async def handle_rule(message: Message):
    rule = message.text.strip()
    rule_text = get_rule_by_id(rule)
    
    if rule_text:
        full_message = f"📌 <b>Пункт {rule}:</b>\n{rule_text}"
        await send_long_message(message, full_message, parse_mode="HTML")
    else:
        await message.answer(f"❌ Пункт ПДР <code>{rule}</code> не знайдено.", parse_mode="HTML")


# --- ФУНКЦІЯ ДЛЯ ДОВГИХ ПОВІДОМЛЕНЬ ---
async def send_long_message(message: Message, text: str, chunk_size: int = 4096, parse_mode: str = None):
    if len(text) <= chunk_size:
        await message.answer(text, parse_mode=parse_mode)
        return
    lines = text.split('\n')
    current_chunk = ""  
    for line in lines:
        if len(current_chunk) + len(line) + 1 > chunk_size:
            await message.answer(current_chunk, parse_mode=parse_mode)
            current_chunk = line
        else:
            current_chunk = current_chunk + "\n" + line if current_chunk else line               
    if current_chunk:
        await message.answer(current_chunk, parse_mode=parse_mode)