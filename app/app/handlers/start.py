from aiogram.types import InputFile
from dependency_injector.wiring import inject, Provide
import re
import pathlib
from pathlib import Path

from app.core.container import Container
from app.models.application import Application
from app.services.application import ApplicationService

from app.models.telegram_user import TelegramUser
from app.services.tg_user_service import TelegramUserService

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from app.utils import const
import app.keyboards.inline_keyboard as kb
from app.loader import bot
from app.states.base import BaseStates
import app.states.tgbot_states as my_states
from logger import logger
from app.utils.const import EDIT_POINT, FIO, ROLE, ERROR_CONTACT, R_TYPE, WAITING_ANSWER


async def cancel(query: types. CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.finish()
    await query.message.answer(const.START_MESSAGE, reply_markup=kb.start_work)
    await query.answer()


async def edit_data(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    data = await state.get_data()
    if 'change' in data:
        del data['change']
    try:
        del data['message_id']
    except:
        pass
    logger.info(data)
    await query.message.answer(EDIT_POINT,
                               reply_markup=kb.genmarkup(data=data))
    await query.answer()


@inject
async def send_ticket(query: types.CallbackQuery,
                      state: FSMContext,
                      application: ApplicationService = Provide[Container.application_service]):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    data = await state.get_data()
    if 'change' in data:
        del data['change']
    if 'message_id' in data:
        del data['message_id']
    await application.create(
        user_id=query.from_user.id,
        obj_in=data
    )
    await state.finish()
    await query.message.answer(
        WAITING_ANSWER)
    await query.message.answer(
        const.START_MESSAGE,
        reply_markup=kb.start_work
    )


@inject
async def test_func(
        message: types.Message,
        application_service: ApplicationService = Provide[Container.application_service]
):
    user_id = message.from_user.id
    await application_service.create(obj_in={
            "role": Application.Role.curator,
            "request_answered": Application.RequestAnswered.moderator,
            "request_type": Application.RequestType.add_edo,
            "field_one": "test",
            "field_two": "test",
            "field_three": "test",
            "field_four": "test"
        },
        user_id=user_id
    )


@dp.callback_query_handler(text='exit', state='*')
async def cancel(query: types. CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.finish()
    await query.message.answer(const.START_MESSAGE, reply_markup=kb.start_work)
    await query.answer()


@dp.callback_query_handler(text='edit', state='*')
async def edit_data(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    data = await state.get_data()
    if 'change' in data:
        del data['change']
    await query.message.answer('Выберите номер пункта для корректировки: ',
                               reply_markup=kb.genmarkup(data=data))
    await query.answer()


@dp.callback_query_handler(text='send', state='*')
async def send_ticket(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    data = await state.get_data()
    if data['adm_or_tech'] == 'adm':
        chat = settings.ADMIN_CHAT_ID
    elif data['adm_or_tech'] == 'tech':
        chat = settings.TECH_CHAT_ID
    del data['adm_or_tech']
    message = ''
    for k, v in data.items():
        message += f'{k}: {v}\n'
    await bot.send_message(chat, message, reply_markup=kb.adm_kb())
    await state.finish()
    await query.message.answer(const.START_MESSAGE, reply_markup=kb.start_work)


@inject
async def start(
        message: types.Message,
        tg_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    await tg_user_service.get_or_create(
        obj_in={
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "user_type": TelegramUser.UserType.employee
        }
    )
    await message.answer(
        const.START_MESSAGE,
        reply_markup=kb.start_work
    )


async def create_ticket(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text=FIO, reply_markup=kb.exit_kb())
    await state.set_state(BaseStates.fio)


async def get_name(message: types.Message, state: FSMContext):
    # проверяем ввод ФИО из трех русских слов
    if bool(re.search(
            r'\b[\u0401\u0451\u0410-\u044f]+\s+[\u0401\u0451\u0410-\u044f]+\s+[\u0401\u0451\u0410-\u044f]+\b',
            message.text, re.IGNORECASE)
            ):
        await state.update_data(name=message.text)
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await message.answer(ROLE,
                             reply_markup=new_kb)
        await state.set_state(BaseStates.role)
    else:
        await state.set_state(BaseStates.fio)
        await message.answer(ERROR_CONTACT)


async def get_role(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(role=query.data)
    new_kb = kb.main_kb().add(kb.exit_button)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer(R_TYPE,
                               reply_markup=new_kb)
    await state.set_state(BaseStates.request_type)


async def get_request_type(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    if query.data == 'add_subobject':
        await state.update_data(
            request_type=Application.RequestType.add_subobject)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        new_kb = kb.add_subobjects_kb().add(kb.exit_button)
        await query.message.answer(const.ADD_SUBOBJECTS)
        await query.message.answer(const.SET_CHAPTER,
                                   reply_markup=new_kb)
        await state.set_state(my_states.AddObj.chapter)
    elif query.data == 'change_status':
        path = Path(pathlib.Path.cwd(), "Смена статуса заявки.docx")
        await state.update_data(
            request_type=Application.RequestType.change_status_application)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        await query.message.answer(const.CHANGE_STATUS_APPLICATION)
        await query.message.answer_document(InputFile(path))
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.ChangeStatus.note)
    elif query.data == 'edit_type_work':
        await state.update_data(
            request_type=Application.RequestType.edit_view_job)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        await query.message.answer(const.EDIT_TYPE_WORK)
        await query.message.answer(const.EDIT_SUBOBJECT_TYPE_WORK,
                                   reply_markup=kb.exit_kb())
        await state.set_state(my_states.EditViewWork.edit_sub_object_type_work)
    elif query.data == 'add_type_work':
        await state.update_data(
            request_type=Application.RequestType.add_view_job)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        await query.message.answer(const.ADD_TYPE_WORK)
        await query.message.answer(const.SELECT_SUBOBJECT,
                                   reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddViewWork.sub_object)
    elif query.data == 'add_coef':
        await state.update_data(
            request_type=Application.RequestType.conversion_factor)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        await query.message.answer(const.CONVERSION_FACTOR)
        await query.message.answer(
            const.UPDATE_COEF, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddCoef.update_coef)
    elif query.data == 'update_storage':
        await state.update_data(
            request_type=Application.RequestType.warehouse_adjustments)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        await query.message.answer(const.UPDATE_STORAGE)
        await query.message.answer(const.NUMBER_BID, reply_markup=kb.exit_kb())
        await state.set_state(my_states.UpdateStorage.number_bid)
    elif query.data == 'add_names':
        path = Path(pathlib.Path.cwd(), "шаблон_добавления_наименований_материалов_в_ЭДО.xlsx")
        await state.update_data(
            request_type=Application.RequestType.add_naming)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        await query.message.answer(const.ADD_NAMING)
        await query.message.answer_document(InputFile(path))
        await query.message.answer(const.SECTION_MATERIAL,
                                   reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddNaming.section_material)
    elif query.data == 'edit_subobject':
        await state.update_data(
            request_type=Application.RequestType.edit_subobject)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        await query.message.answer(const.EDIT_SUBOBJECT)
        await query.message.answer(const.SELECT_SUBOBJECT,
                                   reply_markup=kb.exit_kb())
        await state.set_state(my_states.UpdateSubObject.select_subobject)
    elif query.data == 'add_materials':
        path1 = Path(pathlib.Path.cwd(), "добавление_материалов_на_свободный_остаток.docx")
        path2 = Path(pathlib.Path.cwd(), "добавление_материалов_на_свободный_остаток.xlsx")
        await state.update_data(
            request_type=Application.RequestType.add_material)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        await query.message.answer(const.ADD_MATERIALS)
        await query.message.answer_document(InputFile(path1))
        await query.message.answer_document(InputFile(path2))
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddMat.note)
    elif query.data == 'add_EDO':
        path = Path(pathlib.Path.cwd(), "Добавление объекта в ЭДО.docx")
        await state.update_data(request_type=Application.RequestType.add_edo)
        await state.update_data(
            request_answered=Application.RequestAnswered.admin)
        await query.message.answer(const.ADD_EDO)
        await query.message.answer_document(InputFile(path))
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddObjAdm.note)
    elif query.data == 'open_access':
        path = Path(pathlib.Path.cwd(), "Открытие доступов в ЭДО для сотрудников.docx")
        await state.update_data(request_type=Application.RequestType.open_edo)
        await state.update_data(
            request_answered=Application.RequestAnswered.admin)
        await query.message.answer(const.OPEN_EDO)
        await query.message.answer_document(InputFile(path))
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.OpenAcs.note)
    elif query.data == 'edit_incorrect_move_admin':
        path = Path(pathlib.Path.cwd(), "Редактирование некорректного перемещения.docx")
        await state.update_data(
            request_type=Application.RequestType.edit_some_moving)
        await state.update_data(
            request_answered=Application.RequestAnswered.admin)
        await query.message.answer(const.EDIT_MOV)
        await query.message.answer_document(InputFile(path))
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.EditMoveAdm.note)
    elif query.data == 'edit_shipment':
        path = Path(pathlib.Path.cwd(), "Корректировка поставок.docx")
        await state.update_data(
            request_type=Application.RequestType.adjustment_of_supplies)
        await state.update_data(
            request_answered=Application.RequestAnswered.admin)
        await query.message.answer(const.EDIT_SHIP)
        await query.message.answer_document(InputFile(path))
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.EditShpmnt.note)
    elif query.data == 'adjustment_invoice':
        path = Path(pathlib.Path.cwd(), "Корректировка оформленной накладной.docx")
        await state.update_data(
            request_type=Application.RequestType.adjustment_invoice)
        await state.update_data(
            request_answered=Application.RequestAnswered.moderator)
        await query.message.answer(const.ADJ_INVOICE)
        await query.message.answer_document(InputFile(path))
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AdjInv.note)


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())
    dp.register_callback_query_handler(create_ticket, text='start_work')
    dp.register_callback_query_handler(cancel, text='exit', state='*')
    dp.register_callback_query_handler(edit_data, text='edit', state='*')
    dp.register_message_handler(get_name, state=BaseStates.fio)
    dp.register_callback_query_handler(get_role, state=BaseStates.role)
    dp.register_callback_query_handler(get_request_type, state=BaseStates.request_type)
    dp.register_callback_query_handler(send_ticket, text='send', state='*')
    dp.register_message_handler(test_func, commands=["test"])
