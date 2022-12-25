from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseStates(StatesGroup):
    fio = State()
    role = State()
    request_type = State()
