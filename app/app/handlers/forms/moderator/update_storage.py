import keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.base import BaseStates
from states.tgbot_states import UpdateStorage
from utils import const, get_data


async def get_number_bid(message: types.Message, state: FSMContext):
    await state.update_data(field_one=message.text)
    await message.answer('Укажите новый склад доставки',
                         reply_markup=kb.exit_kb())
    await state.set_state(UpdateStorage.new_storage)


async def get_new_storage(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    await message.answer('Укажите контактное лицо (Ф.И.О.)',
                         reply_markup=kb.exit_kb())
    await state.set_state(UpdateStorage.contact_fio)


async def get_fio(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    await message.answer(
        'Укажите адрес актуального склада (на который нужно поменять)',
        reply_markup=kb.exit_kb())
    await state.set_state(UpdateStorage.address_storage)


async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(field_four=message.text)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=kb.sure())
    await state.set_state(UpdateStorage.sure)


@dp.callback_query_handler(state=UpdateStorage.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(UpdateStorage.edit)
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
        await state.update_data(change='number_bid')
        await query.message.answer(
            const.NUMBER_BID, reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='new_storage')
        await query.message.answer('Укажите новый склад доставки',
                                   reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='contact_fio')
        await query.message.answer('Укажите контактное лицо (Ф.И.О.)',
                                   reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='address')
        await query.message.answer(
            'Укажите адрес актуального склада (на который нужно поменять)',
            reply_markup=kb.exit_kb())
        await state.set_state(UpdateStorage.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
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
    await get_data.send_data(message=message, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(UpdateStorage.sure)


@dp.callback_query_handler(state=UpdateStorage.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    await get_data.send_data(query=query, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(UpdateStorage.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_number_bid, state=UpdateStorage.number_bid)
    dp.register_message_handler(get_new_storage,
                                state=UpdateStorage.new_storage)
    dp.register_message_handler(get_fio, state=UpdateStorage.contact_fio)
    dp.register_message_handler(get_address,
                                state=UpdateStorage.address_storage)
    dp.register_message_handler(edit, state=UpdateStorage.edit)
