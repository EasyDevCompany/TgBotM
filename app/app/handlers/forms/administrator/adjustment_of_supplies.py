import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot, dp
from app.states.base import BaseStates
from app.states.tgbot_states import EditShpmnt
from app.utils import const, get_data
from app.utils import const_edit_shpmnt as text


@dp.callback_query_handler(text='skip', state=EditShpmnt.extra_files)
async def skip(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(extra_file=['Дополнительные файлы', None])
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE, reply_markup=new_kb)
    await get_data.send_data(query=query, state=state)
    await state.set_state(EditShpmnt.sure)


async def get_note(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(note=['Файл служебной записки',
                                      message.document.file_id])
        await message.answer(
            'Укажите номер заявки: ', reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.number_ticket)
    else:
        await message.answer('Пожалуйста, загрузите документ')
        await state.set_state(EditShpmnt.note)


async def get_ticket(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(number_ticket=['Номер заявки',
                                               message.text])
        await message.answer(text.NUM_INVOICE, reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.number_invoice)
    else:
        await state.set_state(EditShpmnt.number_ticket)
        await message.answer('Пожалуйста, укажите номер заявки цифрами')


async def get_invoice(message: types.Message, state: FSMContext):
    await state.update_data(number_invoice=['Номер накладной', message.text])
    await message.answer(
        'Укажите входящий склад(на который приняли поставку): ',
        reply_markup=kb.exit_kb())
    await state.set_state(EditShpmnt.storage)


async def get_storage(message: types.Message, state: FSMContext):
    await state.update_data(storage=['Склад', message.text])
    new_kb = kb.what_edit().add(kb.exit_button)
    await message.answer('Что необходимо отредактировать в поставке:',
                         reply_markup=new_kb)
    await state.set_state(EditShpmnt.what_edit)


@dp.callback_query_handler(state=EditShpmnt.what_edit)
async def get_changes(query: types.CallbackQuery, state: FSMContext):
    if query.data != 'Другое':
        await state.update_data(what_edit=[const.WHAT_EDIT, query.data])
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer(const.DESCRIPTION_ERROR,
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.description)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer('Что редактируем: ',
                                   reply_markup=kb.exit_kb())
        await query.message.answer(const.DESCRIPTION_ERROR,
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.description)


async def get_another_changes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'extra_file' not in data:
        await state.update_data(what_edit=[const.WHAT_EDIT, message.text])
        await message.answer(const.DESCRIPTION_ERROR,
                             reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.description)
    else:
        await state.update_data(what_edit=[const.WHAT_EDIT, message.text])
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(EditShpmnt.sure)


async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=['Описание ошибки', message.text])
    new_kb = kb.exit_kb().add(kb.skip_button)
    await message.answer(text.EXTRA_FILE, reply_markup=new_kb)
    await state.set_state(EditShpmnt.extra_files)


# @dp.callback_query_handler(state=EditShpmnt.extra_files)
async def get_extra_files(message: types.Message,
                          state: FSMContext):
    try:
        await state.update_data(extra_file=['Дополнительные файлы',
                                            message.media_group_id])
    except:
        await state.update_data(extra_file=['Дополнительные файлы',
                                            message.document.file_id])
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(EditShpmnt.sure)
    await get_data.send_data(message=message, state=state)


@dp.callback_query_handler(state=EditShpmnt.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(EditShpmnt.edit)
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
        await state.set_state(EditShpmnt.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_ticket')
        await query.message.answer(
            'Укажите номер заявки, если перемещение по заявке',
            reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_invoice')
        await query.message.answer(text.NUM_INVOICE, reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage')
        await query.message.answer(
            'Укажите входящий склад(на который приняли поставку): ',
            reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='what_edit')
        new_kb = kb.what_edit().add(kb.exit_button)
        await query.message.answer(
            'Что необходимо отредактировать в поставке:',
            reply_markup=new_kb)
        await state.set_state(EditShpmnt.what_edit_correct)
    elif query.data == '9':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='description')
        await query.message.answer(
            const.DESCRIPTION_ERROR,
            reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '10':
        new_kb = kb.exit_kb().add(kb.skip_button)
        await query.message.answer(text.EXTRA_FILE, reply_markup=new_kb)
        await state.set_state(EditShpmnt.extra_files)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=['ФИО', message.text])
    elif point == 'note':
        await state.update_data(note=['Файл служебной записки',
                                      message.document.file_id])
    elif point == 'number_ticket':
        await state.update_data(number_ticket=['Номер заявки',
                                               message.text])
    elif point == 'number_invoice':
        await state.update_data(number_invoice=['Номер накладной',
                                                message.text])
    elif point == 'storage':
        await state.update_data(storage=['Склад', message.text])
    elif point == 'description':
        await state.update_data(description=['Описание ошибки', message.text])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(EditShpmnt.sure)


@dp.callback_query_handler(state=EditShpmnt.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=['Роль', query.data])
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE, reply_markup=new_kb)
    await get_data.send_data(query=query, state=state)
    await state.set_state(EditShpmnt.sure)


@dp.callback_query_handler(state=EditShpmnt.what_edit_correct)
async def get_changes_edit(query: types.CallbackQuery, state: FSMContext, ):
    if query.data != 'Другое':
        await state.update_data(what_edit=[const.WHAT_EDIT, query.data])
        await bot.delete_message(query.message.chat.id,
                                 query.message.message_id)
        new_kb = kb.sure().add(kb.exit_button)
        await get_data.send_data(query=query, state=state)
        await query.message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(EditShpmnt.sure)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer('Что редактируем: ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.another_what_edit)


def register(dp: Dispatcher):
    dp.register_message_handler(
        get_note, state=EditShpmnt.note, content_types=['any'])
    dp.register_message_handler(get_ticket, state=EditShpmnt.number_ticket)
    dp.register_message_handler(get_invoice, state=EditShpmnt.number_invoice)
    dp.register_message_handler(get_storage, state=EditShpmnt.storage)
    dp.register_message_handler(
        get_another_changes, state=EditShpmnt.another_what_edit)
    dp.register_message_handler(get_description, state=EditShpmnt.description)
    dp.register_message_handler(
        get_extra_files,
        state=EditShpmnt.extra_files, content_types=['any'])
    dp.register_message_handler(edit,
                                state=EditShpmnt.edit,
                                content_types=['text', 'document'])
    dp.register_callback_query_handler(skip, state=EditShpmnt.extra_files)
    dp.register_callback_query_handler(get_changes, state=EditShpmnt.what_edit)
    dp.register_callback_query_handler(correct, state=EditShpmnt.sure)
    dp.register_callback_query_handler(get_role, state=EditShpmnt.edit)
    dp.register_callback_query_handler(get_changes_edit, state=EditShpmnt.what_edit_correct)
