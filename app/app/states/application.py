from aiogram.dispatcher.filters.state import State, StatesGroup


class GetApplication(StatesGroup):
    application_id = State()


class GetComment(StatesGroup):
    comment = State()


class EditApplication(StatesGroup):
    field = State()
    new_text = State()
