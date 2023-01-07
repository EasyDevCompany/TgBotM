from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from dependency_injector.wiring import inject, Provide
import re

from app.core.config import settings
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
from app.loader import dp, bot
from loguru import logger
from app.states.base import BaseStates
import app.states.tgbot_states as my_states


@dp.callback_query_handler(text='exit', state='*')
async def cancel(query: types. CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.finish()
    await query.message.answer(const.START_MESSAGE, reply_markup=kb.start_work)
    await query.answer()


@dp.callback_query_handler(text='edit', state='*')
async def edit_data(query: types.CallbackQuery, state: FSMContext):
    print(await state.get_state())
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    data = await state.get_data()
    if 'change' in data:
        del data['change']
    print(len(data))
    print(data)
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
    if 'change' in data:
        del data['change']
    message = ''
    for v in data.values():
        message += f'{v[0]}: {v[1]}\n'
    if 'extra_file' in data:
        if data['extra_file'][1] is not None:
            try:
                await bot.send_media_group(chat, data['extra_file'][1])
            except:
                await bot.send_document(chat, data['extra_file'][1],
                                        caption=message,
                                        reply_markup=kb.adm_kb())
        await bot.send_document(chat, data['note'][1],
                                caption=message, reply_markup=kb.adm_kb())
    elif 'note' in data and 'excel' in data:
        media = types.MediaGroup()
        media.attach_document(data['note'][1])
        media.attach_document(data['excel'][1])
        await bot.send_media_group(chat, media=media)
        await bot.send_message(chat, message, reply_markup=kb.adm_kb())
    elif 'note' in data:
        await bot.send_document(chat, data['note'][1],
                                caption=message, reply_markup=kb.adm_kb())
    else:
        await bot.send_message(chat, message, reply_markup=kb.adm_kb())
    await state.finish()
    await query.message.answer(const.START_MESSAGE, reply_markup=kb.start_work)


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


@dp.callback_query_handler(text='start_work')
async def create_ticket(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text='Введите ФИО', reply_markup=kb.exit_kb())
    await state.set_state(BaseStates.fio)


async def get_name(message: types.Message, state: FSMContext):
    # проверяем ввод ФИО из трех русских слов
    if bool(re.search(
            r'\b[\u0401\u0451\u0410-\u044f]+\s+[\u0401\u0451\u0410-\u044f]+\s+[\u0401\u0451\u0410-\u044f]+\b',
            message.text, re.IGNORECASE)
            ):
        await state.update_data(name=['ФИО', message.text])
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await message.answer('Выберите свою роль',
                             reply_markup=new_kb)
        await state.set_state(BaseStates.role)
    else:
        await state.set_state(BaseStates.fio)
        await message.answer('Введите пожалуйста фамилию, имя и отчество')


@dp.callback_query_handler(state=BaseStates.role)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(role=['Роль', query.data])
    new_kb = kb.main_kb().add(kb.exit_button)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Выберите тип запроса',
                               reply_markup=new_kb)
    await state.set_state(BaseStates.request_type)


