from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура главного меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ПДР України'),
            KeyboardButton(text="ℹ Про бота")
        ]
    ],
    resize_keyboard=True
)

# Клавиатура ПДР Украинї
pdr_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='⬅ Назад')]
    ],
    resize_keyboard=True
)
