from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from states.tgbot_states import EditShpmnt
from loader import dp, bot
from utils import const
from utils import const_edit_shpmnt as text


@dp.callback_query_handler(text='skip', state=EditShpmnt.extra_files)
async def skip(query: types. CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    print(await state.get_data())
    await query.answer()


async def get_note(message: types.Message, state: FSMContext):
    await state.update_data(note=message.document.file_id)
    await message.answer(
        'Укажите номер заявки: ', reply_markup=kb.exit_kb())
    await state.set_state(EditShpmnt.number_ticket)


async def get_ticket(message: types.Message, state: FSMContext):
    await state.update_data(number_ticket=message.text)
    await message.answer(text.NUM_INVOICE, reply_markup=kb.exit_kb())
    await state.set_state(EditShpmnt.number_invoice)


async def get_invoice(message: types.Message, state: FSMContext):
    await state.update_data(number_invoice=message.text)
    await message.answer(
        'Укажите входящий склад(на который приняли поставку): ',
        reply_markup=kb.exit_kb())
    await state.set_state(EditShpmnt.storage)


async def get_storage(message: types.Message, state: FSMContext):
    await state.update_data(storage=message.text)
    new_kb = kb.what_edit().add(kb.exit_button)
    await message.answer('Что необходимо отредактировать в поставке:',
                         reply_markup=new_kb)
    await state.set_state(EditShpmnt.what_edit)


@dp.callback_query_handler(state=EditShpmnt.what_edit)
async def get_changes(query: types.CallbackQuery, state: FSMContext, ):
    if query.data != 'Другое':
        await state.update_data(what_edit=query.data)
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer('Подробное описание ошибки в поставке:',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.description)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer('Что редактируем: ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.another_what_edit)


async def get_another_changes(message: types.Message, state: FSMContext):
    await state.update_data(what_edit=message.text)
    await message.answer('Подробное описание ошибки в поставке:',
                         reply_markup=kb.exit_kb())
    await state.set_state(EditShpmnt.description)


async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    new_kb = kb.exit_kb().add(kb.skip_button)
    await message.answer(text.EXTRA_FILE, reply_markup=new_kb)
    await state.set_state(EditShpmnt.extra_files)


@dp.callback_query_handler()
async def get_extra_files(message: types.Message,
                          state: FSMContext,
                          query: types.CallbackQuery):
    await state.update_data(extra_file=message.document.file_id)
    print(await state.get_data())


def register(dp: Dispatcher):
    dp.register_message_handler(
        get_note, state=EditShpmnt.note, content_types=['document'])
    dp.register_message_handler(get_ticket, state=EditShpmnt.number_ticket)
    dp.register_message_handler(get_invoice, state=EditShpmnt.number_invoice)
    dp.register_message_handler(get_storage, state=EditShpmnt.storage)
    dp.register_message_handler(
        get_another_changes, state=EditShpmnt.another_what_edit)
    dp.register_message_handler(get_description, state=EditShpmnt.description)
    dp.register_message_handler(
        get_extra_files,
        state=EditShpmnt.extra_files, content_types=['document'])
