from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from keyboard.admin_kb import admin_menu
from create_bot import ADMIN_ID

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
	if message.from_user.id == ADMIN_ID:
		await message.answer("Перемикаю інтерфейс...", reply_markup = ReplyKeyboardRemove())
		await message.answer("""
👋 <b>Ласкаво просимо до адміністративної панелі бота «ПДР України»!</b>

Тут ви можете керувати основними функціями бота:

📊 <b>Статистика</b> — перегляд активності бота та кількості користувачів.

👥 <b>Користувачі</b> — пошук, перегляд інформації та керування користувачами.

📢 <b>Розсилка</b> — надсилання повідомлень усім користувачам.

🚫 <b>Бан / Помилування</b> — блокування та розблокування користувачів.

⬅️ <b>Головне меню</b> — вихід з адміністративної панелі.

👇 Оберіть потрібний розділ:
"""
			reply_markup = admin_menu
			parse_mode = "HTML"
		)
	else:
		await message.answer("🚫 В доступі відмовлено")