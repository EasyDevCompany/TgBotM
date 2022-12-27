from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from states.tgbot_states import EditMoveAdm
from loader import dp, bot
from utils import const


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
            'Подробное описание редактирования перемещения: ',
            reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.description)
    else:
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        await query.message.answer('Введите причину: ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditMoveAdm.another_reason)


async def get_another_reason(message: types.Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await message.answer('Подробное описание редактирования перемещения: ',
                         reply_markup=kb.exit_kb())
    await state.set_state(EditMoveAdm.description)


async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    print(await state.get_data())


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
