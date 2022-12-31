import keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.base import BaseStates
from states.tgbot_states import AdjInv
from utils import const, get_data


async def get_note(message: types.Message, state: FSMContext):
    await state.update_data(note=message.document.file_id)
    await message.answer('Укажите номер накладного документа',
                         reply_markup=kb.exit_kb())
    await state.set_state(AdjInv.number_invoice)


async def get_number_invoice(message: types.Message, state: FSMContext):
    await state.update_data(number_invoice=message.text)
    await message.answer('Укажите номер заявки',
                         reply_markup=kb.exit_kb())
    await state.set_state(AdjInv.number_ticket)


async def get_number_ticket(message: types.Message, state: FSMContext):
    await state.update_data(number_ticket=message.text)
    new_kb = kb.adj_inv().add(kb.exit_button)
    await message.answer('Выберите, что необходимо отредактировать в накладной',
                         reply_markup=new_kb)
    await state.set_state(AdjInv.what_edit)


@dp.callback_query_handler(state=AdjInv.what_edit)
async def get_what_edit(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(what_edit=query.data)
    await query.message.answer('Укажите уточняющую информацию',
                               reply_markup=kb.exit_kb())
    await state.set_state(AdjInv.description)


async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(AdjInv.sure)


@dp.callback_query_handler(state=AdjInv.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(AdjInv.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(AdjInv.edit)
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
        await state.set_state(AdjInv.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_invoice')
        await query.message.answer('Укажите номер накладного документа',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AdjInv.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_ticket')
        await query.message.answer('Укажите номер заявки',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AdjInv.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='what_edit')
        await query.message.answer(
            'Выберите, что необходимо отредактировать в накладной',
            reply_markup=kb.adj_inv())
        await state.set_state(AdjInv.what_edit_correct)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='description')
        await query.message.answer('Укажите уточняющую информацию',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AdjInv.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'note':
        await state.update_data(note=message.document.file_id)
    elif point == 'number_invoice':
        await state.update_data(number_invoice=message.text)
    elif point == 'number_ticket':
        await state.update_data(number_ticket=message.text)
    elif point == 'description':
        await state.update_data(description=message.text)
    print(await state.get_data())
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(AdjInv.sure)


@dp.callback_query_handler(state=AdjInv.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    await get_data.send_data(query=query, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AdjInv.sure)


@dp.callback_query_handler(state=AdjInv.what_edit_correct)
async def get_what_edit_correct(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(what_edit=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(AdjInv.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_note,
                                state=AdjInv.note,
                                content_types=['document'])
    dp.register_message_handler(get_number_invoice,
                                state=AdjInv.number_invoice)
    dp.register_message_handler(get_number_ticket,
                                state=AdjInv.number_ticket)
    dp.register_message_handler(get_description, state=AdjInv.description)
    dp.register_message_handler(edit, state=AdjInv.edit,
                                content_types=['text', 'document'])
