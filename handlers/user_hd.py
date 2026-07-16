from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db_manager import get_rule_by_id, get_points_by_section
from database.db_manager_dtp import get_accidents_by_violation, get_accident_by_id, get_accidents_by_rule
from db_users.requests import add_user

from database.db_manager_neb import get_adr_categories, get_adr_fabulas_by_category, get_adr_fabula_text

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
    get_adr_sections_keyboard
)

router = Router()  

class SearchStates(StatesGroup):
    searching_fabula = State()


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


@router.message(F.text == "📘 ПДР України")
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
        "Цей бот створений для водіїв, кандидатів у водії та всіх, кому потрібно "
        "миттєво перевірити правила дорожнього руху прямо в дорозі або під час навчання. 🚘\n\n"
        "📌 <b>Головні переваги:</b>\n"
        "• <b>Миттєвий пошук:</b> Просто введіть номер пункту (наприклад, <code>9.2</code> або <code>15.9</code>), і бот одразу видасть текст правила.\n"
        "• <b>Актуальність:</b> База даних містить офіційну та найсвіжішу редакцію ПДР України.\n"
        "• <b>Зручність:</b> Більше не потрібно гортати довгі сторінки чи шукати в Google — усе доступно в один клік.\n\n"
        "💡 <b>Корисна порада:</b>\n"
        "Щоб розпочати новий пошук, вам не потрібно натискати жодних кнопок — просто введіть новий номер пункту в полі вводу у будь-який момент!\n\n"
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


# ==========================================
# --- НЕБЕЗПЕЧНІ ВАНТАЖІ (ADR) ---
# ==========================================

# 1. Відкриття головного меню категорій ADR (ТЕПЕР ЦЕ ТЕКСТОВА КНОПКА)
@router.message(F.text == "☣️ Небезпечні вантажі")
async def show_adr_categories_message(message: Message):
    await message.answer(
        "☣️ <b>Оберіть категорію порушення:</b>", 
        reply_markup=get_adr_sections_keyboard(page=1), 
        parse_mode="HTML"
    )


# 2. Пагінація головних категорій ADR
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
async def handle_section_click(callback: CallbackQuery):
    section_num = callback.data.split(":")[1]
    points = get_points_by_section(section_num)
    
    if not points:
        await callback.message.answer(f"ℹ️ У базі даних поки немає окремих пунктів для Розділу {section_num}.")
        await callback.answer()
        return

    buttons = []
    for pt in points:
        button_text = f"📍 {pt['id']} — {pt['title']}"
        cb_data = f"view_point:{pt['id']}"
        
        if len(cb_data.encode('utf-8')) > 64:
            continue
            
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=cb_data)])
        
    buttons.append([InlineKeyboardButton(text="⬅️ Назад до Розділів ПДР", callback_data="page:1")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        f"📚 <b>Розділ {section_num}</b>\n\nОберіть пункт правил, щоб прочитати його повністю:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
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