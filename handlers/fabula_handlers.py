from html import escape

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from database.db_manager_dtp import (
    get_accidents_by_violation,
    get_accident_by_id,
    get_accidents_by_rule,
)
from database.db_manager_neb import (
    get_adr_fabulas_by_category,
    get_adr_fabula_text,
)
from database.db_manager_mtz import get_all_mtz_fabulas, get_mtz_fabula_by_id
from handlers.common import SearchStates, send_long_message
from keyboard.user_kb import (
    fabula_type_menu,
    SECTIONS_DTP,
    SECTIONS_ADR,
    get_dtp_sections_keyboard,
    pdr_fabula_submenu,
    get_adr_fabulas_keyboard,
    get_adr_sections_keyboard,
    gb_fabula_submenu,
    get_mtz_flat_keyboard,
)

router = Router()


# ==========================================
# --- ГОЛОВНЕ МЕНЮ ФАБУЛ ---
# ==========================================
@router.message(F.text == "⚖️ Фабули")
async def process_fabula_main_click(message: Message):
    await message.answer(
        "📂 Оберіть тип фабул, який вас цікавить:",
        reply_markup=fabula_type_menu
    )


# ==========================================
# --- ФАБУЛИ ДТП ---
# ==========================================
@router.message(F.text == "🚗 Фабули ДТП")
async def process_fabula_dtp_click(message: Message, state: FSMContext):
    await state.set_state(SearchStates.searching_fabula)
    await message.answer(
        "🚗 Оберіть категорію порушення ПДР за допомогою кнопок нижче\n"
        "або <b>просто напишіть номер пункту</b> (наприклад, <code>12.3</code>), "
        "щоб отримати фабули за ним!",
        reply_markup=get_dtp_sections_keyboard(page=1),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("dtp_page:"))
async def handle_dtp_page_switch(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(
        reply_markup=get_dtp_sections_keyboard(page=page)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("dtp_sect:"))
async def handle_dtp_section_click(callback: CallbackQuery):
    section_idx = int(callback.data.split(":")[1])
    db_violation_name = SECTIONS_DTP[section_idx]

    accidents = get_accidents_by_violation(db_violation_name)

    if not accidents:
        await callback.message.answer(
            f"❌ За категорією «{db_violation_name}» фабул не знайдено."
        )
        await callback.answer()
        return

    inline_kb = []
    for acc in accidents:
        btn_text = f"п. {acc['pdr_rule']} | {acc['title']}"
        if len(btn_text) > 40:
            btn_text = btn_text[:37] + "..."
        inline_kb.append([
            InlineKeyboardButton(
                text=btn_text, callback_data=f"fabula_{acc['id']}"
            )
        ])

    inline_kb.append([
        InlineKeyboardButton(
            text="⬅️ Назад до категорій", callback_data="dtp_page:1"
        )
    ])

    markup = InlineKeyboardMarkup(inline_keyboard=inline_kb)
    await callback.message.edit_text(
        f"🔍 Знайдено випадків у категорії «{db_violation_name}»:",
        reply_markup=markup
    )
    await callback.answer()


@router.callback_query(F.data.startswith("fabula_"))
async def show_full_fabula_dtp(callback: CallbackQuery):
    accident_id = int(callback.data.split("_")[1])
    accident = get_accident_by_id(accident_id)

    if accident:
        response_text = (
            f"📌 <b>Пункт ПДР:</b> {accident['pdr_rule']}\n"
            f"⚠️ <b>Порушення:</b> {accident['violation_title']}\n\n"
            f"📝 <b>Опис пригоди (Фабула):</b>\n"
            f"<i>{accident['fabula']}</i>"
        )
        await send_long_message(callback.message, response_text, parse_mode="HTML")
    else:
        await callback.message.answer("❌ Помилка: Фабулу не знайдено.")

    await callback.answer()


# ==========================================
# --- ФАБУЛИ ПДР ---
# ==========================================
@router.message(F.text == "🚦 Фабули ПДР")
async def process_fabula_pdr(message: Message):
    await message.answer(
        "🚦 <b>Фабули ПДР</b>\n\nОберіть потрібний підрозділ на клавіатурі нижче:",
        reply_markup=pdr_fabula_submenu,
        parse_mode="HTML"
    )


@router.message(F.text == "🚦 Інші порушення ПДР")
async def show_other_pdr_fabulas(message: Message):
    await message.answer(
        "📚 Розділ 'Інші фабули ПДР' знаходиться у розробці..."
    )


# ==========================================
# --- ФАБУЛИ ГБ ---
# ==========================================
@router.message(F.text == "🛡️ Фабули ГБ")
async def process_fabula_gb(message: Message):
    await message.answer(
        "🛡️ <b>Оберіть категорію порушення:</b>",
        reply_markup=gb_fabula_submenu,
        parse_mode="HTML"
    )


@router.message(F.text.in_({"51", "173", "173-2"}))
async def gb_fabula_coming_soon(message: Message):
    await message.answer("📚 Цей розділ знаходиться у розробці...")


# ==========================================
# --- МТЗ (маршрутні транспортні засоби) ---
# ==========================================
@router.message(F.text == "🚌 МТЗ")
async def show_mtz_fabulas_message(message: Message):
    fabulas = get_all_mtz_fabulas()
    await message.answer(
        "🚌 <b>Фабули МТЗ (маршрутні транспортні засоби)</b>\n\n"
        "Оберіть порушення:",
        reply_markup=get_mtz_flat_keyboard(fabulas, page=1),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("mtz_page:"))
async def handle_mtz_page_switch(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    fabulas = get_all_mtz_fabulas()
    await callback.message.edit_reply_markup(
        reply_markup=get_mtz_flat_keyboard(fabulas, page=page)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mtzfab_"))
async def show_full_fabula_mtz(callback: CallbackQuery):
    fabula_id = int(callback.data.split("_")[1])
    fabula = get_mtz_fabula_by_id(fabula_id)

    if fabula:
        fine_value = escape(fabula['fine'])
        fine_display = (
            f"{fine_value} грн" if fine_value.isdigit() else fine_value
        )

        response_text = (
            f"📌 <b>Стаття {fabula['article_number']} ч. "
            f"{fabula['part_number']} КУпАП</b>\n"
            f"⚠️ <b>{escape(fabula['name'])}</b>\n"
            f"💰 <b>Штраф:</b> {fine_display}\n"
        )
        if fabula['legal_norm']:
            response_text += (
                f"📖 <b>Норма:</b> {escape(fabula['legal_norm'])}\n"
            )
        response_text += (
            f"\n📝 <b>Фабула:</b>\n<i>{escape(fabula['fabula_text'])}</i>"
        )

        back_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🔙 До списку", callback_data="mtz_page:1"
            )]
        ])

        await send_long_message(
            callback.message, response_text, parse_mode="HTML"
        )
        await callback.message.answer("Оберіть дію:", reply_markup=back_kb)
    else:
        await callback.message.answer("❌ Помилка: Фабулу не знайдено.")

    await callback.answer()


