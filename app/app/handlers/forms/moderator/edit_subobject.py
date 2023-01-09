import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import UpdateSubObject
from app.utils import const, get_data
from app.utils.const import WHAT_EDIT_EXACTLY, FIO, ROLE, R_TYPE, EDIT_WORK


async def get_sub_object(message: types.Message, state: FSMContext):
    await state.update_data(field_one=message.text)
    await message.answer(WHAT_EDIT_EXACTLY,
                         reply_markup=kb.exit_kb())
    await state.set_state(UpdateSubObject.select_type_work)


async def get_type_work(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(UpdateSubObject.sure)


async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(UpdateSubObject.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(UpdateSubObject.edit)
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
        await state.update_data(change='sub_obj')
        await query.message.answer(
            const.SELECT_SUBOBJECT, reply_markup=kb.exit_kb())
        await state.set_state(UpdateSubObject.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='type_work')
        await query.message.answer(EDIT_WORK,
                                   reply_markup=kb.exit_kb())
        await state.set_state(UpdateSubObject.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'sub_obj':
        await state.update_data(field_one=message.text)
    elif point == 'type_work':
        await state.update_data(field_two=message.text)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(UpdateSubObject.sure)


async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(UpdateSubObject.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_sub_object,
                                state=UpdateSubObject.select_subobject)
    dp.register_message_handler(get_type_work,
                                state=UpdateSubObject.select_type_work)
    dp.register_message_handler(edit, state=UpdateSubObject.edit)
    dp.register_callback_query_handler(correct, state=UpdateSubObject.sure)
    dp.register_callback_query_handler(get_role, state=UpdateSubObject.edit)
