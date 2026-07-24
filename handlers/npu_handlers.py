import re
from html import escape

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from database.db_manager_npu import get_npu_article, get_adjacent_npu_number
from handlers.common import SearchStates
from keyboard.user_kb import npu_search_back_menu, codes_menu

router = Router()


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
            current_group = [
                f"<b>▸ Частина {num}</b>\n📝 {escape(text)}"
            ]
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
    body = (
        "\n\n➖➖➖➖➖➖➖➖➖➖\n\n".join(blocks)
        if len(blocks) > 1
        else (blocks[0] if blocks else "")
    )

    return (
        f"👮 <b>СТАТТЯ {article['number']}</b>\n"
        f"<i>{title}</i>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{body}"
    )


def build_npu_nav_keyboard(number: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="◀️ Попередня",
            callback_data=f"npu_nav:prev:{number}",
        ),
        InlineKeyboardButton(
            text="Наступна ▶️",
            callback_data=f"npu_nav:next:{number}",
        ),
    ]])


async def send_npu_article(
    message: Message, article: dict, keyboard: InlineKeyboardMarkup
):
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
            part = (
                f"<i>(продовження статті {article['number']}, "
                f"частина {i + 1}/{total})</i>\n\n{part}"
            )
        await message.answer(
            part,
            parse_mode="HTML",
            reply_markup=keyboard if is_last else None,
        )


@router.message(F.text == "👮 ЗУ 'Про Національну поліцію'")
async def npu_menu(message: Message, state: FSMContext):
    await state.set_state(SearchStates.searching_npu_number)
    await message.answer(
        '👮 <b>Закон України «Про Національну поліцію»</b>\n\n'
        'Надішліть номер статті, наприклад: <code>1</code> або <code>23</code>',
        reply_markup=npu_search_back_menu,
        parse_mode="HTML"
    )


@router.message(
    SearchStates.searching_npu_number,
    F.text.contains("Назад до Меню"),
)
async def back_from_npu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📚 Кодекси та закони:", reply_markup=codes_menu)


@router.message(SearchStates.searching_npu_number, F.text)
async def handle_npu_number(message: Message):
    number = message.text.strip()
    article = get_npu_article(number)

    if not article:
        await message.answer(
            f"❌ Статтю <code>{escape(number)}</code> не знайдено.",
            parse_mode="HTML"
        )
        return

    keyboard = build_npu_nav_keyboard(number)
    await send_npu_article(message, article, keyboard)


@router.callback_query(F.data.startswith("npu_nav:"))
async def handle_npu_navigation(callback: CallbackQuery):
    _, direction, current_number = callback.data.split(":")
    new_number = get_adjacent_npu_number(current_number, direction)

    if not new_number:
        await callback.answer(
            "Це крайня стаття в списку", show_alert=True
        )
        return

    article = get_npu_article(new_number)
    keyboard = build_npu_nav_keyboard(new_number)
    text = format_npu_article(article)

    if len(text) <= 4096:
        await callback.message.edit_text(
            text, parse_mode="HTML", reply_markup=keyboard
        )
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await send_npu_article(callback.message, article, keyboard)

    await callback.answer()