# ==========================================
# --- НЕБЕЗПЕЧНІ ВАНТАЖІ (ADR) ---
# ==========================================
@router.message(F.text == "☣️ Небезпечні вантажі")
async def show_adr_categories_message(message: Message):
    await message.answer(
        "☣️ <b>Оберіть категорію порушення:</b>",
        reply_markup=get_adr_sections_keyboard(page=1),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("adr_page:"))
async def handle_adr_page_switch(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(
        reply_markup=get_adr_sections_keyboard(page=page)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adr_sect:"))
async def handle_adr_section_click(callback: CallbackQuery):
    section_idx = int(callback.data.split(":")[1])
    db_category_name = SECTIONS_ADR[section_idx]

    fabulas = get_adr_fabulas_by_category(db_category_name)

    if not fabulas:
        await callback.message.answer(
            f"❌ За категорією «{db_category_name}» фабул не знайдено."
        )
        await callback.answer()
        return

    markup = get_adr_fabulas_keyboard(
        fabulas, category_idx=section_idx, page=1
    )

    await callback.message.edit_text(
        f"🔍 <b>Категорія:</b> {db_category_name}\nОберіть порушення:",
        reply_markup=markup,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adr_fpage:"))
async def handle_adr_fabulas_page_switch(callback: CallbackQuery):
    _, cat_idx_str, page_str = callback.data.split(":")
    cat_idx = int(cat_idx_str)
    page = int(page_str)

    db_category_name = SECTIONS_ADR[cat_idx]
    fabulas = get_adr_fabulas_by_category(db_category_name)

    markup = get_adr_fabulas_keyboard(
        fabulas, category_idx=cat_idx, page=page
    )
    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("adrfab_"))
async def show_full_fabula_adr(callback: CallbackQuery):
    fabula_id = int(callback.data.split("_")[1])
    fabula_data = get_adr_fabula_text(fabula_id)

    if fabula_data:
        title = (
            fabula_data[0]
            if isinstance(fabula_data, tuple)
            else fabula_data['title']
        )
        text = (
            fabula_data[1]
            if isinstance(fabula_data, tuple)
            else fabula_data['fabula_text']
        )

        response_text = (
            f"📌 <b>{title}</b>\n\n"
            f"📝 <b>Фабула:</b>\n<i>{text}</i>"
        )

        back_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🔙 До списку категорій", callback_data="adr_page:1"
            )]
        ])

        await send_long_message(
            callback.message, response_text, parse_mode="HTML"
        )
        await callback.message.answer("Оберіть дію:", reply_markup=back_kb)
    else:
        await callback.message.answer("❌ Помилка: Фабулу не знайдено.")

    await callback.answer()


# ==========================================
# --- ПОШУК ФАБУЛ ДТП ЗА НОМЕРОМ ПУНКТУ ---
# ==========================================
@router.message(
    SearchStates.searching_fabula,
    F.text.regexp(r"^\d+\.\d+(\.\d+)?$"),
)
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
            InlineKeyboardButton(
                text=btn_text, callback_data=f"fabula_{acc['id']}"
            )
        ])

    markup = InlineKeyboardMarkup(inline_keyboard=inline_kb)
    await message.answer(
        f"⚖️ <b>Знайдені фабули за п. {rule}:</b>\n"
        "Оберіть випадок нижче, щоб відкрити його фабулу:",
        reply_markup=markup,
        parse_mode="HTML"
    )
