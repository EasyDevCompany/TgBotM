from aiogram.utils import executor
from aiogram import Dispatcher

from loader import dp

from app.core.container import Container
from app import middlewares

from app.models.telegram_user import TelegramUser
from app.models.application import Application
from app.models.user import User

from app.handlers import start
from app.handlers import chat

start.register_start_handler(dp=dp)
chat.register_chat_handler(dp=dp)


def on_startup(dispatcher: Dispatcher):
    middlewares.setup(dp=dispatcher)


if __name__ == "__main__":
    container = Container()
    db = container.db()
    db.create_database()
    container.wire(modules=[start, chat])
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))
