from create_bot import dp
from handlers import user_hd

def register_all_handlers():
    dp.include_router(user_hd.router)