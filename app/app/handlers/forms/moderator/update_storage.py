import re

import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import UpdateStorage
from app.utils import const, get_data
from app.utils.const import EDIT_NEW_STORAGE, REQUEST_NUMBER, EDIT_CONTACT_NAME, EDIT_ADDRESS, ERROR_CONTACT, \
    ADDRESS_ERROR, FIO, ROLE
from dependency_injector.wiring import inject, Provide
from app.services.application import ApplicationService
from app.core.container import Container
from app.models.application import Application
from loguru import logger


async def get_number_bid(message: types.Message, state: FSMContext):
    if not message.text.isalpha():
        await state.update_data(field_one=message.text)
        await message.answer(EDIT_NEW_STORAGE,
                             reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.new_storage)
    else:
        await message.answer(REQUEST_NUMBER)
        await state.set_state(UpdateStorage.number_bid)


async def get_new_storage(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    await message.answer(EDIT_CONTACT_NAME,
                         reply_markup=kb.exit_kb())
    await state.set_state(UpdateStorage.contact_fio)


async def get_fio(message: types.Message, state: FSMContext):
    if bool(re.search(
            r'\b[\u0401\u0451\u0410-\u044f]+\s+[\u0401\u0451\u0410-\u044f]+\s+[\u0401\u0451\u0410-\u044f]+\b',
            message.text, re.IGNORECASE)
            ):
        await state.update_data(field_three=message.text)
        await message.answer(
            EDIT_ADDRESS,
            reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.address_storage)
    else:
        await state.set_state(UpdateStorage.contact_fio)
        await message.answer(ERROR_CONTACT)


@inject
async def get_address(message: types.Message, state: FSMContext,
                      application: ApplicationService = Provide[Container.application_service]):
    if not message.text.isdigit():
        await state.update_data(field_four=message.text)
        data = await state.get_data()
        if 'admin' not in data:
            await get_data.send_data(message=message, state=state)
            new_kb = kb.sure().add(kb.exit_button)
            await message.answer(const.SURE, reply_markup=new_kb)
            await state.set_state(UpdateStorage.sure)
        else:
            black_list = {'admin'}
            new_data = {key: val for key, val in data.items() if key not in black_list}
            unused = ['field_five', 'field_six', 'field_seven', 'field_eight', 'field_nine']
            for i in unused:
                new_data[i] = None
            logger.info(new_data)
            await application.update(data['admin'], obj_in=new_data)
            await message.answer(const.CHANGE_SUCCESS)
            await state.finish()
    else:
        await message.answer(ADDRESS_ERROR)
        await state.set_state(UpdateStorage.address_storage)


async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(UpdateStorage.edit)
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
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_bid')
        await query.message.answer(
            const.NUMBER_BID, reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='new_storage')
        await query.message.answer(EDIT_NEW_STORAGE,
                                   reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='contact_fio')
        await query.message.answer(EDIT_CONTACT_NAME,
                                   reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='address')
        await query.message.answer(
            EDIT_ADDRESS,
            reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    await query.answer()


@inject
async def edit(message: types.Message, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'number_bid':
        await state.update_data(field_one=message.text)
    elif point == 'new_storage':
        await state.update_data(field_two=message.text)
    elif point == 'contact_fio':
        await state.update_data(field_three=message.text)
    elif point == 'address':
        await state.update_data(field_four=message.text)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(UpdateStorage.sure)
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
        await message.answer(const.CHANGE_SUCCESS)
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
        await state.set_state(UpdateStorage.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'role': data['role']})
        await query.message.answer(const.CHANGE_SUCCESS)
        await state.finish()


def register(dp: Dispatcher):
    dp.register_message_handler(get_number_bid, state=UpdateStorage.number_bid)
    dp.register_message_handler(get_new_storage,
                                state=UpdateStorage.new_storage)
    dp.register_message_handler(get_fio, state=UpdateStorage.contact_fio)
    dp.register_message_handler(get_address,
                                state=UpdateStorage.address_storage)
    dp.register_message_handler(edit, state=UpdateStorage.edit)
    dp.register_callback_query_handler(correct, state=UpdateStorage.sure)
    dp.register_callback_query_handler(get_role, state=UpdateStorage.edit)