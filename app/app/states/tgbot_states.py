from aiogram.dispatcher.filters.state import State
from .base import BaseStates


class AdjInv(BaseStates):
    note = State()
    number_invoice = State()
    number_ticket = State()
    what_edit = State()
    what_edit_correct = State()
    description = State()
    sure = State()
    edit = State()


class AddObj(BaseStates):
    note = State()
    chapter = State()
    section = State()
    subobject_name = State()
    sort = State()
    choise = State()
    subsystems = State()
    subsystems_edit = State()
    sure = State()
    edit = State()
    edit_chapter = State()


class AddMat(BaseStates):
    note = State()
    storage = State()
    excel = State()
    myc = State()
    obj = State()
    sure = State()
    edit = State()


class AddObjAdm(BaseStates):
    note = State()
    obj_name = State()
    title = State()
    storage = State()
    new_or_exist = State()
    new_or_exist_edit = State()
    sure = State()
    edit = State()


class OpenAcs(BaseStates):
    note = State()
    staff_name = State()
    what_acs = State()
    staff_role = State()
    another_role = State()
    staff_role_edit = State()
    for_what = State()
    obj_name = State()
    sure = State()
    edit = State()


class EditMoveAdm(BaseStates):
    note = State()
    number_ticket = State()
    number_invoice = State()
    storage_out = State()
    storage_in = State()
    status = State()
    status_edit = State()
    reason = State()
    reason_edit = State()
    another_reason = State()
    description = State()
    sure = State()
    edit = State()


class EditShpmnt(BaseStates):
    note = State()
    number_ticket = State()
    number_invoice = State()
    storage = State()
    what_edit = State()
    what_edit_correct = State()
    another_what_edit = State()
    description = State()
    extra_files = State()
    sure = State()
    edit = State()


class ChangeStatus(BaseStates):
    note = State()
    number_bid = State()
    status_in_bid = State()
    sure = State()
    edit = State()


class AddCoef(BaseStates):
    update_coef = State()
    old_new = State()
    ratio = State()
    sure = State()
    edit = State()


class UpdateStorage(BaseStates):
    number_bid = State()
    new_storage = State()
    contact_fio = State()
    address_storage = State()
    sure = State()
    edit = State()


class AddNaming(BaseStates):
    section_material = State()
    subsection_material = State()
    group_material = State()
    name_material = State()
    unit_of_measureament = State()
    add_several_naming = State()
    sure = State()
    edit = State()


class UpdateSubObject(BaseStates):
    select_subobject = State()
    select_type_work = State()
    sure = State()
    edit = State()


class EditViewWork(BaseStates):
    edit_sub_object_type_work = State()
    edit_type_work = State()
    edit_sort = State()
    edit_sub_systems = State()
    subsystems_edit = State()
    sure = State()
    edit = State()


class AddViewWork(BaseStates):
    sub_object = State()
    type_work = State()
    sort = State()
    subsystems = State()
    subsystems_edit = State()
    sure = State()
    edit = State()
