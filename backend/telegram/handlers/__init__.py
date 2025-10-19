from aiogram import Dispatcher
from .commands import register_commands
from .gameplay import register_game_handlers
from .shop import register_shop_handlers
from .errors import register_error_handlers

def register_handlers(dp: Dispatcher):
    register_commands(dp)
    register_game_handlers(dp)
    register_shop_handlers(dp)
    register_error_handlers(dp)  # Обработка ошибок