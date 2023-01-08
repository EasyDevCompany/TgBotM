import keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.base import BaseStates
from states.tgbot_states import ChangeStatus
from utils import const, get_data


async def get_note(message: types.Message, state: FSMContext):
    await state.update_data(field_one=message.document.file_id)
    await message.answer('Укажите номер заявки',
                         reply_markup=kb.exit_kb())
    await state.set_state(ChangeStatus.number_bid)


async def get_number_bid(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    await message.answer('Укажите какой статус необходимо поставить заявке',
                         reply_markup=kb.exit_kb())
    await state.set_state(ChangeStatus.status_in_bid)


async def get_status_in_bid(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    await get_data.send_data(message=message, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(ChangeStatus.sure)


@dp.callback_query_handler(state=ChangeStatus.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(ChangeStatus.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(ChangeStatus.edit)
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
        await state.update_data(change='note')
        await query.message.answer(
            const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(ChangeStatus.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number')
        await query.message.answer('Укажите номер заявки',
                                   reply_markup=kb.exit_kb())
        await state.set_state(ChangeStatus.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='status')
        await query.message.answer(
            'Укажите, какой статус необходимо поставить заявке',
            reply_markup=kb.exit_kb())
        await state.set_state(ChangeStatus.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'note':
        await state.update_data(field_one=message.document.file_id)
    elif point == 'number':
        await state.update_data(field_two=message.text)
    elif point == 'status':
        await state.update_data(field_three=message.text)
    await get_data.send_data(message=message, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(ChangeStatus.sure)


@dp.callback_query_handler(state=ChangeStatus.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    await get_data.send_data(query=query, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(ChangeStatus.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_note,
                                state=ChangeStatus.note,
                                content_types=['document'])
    dp.register_message_handler(get_number_bid, state=ChangeStatus.number_bid)
    dp.register_message_handler(get_status_in_bid,
                                state=ChangeStatus.status_in_bid)
    dp.register_message_handler(edit, state=ChangeStatus.edit,
                                content_types=['text', 'document'])
