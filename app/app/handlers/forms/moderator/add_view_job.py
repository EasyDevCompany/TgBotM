import keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.base import BaseStates
from states.tgbot_states import AddViewWork
from utils import const, get_data


async def get_sub_object(message: types.Message, state: FSMContext):
    await state.update_data(field_one=message.text)
    await message.answer('Укажите наименование вида работ',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddViewWork.type_work)


async def get_type_work(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    await message.answer('Укажите сортировку',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddViewWork.sort)


async def get_sort(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    new_kb = kb.add_subsystem_kb().add(kb.exit_button)
    await message.answer(
        'Укажите подсистемы, в которых вид работ будет отображаться',
        reply_markup=new_kb)
    await state.set_state(AddViewWork.subsystems)


raw_message = const.YOUR_CHOISE
message_id = ''


@dp.callback_query_handler(state=AddViewWork.subsystems)
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
        await state.update_data(field_four=raw_message[11:])
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        raw_message = const.YOUR_CHOISE
        new_kb = kb.sure().add(kb.exit_button)
        await get_data.send_data(query=query, state=state)
        await query.message.answer(const.SURE,
                                   reply_markup=new_kb)
        await state.set_state(AddViewWork.sure)
    await query.answer()


@dp.callback_query_handler(state=AddViewWork.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(AddViewWork.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(AddViewWork.edit)
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
        await state.update_data(change='sub_object')
        await query.message.answer(
            const.SELECT_SUBOBJECT, reply_markup=kb.exit_kb())
        await state.set_state(AddViewWork.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='type_work')
        await query.message.answer('Укажите наименование вида работ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddViewWork.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='sort')
        await query.message.answer('Укажите сортировку',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddViewWork.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.add_subsystem_kb().add(kb.exit_button)
        await query.message.answer(
            'Укажите подсистемы, в которых вид работ будет отображаться',
            reply_markup=new_kb)
        await state.set_state(AddViewWork.subsystems)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'type_work':
        await state.update_data(field_two=message.text)
    elif point == 'name':
        await state.update_data(name=['ФИО', message.text])
    elif point == 'sub_object':
        await state.update_data(field_one=message.text)
    elif point == 'sort':
        await state.update_data(field_three=message.text)
    await get_data.send_data(message=message, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(AddViewWork.sure)


@dp.callback_query_handler(state=AddViewWork.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    await get_data.send_data(query=query, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddViewWork.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_sub_object, state=AddViewWork.sub_object)
    dp.register_message_handler(get_type_work, state=AddViewWork.type_work)
    dp.register_message_handler(get_sort, state=AddViewWork.sort)
    dp.register_message_handler(get_subsystems,
                                state=AddViewWork.subsystems)
    dp.register_message_handler(edit, state=AddViewWork.edit)
