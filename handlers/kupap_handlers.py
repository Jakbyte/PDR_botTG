import re
from html import escape

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from database.db_manager_kupap import get_kupap_article, get_adjacent_kupap_number
from handlers.common import SearchStates
from keyboard.user_kb import kupap_search_back_menu, codes_menu

router = Router()


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
        extra_text = "\n\n➖➖➖➖➖➖➖➖➖➖\n\n".join(extra_blocks)
        body = (
            f"{body}\n\n➖➖➖➖➖➖➖➖➖➖\n\n{extra_text}"
            if body
            else extra_text
        )

    return (
        f"📖 <b>СТАТТЯ {article['number']}</b>\n"
        f"<i>{title}</i>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{body}"
    )


def build_kupap_nav_keyboard(number: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="◀️ Попередня",
            callback_data=f"kupap_nav:prev:{number}",
        ),
        InlineKeyboardButton(
            text="Наступна ▶️",
            callback_data=f"kupap_nav:next:{number}",
        ),
    ]])


async def send_article(
    message: Message, article: dict, keyboard: InlineKeyboardMarkup
):
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
            part = (
                f"<i>(продовження статті {article['number']}, "
                f"частина {i + 1}/{total})</i>\n\n{part}"
            )
        await message.answer(
            part,
            parse_mode="HTML",
            reply_markup=keyboard if is_last else None,
        )


@router.message(F.text == "📘 КУпАП")
async def kupap_menu(message: Message, state: FSMContext):
    await state.set_state(SearchStates.searching_kupap_number)
    await message.answer(
        '📘 <b>КУпАП — Кодекс України про адміністративні правопорушення</b>\n\n'
        'Надішліть номер статті, наприклад: <code>185</code> або <code>185-1</code>',
        reply_markup=kupap_search_back_menu,
        parse_mode="HTML"
    )


@router.message(
    SearchStates.searching_kupap_number,
    F.text.contains("Назад до Меню"),
)
async def back_from_kupap(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📚 Кодекси та закони:", reply_markup=codes_menu)


@router.message(SearchStates.searching_kupap_number, F.text)
async def handle_kupap_number(message: Message):
    number = message.text.strip()
    article = get_kupap_article(number)

    if not article:
        await message.answer(
            f"❌ Статтю <code>{escape(number)}</code> не знайдено.",
            parse_mode="HTML"
        )
        return

    keyboard = build_kupap_nav_keyboard(number)
    await send_article(message, article, keyboard)


@router.callback_query(F.data.startswith("kupap_nav:"))
async def handle_kupap_navigation(callback: CallbackQuery):
    _, direction, current_number = callback.data.split(":")
    new_number = get_adjacent_kupap_number(current_number, direction)

    if not new_number:
        await callback.answer(
            "Це крайня стаття в списку", show_alert=True
        )
        return

    article = get_kupap_article(new_number)
    keyboard = build_kupap_nav_keyboard(new_number)
    text = format_article(article)

    if len(text) <= 4096:
        await callback.message.edit_text(
            text, parse_mode="HTML", reply_markup=keyboard
        )
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await send_article(callback.message, article, keyboard)

    await callback.answer()
