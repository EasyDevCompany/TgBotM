from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from dependency_injector.wiring import Provide, inject
from loguru import logger

import app.keyboards.inline_keyboard as kb
from app.core.container import Container
from app.loader import bot, dp
from app.models.application import Application
from app.services.application import ApplicationService
from app.states.base import BaseStates
from app.states.tgbot_states import AddObjAdm
from app.utils import const, get_data
from app.utils.const import (DATA_OBJ, ERROR_NUMBERS, FIO, LOAD_DOC,
                             NAME_OBJECT, R_TYPE, ROLE, STORAGE_ERROR,
                             STORAGE_NAME, STORAGE_OBJ, TITUL)


async def get_note(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(field_one=message.document.file_id)
        await message.answer(NAME_OBJECT,
                             reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.obj_name)
    else:
        await message.answer(LOAD_DOC)
        await state.set_state(AddObjAdm.note)


async def get_obj_name(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if not message.text.isdigit():
            await state.update_data(field_two=message.text)
            await message.answer(TITUL, reply_markup=kb.exit_kb())
            await state.set_state(AddObjAdm.title)
        else:
            await message.answer(ERROR_NUMBERS)
            await state.set_state(AddObjAdm.obj_name)
    else:
        await message.answer(NAME_OBJECT)
        await state.set_state(AddObjAdm.obj_name)


async def get_title(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    new_kb = kb.storage_kb().add(kb.exit_button)
    await message.answer(STORAGE_OBJ,
                         reply_markup=new_kb)
    await state.set_state(AddObjAdm.new_or_exist)


async def get_new_or_exist(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    if query.data == 'exist_storage':
        await state.update_data(field_four='существующий')
        await query.message.answer('Укажите склад: ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.storage)
    elif query.data == 'new_storage':
        await state.update_data(field_four='новый')
        await query.message.answer(DATA_OBJ,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.storage)


@inject
async def get_storage(message: types.Message, state: FSMContext,
                      application: ApplicationService = Provide[Container.application_service]):
    if message.content_type == 'text':
        if not message.text.isdigit():
            await state.update_data(field_five=message.text)
            new_kb = kb.sure().add(kb.exit_button)
            data = await state.get_data()
            if 'admin' not in data:
                await get_data.send_data(message=message, state=state)
                await message.answer(const.SURE,
                                     reply_markup=new_kb)
                await state.set_state(AddObjAdm.sure)
            else:
                if 'field_one' in data:
                    black_list = {'admin'}
                    new_data = {key: val for key, val in data.items() if key not in black_list}
                    unused = ['field_six', 'field_seven', 'field_eight', 'field_nine']
                    for i in unused:
                        new_data[i] = None
                    logger.info(new_data)
                    await application.update(data['admin'], obj_in=new_data)
                    await message.answer(const.CHANGE_SUCCESS)
                    ticket = await application.get(data['admin'])
                    await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
                    await state.finish()
                else:
                    await application.update(data['admin'],
                                            obj_in={'application_status': Application.ApplicationStatus.in_work,
                                                    'field_four': data['field_four'],
                                                    'field_five': data['field_five']})
                    await message.answer(const.CHANGE_SUCCESS)
                    ticket = await application.get(data['admin'])
                    await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
                    await state.finish()
        else:
            await message.answer(STORAGE_ERROR)
            await state.set_state(AddObjAdm.storage)
    else:
        await message.answer(STORAGE_NAME)
        await state.set_state(AddObjAdm.storage)


@dp.callback_query_handler(state=AddObjAdm.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await state.update_data(change='name')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    elif query.data == '2':
        await state.update_data(change='role')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(AddObjAdm.edit)
    elif query.data == '3':
        data = await state.get_data()
        if 'admin' in data:
            await bot.delete_message(query.message.chat.id,
                                     query.message.message_id)
            await query.message.answer(text=FIO, reply_markup=kb.exit_kb())
            await state.set_state(BaseStates.fio)
        else:
            await bot.delete_message(
                query.message.chat.id, query.message.message_id)
            await state.finish()
            await query.message.answer(text=FIO, reply_markup=kb.exit_kb())
            await state.set_state(BaseStates.fio)
    elif query.data == '4':
        await state.update_data(change='note')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    elif query.data == '5':
        await state.update_data(change='obj_name')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer(NAME_OBJECT,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='title')
        await query.message.answer(
            TITUL, reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.storage_kb().add(kb.exit_button)
        await query.message.answer(STORAGE_OBJ,
                                   reply_markup=new_kb)
        await state.set_state(AddObjAdm.new_or_exist)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage')
        await query.message.answer(DATA_OBJ,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    await query.answer()


@inject
async def edit(message: types.Message, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'note':
        await state.update_data(field_one=message.document.file_id)
    elif point == 'obj_name':
        await state.update_data(field_two=message.text)
    elif point == 'title':
        await state.update_data(field_three=message.text)
    elif point == 'storage':
        await state.update_data(field_five=message.text)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE,
                             reply_markup=new_kb)
        await state.set_state(AddObjAdm.sure)
    else:
        if 'name' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'name': data['name']})
        elif 'field_one' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_one': data['field_one']})
        elif 'field_two' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_two': data['field_two']})
        elif 'field_three' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_three': data['field_three']})
        elif 'field_four' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_four': data['field_four']})
        elif 'field_five' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_five': data['field_five']})
        await message.answer(const.CHANGE_SUCCESS)
        ticket = await application.get(data['admin'])
        await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
        await state.finish()


@inject
async def get_role(query: types.CallbackQuery, state: FSMContext,
                   application: ApplicationService = Provide[Container.application_service]):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(query=query, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE,
                                   reply_markup=new_kb)
        await state.set_state(AddObjAdm.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'role': data['role']})
        await query.message.answer(const.CHANGE_SUCCESS)
        ticket = await application.get(data['admin'])
        await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
        await state.finish()


def register(dp: Dispatcher):
    dp.register_callback_query_handler(correct, state=AddObjAdm.sure)
    dp.register_callback_query_handler(get_new_or_exist, state=AddObjAdm.new_or_exist)
    dp.register_message_handler(
        get_note, state=AddObjAdm.note, content_types=['any'])
    dp.register_message_handler(get_obj_name, state=AddObjAdm.obj_name, content_types=['any'])
    dp.register_message_handler(get_title, state=AddObjAdm.title)
    dp.register_message_handler(get_storage, state=AddObjAdm.storage, content_types=['any'])
    dp.register_message_handler(edit,
                                state=AddObjAdm.edit,
                                content_types=['text', 'document'])
    dp.register_callback_query_handler(get_role, state=AddObjAdm.edit)