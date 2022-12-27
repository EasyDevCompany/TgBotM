from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import executor
from aiogram import Dispatcher, types

from app.app.handlers.form_change_status_application import name_invalid, name, role, type_application, \
    change_status_application, added_file, write_number_application, write_number_application_invalid, \
    write_status_application, write_status_application_invalid, check_result, finally_result
from app.app.states.base import BaseStates, ChangeStatusApplication
from loader import dp

from app.core.container import Container
from app import middlewares

from app.app.handlers import start

start.register_start_handler(dp=dp)


def on_startup(dispatcher: Dispatcher):
    middlewares.setup(dp=dispatcher)


def register_handler(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())
    dp.register_callback_query_handler(name)
    dp.register_message_handler(name_invalid, lambda message: message.text.isdigit(), state=BaseStates.fio)
    dp.register_message_handler(role, state=BaseStates.fio)
    dp.register_callback_query_handler(type_application, state=BaseStates.role)
    dp.register_callback_query_handler(change_status_application, state=BaseStates.request_type)
    dp.register_callback_query_handler(added_file, state=ChangeStatusApplication.add_file)
    dp.register_message_handler(write_number_application, state=ChangeStatusApplication.request_number,
                                content_types=types.ContentTypes.DOCUMENT)
    dp.register_message_handler(write_number_application_invalid, lambda message: not message.text.isdigit(),
                                state=ChangeStatusApplication.request_status)
    dp.register_message_handler(write_status_application, lambda message: message.text.isdigit(),
                                state=ChangeStatusApplication.request_status)
    dp.register_message_handler(write_status_application_invalid, lambda message: message.text.isdigit(),
                                state=ChangeStatusApplication.check_result)
    dp.register_message_handler(check_result, state=ChangeStatusApplication.check_result)
    dp.register_callback_query_handler(finally_result, state=ChangeStatusApplication.finaly_result)


if __name__ == "__main__":
    container = Container()
    db = container.db()
    db.create_database()
    container.wire(modules=[start])
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))
