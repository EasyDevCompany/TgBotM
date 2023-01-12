from aiogram.utils import executor
from aiogram import Dispatcher

from loader import dp

from app.core.container import Container
from app import middlewares

from app.models.telegram_user import TelegramUser
from app.models.application import Application
from app.models.user import User

from app.handlers import start, chat, forms
from app.handlers.forms import administrator
import app.handlers.forms.moderator as moderator
import app.handlers.forms.administrator as administrator


start.register_start_handler(dp=dp)
chat.register_chat_handler(dp=dp)
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
    container.wire(modules=[start,
                            chat,
                            administrator.add_edo,
                            administrator.adjustment_of_supplies,
                            administrator.edit_some_moving,
                            administrator.open_edo,
                            moderator.change_status_application,
                            moderator.add_material,
                            moderator.add_naming,
                            moderator.add_subobject,
                            moderator.add_view_job,
                            moderator.adjustment_invoice,
                            moderator.conversion_factor,
                            moderator.edit_subobject,
                            moderator.edit_view_job,
                            moderator.update_storage])
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))
