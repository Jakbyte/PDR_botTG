from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import get_rule_by_id, get_points_by_section
from keyboard.user_kb import main_menu, pdr_options_menu, pdr_search_back_menu, get_sections_keyboard

router = Router()  

# --- ХЕНДЛЕР ДЛЯ ВІДКРИТТЯ ПУНКТУ
@router.callback_query(F.data.startswith("view_point:"))
async def handle_view_point(callback: CallbackQuery):
    point_id = callback.data.split(":")[1]
    rule_text = get_rule_by_id(point_id)
    
    if rule_text:
        full_message = f"📌 <b>Пункт {point_id}:</b>\n\n{rule_text}"
        # Використовуємо callback.message для надсилання відповіді
        await send_long_message(callback.message, full_message, parse_mode="HTML")
    else:
        await callback.message.answer(f"❌ Текст для пункту {point_id} не знайдено.")
        
    await callback.answer()

# --- СТАРТ ТА ГОЛОВНЕ МЕНЮ ---
@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Головне меню:", reply_markup=main_menu)

@router.message(F.text == "ПДР України")
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

# --- КНОПКИ НАЗАД ---
@router.message(F.text == "⬅ Назад до меню ПДР")
async def back_to_pdr(message: Message):
    await pdr_ukrainy(message)

@router.message(F.text == "⬅ Назад")
async def back_to_main(message: Message):
    await message.answer("Головне меню:", reply_markup=main_menu)

# --- ШВИДКИЙ ПОШУК ---
@router.message(F.text.regexp(r"^\d+\.\d+(\.\d+)?$"))
async def handle_rule(message: Message):
    rule = message.text.strip()
    rule_text = get_rule_by_id(rule)
    if rule_text:
        full_message = f"📌 <b>Пункт {rule}:</b>\n{rule_text}"
        await send_long_message(message, full_message, parse_mode="HTML")
    else:
        await message.answer(f"❌ Пункт <code>{rule}</code> не знайдено", parse_mode="HTML")

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