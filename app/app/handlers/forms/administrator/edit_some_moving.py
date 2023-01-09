import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import EditMoveAdm
from app.utils import const, get_data
from app.utils.const import NUMBER_REQUEST_IF, LOAD_DOC, INVOICE_NUMBER, R_NUMBER_ERROR, OUTGOING_STORAGE, \
    OUTGOING_STORAGE_INCOME, STATUS_GOING, REASON, FIO, ROLE, R_TYPE


async def get_note(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(field_one=message.document.file_id)
        await message.answer(NUMBER_REQUEST_IF, reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.number_ticket)
    else:
        await message.answer(LOAD_DOC)
        await state.set_state(EditMoveAdm.note)


async def get_ticket(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(field_two=message.text)
        await message.answer(INVOICE_NUMBER, reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.number_invoice)
    else:
        await message.answer(R_NUMBER_ERROR)
        await state.set_state(EditMoveAdm.number_ticket)


async def get_invoice(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    await message.answer(OUTGOING_STORAGE, reply_markup=kb.exit_kb())
    await state.set_state(EditMoveAdm.storage_out)


async def storage_out(message: types.Message, state: FSMContext):
    await state.update_data(field_four=message.text)
    await message.answer(OUTGOING_STORAGE_INCOME, reply_markup=kb.exit_kb())
    await state.set_state(EditMoveAdm.storage_in)


async def storage_in(message: types.Message, state: FSMContext):
    await state.update_data(field_five=message.text)
    new_kb = kb.status_kb().add(kb.exit_button)
    await message.answer(STATUS_GOING, reply_markup=new_kb)
    await state.set_state(EditMoveAdm.status)


async def get_status(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(field_six=query.data)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    new_kb = kb.reason_kb().add(kb.exit_button)
    await query.message.answer(const.REASON, reply_markup=new_kb)
    await state.set_state(EditMoveAdm.reason)


async def get_reason(query: types.CallbackQuery, state: FSMContext):
    if query.data != 'Другое':
        await state.update_data(field_seven=query.data)
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        await query.message.answer(
            const.DESCRIPTION_MOVE,
            reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.description)
    else:
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        await query.message.answer(REASON,
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.another_reason)


async def get_another_reason(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'description' not in data:
        await state.update_data(field_seven=message.text)
        await message.answer(const.DESCRIPTION_MOVE,
                             reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.description)
    else:
        await state.update_data(reason=[const.REASON, message.text])
        await get_data.send_data(message=message, state=state)
        await message.answer(const.SURE,
                             reply_markup=kb.sure())
        await state.set_state(EditMoveAdm.sure)


async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(field_eight=message.text)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=kb.sure())
    await state.set_state(EditMoveAdm.sure)


async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(EditMoveAdm.edit)
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
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_ticket')
        await query.message.answer(NUMBER_REQUEST_IF, reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_invoice')
        await query.message.answer(INVOICE_NUMBER,
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage_out')
        await query.message.answer(
            OUTGOING_STORAGE,
            reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage_in')
        await query.message.answer(
            OUTGOING_STORAGE_INCOME,
            reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '9':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='status')
        new_kb = kb.status_kb().add(kb.exit_button)
        await query.message.answer(STATUS_GOING,
                                   reply_markup=new_kb)
        await state.set_state(EditMoveAdm.status_edit)
    elif query.data == '10':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='reason')
        new_kb = kb.reason_kb().add(kb.exit_button)
        await query.message.answer(
            const.REASON, reply_markup=new_kb)
        await state.set_state(EditMoveAdm.reason_edit)
    elif query.data == '11':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='description')
        await query.message.answer(
            const.DESCRIPTION_MOVE,
            reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'note':
        await state.update_data(field_one=message.document.file_id)
    elif point == 'number_ticket':
        await state.update_data(number_ticket=['Номер заявки', message.text])
    elif point == 'number_invoice':
        await state.update_data(field_three=message.text)
    elif point == 'storage_out':
        await state.update_data(field_four=message.text)
    elif point == 'storage_in':
        await state.update_data(field_five=message.text)
    elif point == 'description':
        await state.update_data(field_eight=['Описание', message.text])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(EditMoveAdm.sure)


async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(EditMoveAdm.sure)


async def get_status_edit(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(field_six=query.data)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(EditMoveAdm.sure)


async def get_reason_edit(query: types.CallbackQuery, state: FSMContext):
    if query.data != 'Другое':
        await state.update_data(field_seven=query.data)
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE, reply_markup=new_kb)
        await get_data.send_data(query=query, state=state)
        await state.set_state(EditMoveAdm.sure)
    else:
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        await query.message.answer(REASON,
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.another_reason)


def register(dp: Dispatcher):
    dp.register_message_handler(get_note,
                                state=EditMoveAdm.note,
                                content_types=['any'])
    dp.register_message_handler(get_ticket, state=EditMoveAdm.number_ticket)
    dp. register_message_handler(get_invoice, state=EditMoveAdm.number_invoice)
    dp.register_message_handler(storage_out, state=EditMoveAdm.storage_out)
    dp.register_message_handler(storage_in, state=EditMoveAdm.storage_in)
    dp.register_message_handler(get_another_reason,
                                state=EditMoveAdm.another_reason)
    dp.register_message_handler(get_description, state=EditMoveAdm.description)
    dp.register_message_handler(edit,
                                state=EditMoveAdm.edit,
                                content_types=['text', 'document'])
    dp.register_callback_query_handler(get_status, state=EditMoveAdm.status)
    dp.register_callback_query_handler(get_reason, state=EditMoveAdm.reason)
    dp.register_callback_query_handler(correct, state=EditMoveAdm.sure)
    dp.register_callback_query_handler(get_role, state=EditMoveAdm.edit)
    dp.register_callback_query_handler(get_status_edit, state=EditMoveAdm.status_edit)
    dp.register_callback_query_handler(get_reason_edit, state=EditMoveAdm.reason_edit)
