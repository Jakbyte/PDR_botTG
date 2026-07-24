from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from db_users.requests import add_user
from handlers.common import send_long_message
from keyboard.user_kb import main_menu

from handlers.kupap_handlers import router as kupap_router
from handlers.npu_handlers import router as npu_router
from handlers.fabula_handlers import router as fabula_router
from handlers.pdr_handlers import router as pdr_router

router = Router()

# Порядок включення роутерів має значення:
# kupap та npu — перші, бо мають state-фільтри для текстових повідомлень
# fabula — перед pdr, бо має regex-хендлер зі станом
# pdr — останній, бо має catch-all regex для номерів пунктів
router.include_router(kupap_router)
router.include_router(npu_router)
router.include_router(fabula_router)
router.include_router(pdr_router)


# ==========================================
# --- СТАТТ ТА ГОЛОВНЕ МЕНЮ ---
# ==========================================
@router.message(F.text == "/start")
async def start(message: Message):
    add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    await message.answer(
        f"👋 Привіт, {message.from_user.first_name}!\n"
        "Я допоможу тобі швидко знайти ПДР України. "
        "Оберіть дію в меню нижче:",
        reply_markup=main_menu
    )


@router.message(F.text == "ℹ Про бота")
async def about(message: Message):
    text = (
        "ℹ️ <b>Про бота «ПДР України | Швидкий пошук»</b>\n\n"
        "Довідковий інструмент для поліцейських — швидкий доступ до нормативної "
        "бази.\n\n"
        "<b>📌 Розділи:</b>\n"
        "📘 <b>ПДР</b> — пошук пункту за номером (наприклад, <code>9.2</code>) "
        "або за розділами.\n"
        "📋 <b>КУпАП</b> — пошук статті за номером, санкція виділена окремо "
        "для швидкої перевірки.\n"
        "👮 <b>Закон України «Про Національну поліцію»</b> — за номером "
        "статті.\n"
        "⚖️ <b>Фабули</b> — приклади кваліфікації правопорушень по ДТП та "
        "небезпечних вантажах.\n\n"
        "💡 Гортайте статті кнопками «◀️ Попередня / Наступна ▶️» — не "
        "потрібно щоразу вводити номер заново.\n\n"
        "🔄 База регулярно оновлюється відповідно до змін у "
        "законодавстві.\n\n"
        "───────────────────\n"
        "👨‍💻 <b>Підтримка та пропозиції:</b>\n"
        "Якщо ви знайшли помилку або маєте ідею щодо покращення бота, "
        "пишіть розробнику: @jakbyte"
    )
    await message.answer(text, parse_mode="HTML")


# ==========================================
# --- КНОПКИ НАЗАД (СИСТЕМА ПОВЕРНЕНЬ) ---
# ==========================================
@router.message(F.text == "⬅ Назад до головного")
async def back_to_main_from_fabula(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Головне меню:", reply_markup=main_menu)


@router.message(F.text == "⬅ Назад до menu ПДР")
async def back_to_pdr(message: Message):
    from handlers.pdr_handlers import pdr_ukrainy
    await pdr_ukrainy(message)


@router.message(F.text == "⬅ Назад")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Головне меню:", reply_markup=main_menu)


@router.callback_query(F.data == "noop")
async def handle_noop(callback: CallbackQuery):
    await callback.answer()
