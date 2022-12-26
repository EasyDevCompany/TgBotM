from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class BaseState(StatesGroup):
    name = State()
    role = State()


class EditMove(BaseState):
    note = State()
    chapter = State()
    section = State()
    subobject_name = State()
    sort = State()
    subsystems = State()


class AddObj(EditMove):
    pass


class AddMat(BaseState):
    note = State()
    storage = State()
    excel = State()
    myc = State()
    obj = State()


class AddObj(BaseState):
    note = State()
    obj_name = State()
    title = State()
    storage = State()
    if_new = State()


class OpenAcs(BaseState):
    note = State()
    staff_name = State()
    what_acs = State()
    role = State()
    for_what = State()
    obj_name = State()


class EditMoveAdm(BaseState):
    note = State()
    number_ticket = State()
    number_invoice = State()
    storage_out = State()
    storage_in = State()
    status = State()
    reason = State()
    description = State()


class EditShpmnt(BaseState):
    note = State()
    number_ticket = State()
    number_invoice = State()
    storage = State()
    what_edit = State()
    description = State()
    extra_files = State()
