import logging
import asyncio
import os 

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import user_hd, admin_hd
from dotenv import load_dotenv

from db_users.connect import init_users_db


load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

dp.include_router(admin_hd.router)
dp.include_router(user_hd.router)

async def main():
    init_users_db()
    
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
    ])

    await bot.delete_webhook(drop_pending_updates=True) 
    
    await dp.start_polling(bot)

if __name__  == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('🤖 Бот включено та готово до роботи!')
    
    try:
        asyncio.run(main())  
    except KeyboardInterrupt:
        print('💤 Бот вимкнено!')