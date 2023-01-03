import keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.base import BaseStates
from states.tgbot_states import UpdateSubObject
from utils import const, get_data


async def get_sub_object(message: types.Message, state: FSMContext):
    await state.update_data(sub_obj=['Подобъект', message.text])
    await message.answer('Укажите, что именно необходимо отредактировать',
                         reply_markup=kb.exit_kb())
    await state.set_state(UpdateSubObject.select_type_work)


async def get_type_work(message: types.Message, state: FSMContext):
    await state.update_data(type_work=['Что редактировать', message.text])
    await get_data.send_data(message=message, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(UpdateSubObject.sure)


@dp.callback_query_handler(state=UpdateSubObject.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(UpdateSubObject.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(UpdateSubObject.edit)
    elif query.data == '3':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='request_type')
        new_kb = kb.main_kb().add(kb.exit_button)
        await query.message.answer('Выберите тип запроса',
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
        await query.message.answer('Укажите наименование вида работ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(UpdateSubObject.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=['ФИО', message.text])
    elif point == 'sub_obj':
        await state.update_data(sub_obj=['Подобъект', message.text])
    elif point == 'type_work':
        await state.update_data(type_work=['Что редактировать', message.text])
    await get_data.send_data(message=message, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(UpdateSubObject.sure)


@dp.callback_query_handler(state=UpdateSubObject.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=['Роль', query.data])
    await get_data.send_data(query=query, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(UpdateSubObject.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_sub_object,
                                state=UpdateSubObject.select_subobject)
    dp.register_message_handler(get_type_work,
                                state=UpdateSubObject.select_type_work)
    dp.register_message_handler(edit, state=UpdateSubObject.edit)