@dp.callback_query_handler(state=BaseStates.request_type)
async def get_request_type(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    if query.data == 'add_subobject':
        await state.update_data(request_type=[const.REQUEST_TYPE,
                                              'Добавление подобъектов'])
        await state.update_data(adm_or_tech='tech')
        new_kb = kb.add_subobjects_kb().add(kb.exit_button)
        await query.message.answer(const.ADD_SUBOBJECTS)
        await query.message.answer(const.SET_CHAPTER,
                                   reply_markup=new_kb)
        await state.set_state(my_states.AddObj.chapter)
    elif query.data == 'change_status':
        await state.update_data(request_type=[const.REQUEST_TYPE,
                                              'Смена статуса заявки'])
        await state.update_data(adm_or_tech='tech')
        await query.message.answer(const.CHANGE_STATUS_APPLICATION)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.ChangeStatus.note)
    elif query.data == 'edit_type_work':
        await state.update_data(request_type=[const.REQUEST_TYPE,
                                              'Редактирование видов работ'])
        await state.update_data(adm_or_tech='tech')
        await query.message.answer(const.EDIT_TYPE_WORK)
        await query.message.answer(const.EDIT_SUBOBJECT_TYPE_WORK,
                                   reply_markup=kb.exit_kb())
        await state.set_state(my_states.EditViewWork.edit_sub_object_type_work)
    elif query.data == 'add_type_work':
        await state.update_data(request_type=[const.REQUEST_TYPE,
                                              'Добавление видов работ'])
        await state.update_data(adm_or_tech='tech')
        await query.message.answer(const.ADD_TYPE_WORK)
        await query.message.answer(const.SELECT_SUBOBJECT,
                                   reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddViewWork.sub_object)
    elif query.data == 'add_coef':
        await state.update_data(request_type=[
            const.REQUEST_TYPE,
            'Добавление коэффициента пересчёта по наименованию'])
        await state.update_data(adm_or_tech='tech')
        await query.message.answer(const.CONVERSION_FACTOR)
        await query.message.answer(
            const.UPDATE_COEF, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddCoef.update_coef)
    elif query.data == 'update_storage':
        await state.update_data(request_type=[const.REQUEST_TYPE,
                                              'Корректировка склада в заявке'])
        await state.update_data(adm_or_tech='tech')
        await query.message.answer(const.UPDATE_STORAGE)
        await query.message.answer(const.NUMBER_BID, reply_markup=kb.exit_kb())
        await state.set_state(my_states.UpdateStorage.number_bid)
    elif query.data == 'add_names':
        await state.update_data(request_type=[const.REQUEST_TYPE,
                                              'Добавление наименований'])
        await state.update_data(adm_or_tech='tech')
        await query.message.answer(const.ADD_NAMING)
        await query.message.answer(const.SECTION_MATERIAL,
                                   reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddNaming.section_material)
    elif query.data == 'edit_subobject':
        await state.update_data(request_type=[const.REQUEST_TYPE,
                                              'Редактирование подобъектов'])
        await state.update_data(adm_or_tech='tech')
        await query.message.answer(const.EDIT_SUBOBJECT)
        await query.message.answer(const.SELECT_SUBOBJECT,
                                   reply_markup=kb.exit_kb())
        await state.set_state(my_states.UpdateSubObject.select_subobject)
    elif query.data == 'add_materials':
        await state.update_data(request_type=[
            const.REQUEST_TYPE,
            'Добавление материалов на свободный остаток'])
        await state.update_data(adm_or_tech='tech')
        await query.message.answer(const.ADD_MATERIALS)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddMat.note)
    elif query.data == 'add_EDO':
        await state.update_data(request_type=[const.REQUEST_TYPE,
                                              'Добавление объекта в ЭДО'])
        await state.update_data(adm_or_tech='adm')
        await query.message.answer(const.ADD_EDO)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddObjAdm.note)
    elif query.data == 'open_access':
        await state.update_data(request_type=[
            const.REQUEST_TYPE, 'Открытие доступов в ЭДО для сотрудников'])
        await state.update_data(adm_or_tech='adm')
        await query.message.answer(const.OPEN_EDO)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.OpenAcs.note)
    elif query.data == 'edit_incorrect_move_admin':
        await state.update_data(request_type=[
            const.REQUEST_TYPE, 'Редактирование некорректного перемещения'])
        await state.update_data(adm_or_tech='adm')
        await query.message.answer(const.EDIT_MOV)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.EditMoveAdm.note)
    elif query.data == 'edit_shipment':
        await state.update_data(request_type=[const.REQUEST_TYPE,
                                              'Корректировка поставок'])
        await state.update_data(adm_or_tech='adm')
        await query.message.answer(const.EDIT_SHIP)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.EditShpmnt.note)
    elif query.data == 'adjustment_invoice':
        await state.update_data(request_type=[
            const.REQUEST_TYPE, 'Корректировка оформленной накладной'])
        await state.update_data(adm_or_tech='tech')
        await query.message.answer(const.ADJ_INVOICE)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AdjInv.note)


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())
    dp.register_callback_query_handler(create_ticket)
    dp.register_callback_query_handler(cancel, text='exit', state='*')
    dp.register_callback_query_handler(edit_data, text='edit', state='*')
    dp.register_message_handler(get_name, state=BaseStates.fio)
    dp.register_callback_query_handler(get_role, state=BaseStates.role)
    dp.register_callback_query_handler(get_request_type, state=BaseStates.request_type)
    dp.register_callback_query_handler(send_ticket, text='send', state='*')
    dp.register_message_handler(test_func, commands=["test"])
