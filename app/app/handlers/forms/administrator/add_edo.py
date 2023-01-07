import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot, dp
from app.states.base import BaseStates
from app.states.tgbot_states import AddObjAdm
from app.utils import const, get_data


async def get_note(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(note=['Файл служебной записки',
                                      message.document.file_id])
        await message.answer(
            'Укажите название объекта, который необходимо добавить: ',
            reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.obj_name)
    else:
        await message.answer('Пожалуйста, загрузите документ')
        await state.set_state(AddObjAdm.note)


async def get_obj_name(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if not message.text.isdigit():
            await state.update_data(obj_name=['Название объекта', message.text])
            await message.answer('Укажите титул объекта: ', reply_markup=kb.exit_kb())
            await state.set_state(AddObjAdm.title)
        else:
            await message.answer('Название объекта не может состоять только из цифр')
            await state.set_state(AddObjAdm.obj_name)
    else:
        await message.answer('Пожалуйста, укажите название объекта')
        await state.set_state(AddObjAdm.obj_name)


async def get_title(message: types.Message, state: FSMContext):
    await state.update_data(title=['Титул объекта', message.text])
    new_kb = kb.storage_kb().add(kb.exit_button)
    await message.answer('Укажите склад объекта:',
                         reply_markup=new_kb)
    await state.set_state(AddObjAdm.new_or_exist)


@dp.callback_query_handler(state=AddObjAdm.new_or_exist)
async def get_new_or_exist(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    if query.data == 'exist_storage':
        await state.update_data(new_or_exist=['Уже существующий или новый',
                                              'существующий'])
        await query.message.answer('Укажите склад: ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.storage)
    elif query.data == 'new_storage':
        await state.update_data(new_or_exist=['Уже существующий или новый',
                                              'новый'])
        await query.message.answer('Укажите название нового склада, '
                                   'Ф.И.О ответственного лица и титул',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.storage)


async def get_storage(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if not message.text.isdigit():
            await state.update_data(storage=['Склад', message.text])
            await get_data.send_data(message=message, state=state)
            new_kb = kb.sure().add(kb.exit_button)
            await message.answer(const.SURE,
                                 reply_markup=new_kb)
            await state.set_state(AddObjAdm.sure)
        else:
            await message.answer('Название склада не может состоять только из цифр')
            await state.set_state(AddObjAdm.storage)
    else:
        await message.answer('Пожалуйста, напишите название склада')
        await state.set_state(AddObjAdm.storage)


@dp.callback_query_handler(state=AddObjAdm.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await state.update_data(change='name')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    elif query.data == '2':
        await state.update_data(change='role')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(AddObjAdm.edit)
    elif query.data == '3':
        await state.update_data(change='request_type')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.main_kb().add(kb.exit_button)
        await query.message.answer('Выберите тип запроса',
                                   reply_markup=new_kb)
        await state.set_state(BaseStates.request_type)
    elif query.data == '4':
        await state.update_data(change='note')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    elif query.data == '5':
        await state.update_data(change='obj_name')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer(
            'Укажите название объекта, который необходимо добавить: ',
            reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='title')
        await query.message.answer(
            'Укажите титул объекта: ', reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.storage_kb().add(kb.exit_button)
        await query.message.answer('Укажите склад объекта:',
                                   reply_markup=new_kb)
        await state.set_state(AddObjAdm.new_or_exist)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage')
        await query.message.answer('Укажите название нового склада, '
                                   'Ф.И.О ответственного лица и титул',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObjAdm.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=['ФИО', message.text])
    elif point == 'note':
        await state.update_data(note=['Файл служебной записки',
                                      message.document.file_id])
    elif point == 'obj_name':
        await state.update_data(obj_name=['Название объекта', message.text])
    elif point == 'title':
        await state.update_data(title=['Титул объекта', message.text])
    elif point == 'storage':
        await state.update_data(storage=['Склад', message.text])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(AddObjAdm.sure)


@dp.callback_query_handler(state=AddObjAdm.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=['Роль', query.data])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddObjAdm.sure)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(get_new_or_exist, state=AddObjAdm.new_or_exist)
    dp.register_message_handler(
        get_note, state=AddObjAdm.note, content_types=['any'])
    dp.register_message_handler(get_obj_name, state=AddObjAdm.obj_name, content_types=['any'])
    dp.register_message_handler(get_title, state=AddObjAdm.title)
    dp.register_message_handler(get_storage, state=AddObjAdm.storage, content_types=['any'])
    dp.register_message_handler(edit,
                                state=AddObjAdm.edit,
                                content_types=['text', 'document'])
    dp.register_callback_query_handler(correct, state=AddObjAdm.sure)
    dp.register_callback_query_handler(get_role, state=AddObjAdm.edit)
