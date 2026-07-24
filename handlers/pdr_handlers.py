from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.db_manager import get_rule_by_id, get_points_by_section
from handlers.common import send_long_message
from keyboard.user_kb import (
    pdr_options_menu,
    get_sections_keyboard,
    codes_menu,
)

router = Router()


@router.message(F.text == "📖 ПДР України")
async def pdr_ukrainy(message: Message):
    await message.answer(
        'Виберіть варіант навігації:\n\n'
        '🔢 <b>Пошук за номером:</b> інструкція, як викликати конкретний пункт.\n'
        '📚 <b>Розділи ПДР:</b> відкрити інтерактивний зміст правил.',
        reply_markup=pdr_options_menu,
        parse_mode="HTML"
    )


@router.message(F.text == "🔢 Пошук за номером пункту")
async def pdr_search_mode(message: Message):
    await message.answer(
        '📥 <b>Введення номера пункту правила</b>\n\n'
        'Просто надішліть мені номер пункту цифрами.\n'
        'Наприклад: <code>8.4</code>, <code>15.9</code> або <code>32.2</code>',
        reply_markup=pdr_options_menu,
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


@router.callback_query(F.data.startswith("section:"))
async def handle_section_click(callback: CallbackQuery, page: int = 1):
    section_num = callback.data.split(":")[1]
    points = get_points_by_section(section_num)

    if not points:
        await callback.message.answer(
            f"ℹ️ У базі даних поки немає окремих пунктів для Розділу {section_num}."
        )
        await callback.answer()
        return

    await render_section_points(callback, section_num, points, page=1)
    await callback.answer()


async def render_section_points(
    callback: CallbackQuery, section_num: str, points: list, page: int
):
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
        nav_row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"section_page:{section_num}:{page-1}",
            )
        )
    if total_pages > 1:
        nav_row.append(
            InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop")
        )
    if page < total_pages:
        nav_row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"section_page:{section_num}:{page+1}",
            )
        )
    if nav_row:
        buttons.append(nav_row)

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад до Розділів ПДР", callback_data="page:1"
            )
        ]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        f"📚 <b>Розділ {section_num}</b>\n\n"
        "Оберіть пункт правил, щоб прочитати його повністю:",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("section_page:"))
async def handle_section_page_switch(callback: CallbackQuery):
    _, section_num, page_str = callback.data.split(":")
    page = int(page_str)
    points = get_points_by_section(section_num)
    await render_section_points(callback, section_num, points, page=page)
    await callback.answer()


@router.callback_query(F.data.startswith("view_point:"))
async def handle_view_point(callback: CallbackQuery):
    point_id = callback.data.split(":")[1]
    rule_text = get_rule_by_id(point_id)

    if rule_text:
        full_message = f"📌 <b>Пункт {point_id}:</b>\n\n{rule_text}"
        await send_long_message(callback.message, full_message, parse_mode="HTML")
    else:
        await callback.message.answer(
            f"❌ Текст для пункту {point_id} не знайдено."
        )

    await callback.answer()


@router.message(F.text == "📚 Кодекси та закони")
async def codes_menu_handler(message: Message):
    await message.answer(
        "📚 <b>Кодекси та закони</b>\n\nОберіть потрібний документ:",
        reply_markup=codes_menu,
        parse_mode="HTML"
    )


@router.message(F.text.regexp(r"^\d+\.\d+(\.\d+)?$"))
async def handle_rule(message: Message):
    rule = message.text.strip()
    rule_text = get_rule_by_id(rule)

    if rule_text:
        full_message = f"📌 <b>Пункт {rule}:</b>\n{rule_text}"
        await send_long_message(message, full_message, parse_mode="HTML")
    else:
        await message.answer(
            f"❌ Пункт ПДР <code>{rule}</code> не знайдено.", parse_mode="HTML"
        )
