from aiogram.dispatcher.filters.state import State
from .base import BaseStates


class AdminOrModerator(BaseStates):
    take_to_work = State()
    return_to_employee = State()
    request_processed = State()
    sure = State()
    edit = State()
