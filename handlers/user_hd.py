from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from data.pdr_ua import pdr
from keyboard.user_kb import main_menu, pdr_menu


router = Router()  

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Головне меню:", reply_markup=main_menu)

@router.message(F.text == "ПДР України")
async def pdr_ukrainy(message: Message):
    await message.answer('Для пошуку по пункту правил:\n Введи пункт правил(Наприклад: 8.4)', reply_markup=pdr_menu)

@router.message(F.text == "ℹ Про бота")
async def about(message: Message):
    text = (
        "ℹ️ <b>Про бота «ПДР України | Швидкий пошук»</b>\n\n"
        "Цей бот створений для водіїв, кандидатів у водії та всіх, кому потрібно "
        "миттєво перевірити правила дорожнього руху прямо в дорозі або під час навчання. 🚘\n\n"
        "📌 <b>Головні переваги:</b>\n"
        "• <b>Миттєвий пошук:</b> Просто введіть номер пункту (наприклад, <code>9.2</code> або <code>15.9</code>), і бот одразу видасть текст правила.\n"
        "• <b>Актуальність:</b> База даних містить офіційну та найсвіжішу редакцію ПДР України.\n"
        "• <b>Зручність:</b> Більше не потрібно гортати довгі сторінки чи шукати в Google — усе доступно в один клік.\n\n"
        "💡 <b>Корисна порада:</b>\n"
        "Щоб розпочати новий пошук, вам не потрібно натискати жодних кнопок — просто введіть новий номер пункту в полі вводу у будь-який момент!\n\n"
        "───────────────────\n"
        "👨‍💻 <b>Підтримка та пропозиції:</b>\n"
        "Якщо ви знайшли помилку або маєте ідею щодо покращення бота, пишіть розробнику: @jakbyte"
    )
    
    await message.answer(text, parse_mode="HTML")

# Назад
@router.message(F.text == "⬅ Назад")
async def back(message: Message):
    await message.answer("Головне меню:", reply_markup=main_menu)

async def send_long_message(message: Message, text: str, chunk_size: int = 4096):
    for i in range(0, len(text), chunk_size):
        await message.answer(text[i:i + chunk_size])

@router.message(F.text.regexp(r"^\d+\.\d+(\.\d+)?$"))
async def handle_rule(message: Message):
    rule = message.text.strip()
    if rule in pdr:
        await send_long_message(message, f"Пункт {rule}:\n{pdr[rule]}")
    else:
        await message.answer(f"Пункт {rule} не знайдено")