from aiogram.utils import executor
from aiogram import Dispatcher

from loader import dp

from core.container import Container
import middlewares

from handlers import start

start.register_start_handler(dp=dp)


def on_startup(dispatcher: Dispatcher):
    middlewares.setup(dp=dispatcher)

start.register(dp)

if __name__ == "__main__":
    container = Container()
    # db = container.db()
    # db.create_database()
    container.wire(modules=[start])
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))
