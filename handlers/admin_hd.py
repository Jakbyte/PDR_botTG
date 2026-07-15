import os
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.exceptions import TelegramForbiddenError, TelegramAPIError

from keyboard.admin_kb import admin_menu
from keyboard.user_kb import main_menu  


from db_users.requests import get_stats, get_active_users, set_user_inactive, get_connection


class AdminStates(StatesGroup):
    waiting_for_broadcast = State()

router = Router()

ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

#  ФІЛЬТР НА АДМІНА 
def is_admin(message: types.Message) -> bool:
    return message.from_user.id == ADMIN_ID


#  ВХІД В АДМІН-ПАНЕЛЬ 
@router.message(Command("admin"), is_admin)
async def admin_panel(message: types.Message):

    await message.answer(
        "👋 <b>Ласкаво просимо до адміністративної панелі бота «ПДР України»!</b>\n\n"
        "Тут ви можете керувати основними функціями бота:\n\n"
        "📊 <b>Статистика</b> — перегляд активності бота та кількості користувачів.\n\n"
        "👥 <b>Користувачі</b> — пошук, перегляд інформації та керування користувачами.\n\n"
        "📢 <b>Розсилка</b> — надсилання повідомлень усім користувачам.\n\n"
        "⬅️ <b>Головне меню</b> — вихід з адміністративної панелі.\n\n"
        "👇 Оберіть потрібний розділ:",
        reply_markup=admin_menu, 
        parse_mode="HTML"
    )


#  КНОПКА СТАТИСТИКА 
@router.message(F.text == "📊 Статистика бота", is_admin)
async def show_stats(message: types.Message):
    total, active = get_stats()
    blocked = total - active
    
    await message.answer(
        "📊 <b>Поточна статистика бота:</b>\n\n"
        f"👥 Всього зареєстровано: <code>{total}</code>\n"
        f"🟢 Активні користувачі: <code>{active}</code>\n"
        f"🔴 Заблокували бота: <code>{blocked}</code>",
        parse_mode="HTML"
    )


# КНОПКА КОРИСТУВАЧІ (Вивід останніх 30)
@router.message(F.text == "👥 Користувачі", is_admin)
async def show_users_list(message: types.Message):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, first_name, username, is_active FROM users LIMIT 30")
            users = cursor.fetchall()
            
        if not users:
            await message.answer("ℹ️ У базі даних поки немає користувачів.")
            return
            
        text = "👥 <b>Список користувачів (останні 30):</b>\n\n"
        for user_id, first_name, username, is_active in users:
            status = "🟢" if is_active == 1 else "🔴"
            user_link = f"@{username}" if username else "немає юзернейму"
            text += f"{status} {first_name} ({user_link}) | ID: <code>{user_id}</code>\n"
            
        await message.answer(text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"❌ Помилка читання списку користувачів: {e}")


# КНОПКА РОЗСИЛКА (Вхід в режим очікування повідомлення)
@router.message(F.text == "📢 Розсилка", is_admin)
async def start_broadcast(message: types.Message, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_broadcast)
    await message.answer(
        "📢 <b>Режим розсилки активовано!</b>\n\n"
        "Будь ласка, надішліть повідомлення, яке ви хочете надіслати всім користувачам. "
        "Це може бути текст із форматуванням, картинка, відео чи навіть документ.\n\n"
        "<i>Для скасування надішліть слово: <b>відміна</b></i>",
        parse_mode="HTML"
    )


# --- ОБРОБКА ТЕКСТУ РОЗСИЛКИ ---
@router.message(AdminStates.waiting_for_broadcast, is_admin)
async def process_broadcast(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "відміна":
        await state.clear()
        await message.answer("❌ Розсилку скасовано.", reply_markup=admin_menu)
        return

    await state.clear()
    
    active_users = get_active_users()
    if not active_users:
        await message.answer("❌ Немає активних користувачів для розсилки.", reply_markup=admin_menu)
        return

    await message.answer(f"⏳ Початок розсилки на {len(active_users)} користувачів...")
    
    sent_count = 0
    blocked_count = 0
    
    for user_id in active_users:
        try:
            await message.copy_to(chat_id=user_id)
            sent_count += 1
            await asyncio.sleep(0.05) 
        except TelegramForbiddenError:
            set_user_inactive(user_id)
            blocked_count += 1
        except TelegramAPIError as e:
            print(f"Помилка відправки користувачу {user_id}: {e}")

    await message.answer(
        "✅ <b>Розсилку успішно завершено!</b>\n\n"
        f"📩 Успішно доставлено: <code>{sent_count}</code>\n"
        f"🚫 Виявлено нових блокувань: <code>{blocked_count}</code>",
        reply_markup=admin_menu,
        parse_mode="HTML"
    )


# --- 4. КНОПКА ГОЛОВНЕ МЕНЮ (Вихід з адмінки) ---
@router.message(F.text == "⬅️ Головне меню", is_admin)
async def exit_admin(message: types.Message):
    await message.answer(
        "Повертаємося до головного меню користувача.",
        reply_markup=main_menu
    )