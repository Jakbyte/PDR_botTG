from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📊 Статистика бота'), 
            KeyboardButton(text='👥 Користувачі') 
        ],
        [
            KeyboardButton(text='📢 Розсилка')
        ],
        [
            KeyboardButton(text='⬅️ Головне меню')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False 
) 