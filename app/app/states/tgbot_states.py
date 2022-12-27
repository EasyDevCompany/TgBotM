from aiogram.dispatcher.filters.state import State
from .base import BaseStates


class EditMove(BaseStates):
    note = State()
    number_ticket = State()
    number_invoice = State()
    storage_out = State()
    storage_in = State()
    status = State()
    reason = State()
    description = State()


class AddObj(BaseStates):
    note = State()
    chapter = State()
    section = State()
    subobject_name = State()
    sort = State()
    choise = State()
    subsystems = State()


class AddMat(BaseStates):
    note = State()
    storage = State()
    excel = State()
    myc = State()
    obj = State()


class AddObjAdm(BaseStates):
    note = State()
    obj_name = State()
    title = State()
    storage = State()
    exist_storage = State()
    if_new = State()


class OpenAcs(BaseStates):
    note = State()
    staff_name = State()
    what_acs = State()
    role = State()
    for_what = State()
    obj_name = State()


class EditMoveAdm(BaseStates):
    note = State()
    number_ticket = State()
    number_invoice = State()
    storage_out = State()
    storage_in = State()
    status = State()
    reason = State()
    description = State()


class EditShpmnt(BaseStates):
    note = State()
    number_ticket = State()
    number_invoice = State()
    storage = State()
    what_edit = State()
    description = State()
    extra_files = State()
