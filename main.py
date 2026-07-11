from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers.user_hd import router 
import asyncio
import os 
from dotenv import load_dotenv
import logging

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
dp.include_router(router)

async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
    ])
    await dp.start_polling(bot)

async def main():
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot)

if __name__  == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('Бот включен!')
    try:
        asyncio.run(main())  
    except KeyboardInterrupt:
        print('Бот выключен!')