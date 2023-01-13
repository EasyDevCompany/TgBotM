import re

import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import OpenAcs
from app.utils import const, get_data
from app.utils.const import LOAD_DOC, FIO_EMPLOYEE, ACCESS, FIO, ROLE, R_TYPE


async def get_note(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(field_one=message.document.file_id)
        await message.answer(FIO_EMPLOYEE, reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.staff_name)
    else:
        await message.answer(LOAD_DOC)
        await state.set_state(OpenAcs.note)


async def get_name(message: types.Message, state: FSMContext):
    if bool(re.search(
            r'\b[\u0401\u0451\u0410-\u044f]+\s+[\u0401\u0451\u0410-\u044f]+\s+[\u0401\u0451\u0410-\u044f]+\b',
            message.text, re.IGNORECASE)
            ):
        await state.update_data(field_two=message.text)
        await message.answer(ACCESS,
                             reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.what_acs)
    else:
        await message.answer(FIO)
        await state.set_state(OpenAcs.staff_name)


async def get_acs(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    await message.answer(const.FOR_WHAT_ACS, reply_markup=kb.exit_kb())
    await state.set_state(OpenAcs.for_what)


async def get_reason(message: types.Message, state: FSMContext):
    await state.update_data(field_four=message.text)
    await get_data.send_data(message=message, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(OpenAcs.sure)


async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(OpenAcs.edit)
    elif query.data == '3':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='request_type')
        new_kb = kb.main_kb().add(kb.exit_button)
        await query.message.answer(R_TYPE,
                                   reply_markup=new_kb)
        await state.set_state(BaseStates.request_type)
    elif query.data == '4':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='note')
        await query.message.answer(
            const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='staff_name')
        await query.message.answer(
            FIO_EMPLOYEE, reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='what_acs')
        await query.message.answer(ACCESS,
                                   reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='for_what')
        await query.message.answer(
            const.FOR_WHAT_ACS, reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'note':
        await state.update_data(field_one=message.document.file_id)
    elif point == 'staff_name':
        await state.update_data(field_two=message.text)
    elif point == 'what_acs':
        await state.update_data(field_three=message.text)
    elif point == 'for_what':
        await state.update_data(field_four=message.text)
    await get_data.send_data(message=message, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(OpenAcs.sure)


async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(OpenAcs.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(
        get_note, state=OpenAcs.note, content_types=['any'])
    dp.register_message_handler(get_name, state=OpenAcs.staff_name)
    dp.register_message_handler(get_acs, state=OpenAcs.what_acs)
    dp.register_message_handler(get_reason, state=OpenAcs.for_what)
    dp.register_message_handler(edit,
                                state=OpenAcs.edit,
                                content_types=['text', 'document'])
    dp.register_callback_query_handler(correct, state=OpenAcs.sure)
    dp.register_callback_query_handler(get_role, state=OpenAcs.edit)

