from aiogram.utils import executor
from aiogram import Dispatcher

from loader import dp

from app.core.container import Container
from app import middlewares

from app.handlers import start


def on_startup(dispatcher: Dispatcher):
    middlewares.setup(dp=dispatcher)


if __name__ == "__main__":
    container = Container()
    db = container.db()
    db.create_database()
    container.wire(modules=[start])
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))
