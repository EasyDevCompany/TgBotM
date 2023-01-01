import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot, dp
from app.states.base import BaseStates
from app.states.tgbot_states import EditMoveAdm
from app.utils import const, get_data


async def get_note(message: types.Message, state: FSMContext):
    await state.update_data(note=message.document.file_id)
    await message.answer(
        'Укажите номер заявки, если перемещение по заявке',
        reply_markup=kb.exit_kb())
    await state.set_state(EditMoveAdm.number_ticket)


async def get_ticket(message: types.Message, state: FSMContext):
    await state.update_data(number_ticket=message.text)
    await message.answer('Укажите номер накладной', reply_markup=kb.exit_kb())
    await state.set_state(EditMoveAdm.number_invoice)


async def get_invoice(message: types.Message, state: FSMContext):
    await state.update_data(number_invoice=message.text)
    await message.answer(
        'Укажите исходящий склад\n(откуда было отправлено)',
        reply_markup=kb.exit_kb())
    await state.set_state(EditMoveAdm.storage_out)


async def storage_out(message: types.Message, state: FSMContext):
    await state.update_data(storage_out=message.text)
    await message.answer(
        'Укажите входящий склад\n(куда было отправлено)',
        reply_markup=kb.exit_kb())
    await state.set_state(EditMoveAdm.storage_in)


async def storage_in(message: types.Message, state: FSMContext):
    await state.update_data(storage_in=message.text)
    new_kb = kb.status_kb().add(kb.exit_button)
    await message.answer('Укажите статус перемещения', reply_markup=new_kb)
    await state.set_state(EditMoveAdm.status)


@dp.callback_query_handler(state=EditMoveAdm.status)
async def get_status(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(status=query.data)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    new_kb = kb.reason_kb().add(kb.exit_button)
    await query.message.answer('Причина корректировки', reply_markup=new_kb)
    await state.set_state(EditMoveAdm.reason)


@dp.callback_query_handler(state=EditMoveAdm.reason)
async def get_reason(query: types.CallbackQuery, state: FSMContext):
    if query.data != 'Другое':
        await state.update_data(reason=query.data)
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        await query.message.answer(
            const.DESCRIPTION_MOVE,
            reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.description)
    else:
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        await query.message.answer('Введите причину: ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.another_reason)


async def get_another_reason(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'description' not in data:
        await state.update_data(reason=message.text)
        await message.answer(const.DESCRIPTION_MOVE,
                             reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.description)
    else:
        await state.update_data(reason=message.text)
        await get_data.send_data(message=message, state=state)
        await message.answer(const.SURE,
                             reply_markup=kb.sure())
        await state.set_state(EditMoveAdm.sure)


async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=kb.sure())
    await state.set_state(EditMoveAdm.sure)


@dp.callback_query_handler(state=EditMoveAdm.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(EditMoveAdm.edit)
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
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_ticket')
        await query.message.answer(
            'Укажите номер заявки, если перемещение по заявке',
            reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_invoice')
        await query.message.answer('Укажите номер накладной',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage_out')
        await query.message.answer(
            'Укажите исходящий склад\n(откуда было отправлено)',
            reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage_in')
        await query.message.answer(
            'Укажите входящий склад\n(куда было отправлено)',
            reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.edit)
    elif query.data == '9':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='status')
        new_kb = kb.status_kb().add(kb.exit_button)
        await query.message.answer('Укажите статус перемещения',
                                   reply_markup=new_kb)
        await state.set_state(EditMoveAdm.status_edit)
    elif query.data == '10':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='reason')
        new_kb = kb.reason_kb().add(kb.exit_button)
        await query.message.answer(
            'Причина корректировки', reply_markup=new_kb)
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
        await state.update_data(note=message.document.file_id)
    elif point == 'number_ticket':
        await state.update_data(number_ticket=message.text)
    elif point == 'number_invoice':
        await state.update_data(number_invoice=message.text)
    elif point == 'storage_out':
        await state.update_data(storage_out=message.text)
    elif point == 'storage_in':
        await state.update_data(storage_in=message.text)
    elif point == 'description':
        await state.update_data(description=message.text)
    print(await state.get_data())
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(EditMoveAdm.sure)


@dp.callback_query_handler(state=EditMoveAdm.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(EditMoveAdm.sure)


@dp.callback_query_handler(state=EditMoveAdm.status_edit)
async def get_status_edit(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(status=query.data)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(EditMoveAdm.sure)


@dp.callback_query_handler(state=EditMoveAdm.reason_edit)
async def get_reason_edit(query: types.CallbackQuery, state: FSMContext):
    if query.data != 'Другое':
        await state.update_data(reason=query.data)
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE, reply_markup=new_kb)
        await get_data.send_data(query=query, state=state)
        await state.set_state(EditMoveAdm.sure)
    else:
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        await query.message.answer('Введите причину: ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.another_reason)


def register(dp: Dispatcher):
    dp.register_message_handler(get_note,
                                state=EditMoveAdm.note,
                                content_types=['document'])
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
