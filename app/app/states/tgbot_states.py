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
    staff_role = State()
    another_role = State()
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
    another_reason = State()
    description = State()


class EditShpmnt(BaseStates):
    note = State()
    number_ticket = State()
    number_invoice = State()
    storage = State()
    what_edit = State()
    another_what_edit = State()
    description = State()
    extra_files = State()


class ChangeStatus(BaseStates):
    note = State()
    number_bid = State()
    status_in_bid = State()


class AddCoef(BaseStates):
    update_coef = State()
    old_new = State()
    ratio = State()


class UpdateStorage(BaseStates):
    number_bid = State()
    new_storage = State()
    fio = State()
    address_storage = State()


class AddNaming(BaseStates):
    section_material = State()
    subsection_material = State()
    group_material = State()
    name_material = State()
    unit_of_measureament = State()
    add_several_naming = State()


class UpdateSubObject(BaseStates):
    select_subobject = State()
    select_type_work = State()


class EditViewWork(BaseStates):
    edit_sub_object_type_work = State()
    edit_type_work = State()
    edit_sort = State()
    edit_sub_systems = State()


class AddViewWork(BaseStates):
    sub_object = State()
    type_work = State()
    sort = State()
    subsystems = State()
