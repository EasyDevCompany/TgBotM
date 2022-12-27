from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from states.tgbot_states import AddObjAdm
from loader import dp


async def get_note(message: types.Message, state: FSMContext):
    await state.update_data(note=message.document.file_id)
    await message.answer(
        'Укажите название объекта, который необходимо добавить: ')
    await state.set_state(AddObjAdm.obj_name)


async def get_obj_name(message: types.Message, state: FSMContext):
    await state.update_data(obj_name=message.text)
    await message.answer('Укажите титул объекта: ')
    await state.set_state(AddObjAdm.title)


async def get_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer('Укажите склад объекта:',
                         reply_markup=kb.storage_kb())
    await state.set_state(AddObjAdm.storage)


@dp.callback_query_handler(state=AddObjAdm.storage)
async def get_storage(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'exist_storage':
        await query.message.answer('Укажите склад: ')
        await state.set_state(AddObjAdm.exist_storage)
    elif query.data == 'new_storage':
        await query.message.answer('Укажите название нового склада, '
                                   'Ф.И.О ответственного лица и титул')
        await state.set_state(AddObjAdm.if_new)


async def exist_storage(message: types.Message, state: FSMContext):
    await state.update_data(storage=message.text)
    print(await state.get_data())


async def if_new(message: types.Message, state: FSMContext):
    await state.update_data(storage=message.text)
    print(await state.get_data())


def register(dp: Dispatcher):
    dp.register_message_handler(
        get_note, state=AddObjAdm.note, content_types=['document'])
    dp.register_message_handler(get_obj_name, state=AddObjAdm.obj_name)
    dp.register_message_handler(get_title, state=AddObjAdm.title)
    dp.register_message_handler(exist_storage, state=AddObjAdm.exist_storage)
    dp.register_message_handler(if_new, state=AddObjAdm.if_new)
