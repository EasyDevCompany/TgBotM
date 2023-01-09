import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import AddViewWork
from app.utils import const, get_data
from app.utils.const import EDIT_WORK, EDIT_SORT, EDIT_SUBSISTEMS, FIO, ROLE, R_TYPE


async def get_sub_object(message: types.Message, state: FSMContext):
    await state.update_data(field_one=message.text)
    await message.answer(EDIT_WORK,
                         reply_markup=kb.exit_kb())
    await state.set_state(AddViewWork.type_work)


async def get_type_work(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    await message.answer(EDIT_SORT,
                         reply_markup=kb.exit_kb())
    await state.set_state(AddViewWork.sort)


async def get_sort(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    new_kb = kb.add_subsystem_kb().add(kb.exit_button)
    await message.answer(
        EDIT_SUBSISTEMS,
        reply_markup=new_kb)
    await state.set_state(AddViewWork.subsystems)


async def get_subsystems(query: types.CallbackQuery, state: FSMContext):
    new_kb = kb.accept().add(kb.exit_button)
    data = await state.get_data()
    if query.data != 'accept' and 'field_four' not in data:
        await state.update_data(field_four=query.data)
        data = await state.get_data()
        msg = await query.message.answer(data['field_four'], reply_markup=new_kb)
        await state.update_data(message_id=msg.message_id)
    elif query.data != 'accept':
        data = await state.get_data()
        await state.update_data(field_four=data['field_four'] + ', ' + query.data)
        new_data = await state.get_data()
        await bot.edit_message_text(new_data['field_four'],
                                    query.message.chat.id, new_data['message_id'], reply_markup=new_kb)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await get_data.send_data(query=query, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE,
                                   reply_markup=new_kb)
        await state.set_state(AddViewWork.sure)
    await query.answer()


async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(AddViewWork.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(AddViewWork.edit)
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
        await state.update_data(change='sub_object')
        await query.message.answer(
            const.SELECT_SUBOBJECT, reply_markup=kb.exit_kb())
        await state.set_state(AddViewWork.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='type_work')
        await query.message.answer(EDIT_WORK,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddViewWork.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='sort')
        await query.message.answer(EDIT_SORT,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddViewWork.edit)
    elif query.data == '7':
        await state.update_data(field_four='')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.add_subsystem_kb().add(kb.exit_button)
        await query.message.answer(
            EDIT_SUBSISTEMS,
            reply_markup=new_kb)
        await state.set_state(AddViewWork.subsystems_edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'type_work':
        await state.update_data(field_two=message.text)
    elif point == 'name':
        await state.update_data(name=message.text)
    elif point == 'sub_object':
        await state.update_data(field_one=message.text)
    elif point == 'sort':
        await state.update_data(field_three=message.text)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(AddViewWork.sure)


async def get_subsystems_edit(query: types.CallbackQuery, state: FSMContext):
    new_kb = kb.accept().add(kb.exit_button)
    data = await state.get_data()
    if query.data != 'accept' and data['field_four'] == '':
        await state.update_data(field_four=query.data)
        data = await state.get_data()
        msg = await query.message.answer(data['field_four'], reply_markup=new_kb)
        await state.update_data(message_id=msg.message_id)
    elif query.data != 'accept':
        data = await state.get_data()
        await state.update_data(field_four=data['field_four'] + ', ' + query.data)
        new_data = await state.get_data()
        await bot.edit_message_text(new_data['field_four'],
                                    query.message.chat.id,
                                    new_data['message_id'], reply_markup=new_kb)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await get_data.send_data(query=query, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE,
                                   reply_markup=new_kb)
        await state.set_state(AddViewWork.sure)
    await query.answer()


async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddViewWork.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_sub_object, state=AddViewWork.sub_object)
    dp.register_message_handler(get_type_work, state=AddViewWork.type_work)
    dp.register_message_handler(get_sort, state=AddViewWork.sort)
    dp.register_callback_query_handler(get_subsystems,
                                       state=AddViewWork.subsystems)
    dp.register_message_handler(edit, state=AddViewWork.edit)
    dp.register_callback_query_handler(correct, state=AddViewWork.sure)
    dp.register_callback_query_handler(get_role, state=AddViewWork.edit)
    dp.register_callback_query_handler(get_subsystems_edit, state=AddViewWork.subsystems_edit)
