import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot, dp
from app.states.base import BaseStates
from app.states.tgbot_states import EditViewWork
from app.utils import const, get_data


async def get_edit_sub_object_type_work(message: types.Message,
                                        state: FSMContext):
    await state.update_data(sub_object_type_work=['Подобъект видов работ',
                                                  message.text])
    await message.answer('Укажите вид работ',
                         reply_markup=kb.exit_kb())
    await state.set_state(EditViewWork.edit_type_work)


async def get_edit_type_work(message: types.Message, state: FSMContext):
    await state.update_data(type_work=['Вид работ', message.text])
    await message.answer('Укажите сортировку',
                         reply_markup=kb.exit_kb())
    await state.set_state(EditViewWork.edit_sort)


async def get_edit_sort(message: types.Message, state: FSMContext):
    await state.update_data(sort=['Сортировка', message.text])
    new_kb = kb.add_subsystem_kb().add(kb.exit_button)
    await message.answer(
        'Укажите подсистемы, в которых вид работ будет отображаться',
        reply_markup=new_kb)
    await state.set_state(EditViewWork.edit_sub_systems)


raw_message = const.YOUR_CHOISE
message_id = ''


@dp.callback_query_handler(state=EditViewWork.edit_sub_systems)
async def get_subsystems(query: types.CallbackQuery, state: FSMContext):
    global raw_message
    global message_id
    new_kb = kb.accept().add(kb.exit_button)
    if raw_message == const.YOUR_CHOISE and query.data != 'accept':
        raw_message += query.data
        msg = await query.message.answer(raw_message, reply_markup=new_kb)
        message_id = msg.message_id
    elif query.data != 'accept':
        raw_message += ', ' + query.data
        await bot.edit_message_text(raw_message,
                                    query.message.chat.id,
                                    message_id, reply_markup=new_kb)
    else:
        await state.update_data(subsystems=['Подсистемы', raw_message[11:]])
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        raw_message = 'Ваш выбор: '
        new_kb = kb.sure().add(kb.exit_button)
        await get_data.send_data(query=query, state=state)
        await query.message.answer('Вы уверены, что все данные верны?',
                                   reply_markup=new_kb)
        await state.set_state(EditViewWork.sure)
    await query.answer()


@dp.callback_query_handler(state=EditViewWork.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(EditViewWork.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(EditViewWork.edit)
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
        await state.update_data(change='sub_object_type_work')
        await query.message.answer(
            const.EDIT_SUBOBJECT_TYPE_WORK, reply_markup=kb.exit_kb())
        await state.set_state(EditViewWork.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='type_work')
        await query.message.answer('Укажите вид работ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditViewWork.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='sort')
        await query.message.answer('Укажите сортировку',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditViewWork.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.add_subsystem_kb().add(kb.exit_button)
        await query.message.answer(
            'Укажите подсистемы, в которых вид работ будет отображаться',
            reply_markup=new_kb)
        await state.set_state(EditViewWork.edit_sub_systems)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=['ФИО', message.text])
    elif point == 'sub_object_type_work':
        await state.update_data(sub_object_type_work=['Подобъект видов работ',
                                                      message.text])
    elif point == 'type_work':
        await state.update_data(type_work=['Вид работ', message.text])
    elif point == 'sort':
        await state.update_data(type_work=['Вид работ', message.text])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(EditViewWork.sure)


@dp.callback_query_handler(state=EditViewWork.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(role=['Роль', query.data])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(EditViewWork.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_edit_sub_object_type_work,
                                state=EditViewWork.edit_sub_object_type_work)
    dp.register_message_handler(get_edit_type_work,
                                state=EditViewWork.edit_type_work)
    dp.register_message_handler(get_edit_sort, state=EditViewWork.edit_sort)
    dp.register_message_handler(edit, state=EditViewWork.edit)
    dp.register_callback_query_handler(get_subsystems, state=EditViewWork.edit_sub_systems)
    dp.register_callback_query_handler(correct, state=EditViewWork.sure)
    dp.register_callback_query_handler(get_role, state=EditViewWork.edit)
