import logging
import asyncio
from aiogram.types import BotCommand

from create_bot import bot, dp
from bot import register_all_handlers
from db_users.connect import init_users_db


register_all_handlers()


async def main():
    init_users_db()

    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
    ])

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('🤖 Бот включено та готово до роботи!')

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('💤 Бот вимкнено!')