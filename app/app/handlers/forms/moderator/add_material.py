import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot, dp
from app.states.base import BaseStates
from app.states.tgbot_states import AddMat
from app.utils import const, get_data


async def get_note(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(note=['Файл служебной записки',
                                      message.document.file_id])
        await message.answer('Выберите склад, куда необходимо добавить остатки: ',
                             reply_markup=kb.exit_kb())
        await state.set_state(AddMat.storage)
    else:
        await message.answer('Пожалуйста, загрузите документ')
        await state.set_state(AddMat.note)


async def get_storage(message: types.Message, state: FSMContext):
    await state.update_data(storage=['Склад', message.text])
    await message.answer('Excel файл с данными по наименованиям по формату: ',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddMat.excel)


async def get_excel(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(excel=['Excel файл', message.document.file_id])
        new_kb = kb.reserve_or_leave().add(kb.exit_button)
        await message.answer('Укажите, необходимо ли добавлять остатки на резерв '
                             'или на свободные остатки', reply_markup=new_kb)
        await state.set_state(AddMat.myc)
    else:
        await message.answer('Пожалуйста, загрузите Excel документ')
        await state.set_state(AddMat.excel)


@dp.callback_query_handler(state=AddMat.myc)
async def get_choise(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(choise=['Действие с остатками', query.data])
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    if query.data == 'reserve':
        await query.message.answer('Если остатки на резерве, то на какой '
                                   'объект их необходимо резервировать',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddMat.obj)
    elif query.data == 'leave':
        await state.update_data(obj=[const.WHICH_OBJECT, 'None'])
        await get_data.send_data(query=query, state=state)
        await query.message.answer(const.SURE,
                                   reply_markup=kb.sure())
        await state.set_state(AddMat.sure)


async def get_obj(message: types.Message, state: FSMContext):
    await state.update_data(obj=[const.WHICH_OBJECT, message.text])
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=kb.sure())
    await state.set_state(AddMat.sure)


@dp.callback_query_handler(state=AddMat.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(AddMat.edit)
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
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage')
        await query.message.answer(
            'Выберите склад, куда необходимо добавить остатки: ',
            reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='excel')
        await query.message.answer(
            'Excel файл с данными по наименованиям по формату: ',
            reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='choise')
        new_kb = kb.reserve_or_leave().add(kb.exit_button)
        await query.message.answer(
            'Укажите, необходимо ли добавлять остатки на резерв '
            'или на свободные остатки', reply_markup=new_kb)
        await state.set_state(AddMat.myc)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='obj')
        await query.message.answer('Если остатки на резерве, то на какой '
                                   'объект их необходимо резервировать',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=['ФИО', message.text])
    elif point == 'note':
        await state.update_data(note=['Файл служебной записки',
                                      message.document.file_id])
    elif point == 'storage':
        await state.update_data(storage=['Склад', message.text])
    elif point == 'excel':
        await state.update_data(excel=['Excel файл', message.document.file_id])
    elif point == 'obj':
        await state.update_data(obj=[const.WHICH_OBJECT, message.text])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(AddMat.sure)


@dp.callback_query_handler(state=AddMat.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=['Роль', query.data])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddMat.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_note,
                                state=AddMat.note, content_types=['any'])
    dp.register_message_handler(get_storage, state=AddMat.storage)
    dp.register_message_handler(get_excel,
                                state=AddMat.excel, content_types=['any'])
    dp.register_message_handler(get_obj, state=AddMat.obj)
    dp.register_message_handler(edit,
                                state=AddMat.edit,
                                content_types=['text', 'document'])
    dp.register_callback_query_handler(get_choise, state=AddMat.myc)
    dp.register_callback_query_handler(correct, state=AddMat.sure)
    dp.register_callback_query_handler(get_role, state=AddMat.edit)
