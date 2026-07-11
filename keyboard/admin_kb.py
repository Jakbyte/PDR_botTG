from aiogram.types import ReplyKeyboardMarkup, KeybordButton

admin_menu = ReplyKeyboardMarkup(
	keyboard = [
	[KeyboardButton(text = '📊 Статистика бота'), KeyboardButton(text = '👤 Пользователи')],
	[KeyboardButton(text = '📢 Розсилка'), KeyboardButton(text = '🚫 Бан / Помилування')],
	[KeyboardButton(text = '⬅️ Головне меню')]
	],
	resize_keyboard = True

	)