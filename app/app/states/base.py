from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseStates(StatesGroup):
    fio = State()
    role = State()
    request_type = State()


class ChangeStatusApplication(StatesGroup):
    add_file = State()
    request_number = State()
    request_status = State()
    check_result = State()
    finaly_result = State()

