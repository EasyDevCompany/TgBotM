from aiogram.utils import executor
from aiogram import Dispatcher

from loader import dp

from core.container import Container
import middlewares

from handlers import start
import handlers.forms.moderator as moderator
import handlers.forms.administrator as administrator


start.register_start_handler(dp=dp)
moderator.add_subobject.register(dp=dp)
moderator.add_material.register(dp=dp)
administrator.add_edo.register(dp=dp)
administrator.open_edo.register(dp=dp)
administrator.edit_some_moving.register(dp=dp)
administrator.adjustment_of_supplies.register(dp=dp)


def on_startup(dispatcher: Dispatcher):
    middlewares.setup(dp=dispatcher)


if __name__ == "__main__":
    container = Container()
    db = container.db()
    db.create_database()
    container.wire(modules=[start])
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))
