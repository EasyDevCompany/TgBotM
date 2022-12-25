from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseStates(StatesGroup):
    role = State()
    request_type = State()
