from aiogram.utils import executor
from aiogram import Dispatcher

from loader import dp

from app.core.container import Container
from app import middlewares

from app.handlers import start, chat
import handlers.forms.moderator as moderator
import handlers.forms.administrator as administrator

chat.register_start_support_handler(dp=dp)
start.register_start_handler(dp=dp)
moderator.add_subobject.register(dp=dp)
moderator.add_material.register(dp=dp)
moderator.add_naming.register(dp=dp)
moderator.add_view_job.register(dp=dp)
moderator.change_status_application.register(dp=dp)
moderator.conversion_factor.register(dp=dp)
moderator.edit_subobject.register(dp=dp)
moderator.edit_view_job.register(dp=dp)
moderator.adjustment_invoice.register(dp=dp)
moderator.update_storage.register(dp=dp)
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
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))