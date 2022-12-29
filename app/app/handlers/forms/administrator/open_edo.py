import keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.base import BaseStates
from states.tgbot_states import OpenAcs
from utils import const


async def get_note(message: types.Message, state: FSMContext):
    await state.update_data(note=message.document.file_id)
    await message.answer('Укажите ФИО сотрудника', reply_markup=kb.exit_kb())
    await state.set_state(OpenAcs.staff_name)


async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(staff_name=message.text)
    await message.answer('Укажите, доступ к чему нужен сотруднику',
                         reply_markup=kb.exit_kb())
    await state.set_state(OpenAcs.what_acs)


async def get_acs(message: types.Message, state: FSMContext):
    await state.update_data(what_acs=message.text)
    storage_man_button = types.InlineKeyboardButton(
        'Кладовщик центрального склада', callback_data='Кладовщик ЦС')
    other_button = types.InlineKeyboardButton(
        'Другое', callback_data='other_role')
    new_kb = kb.choose_your_role().add(
        storage_man_button).add(other_button).add(kb.exit_button)
    await message.answer('Выберите роль сотрудника', reply_markup=new_kb)
    await state.set_state(OpenAcs.staff_role)


@dp.callback_query_handler(state=OpenAcs.staff_role)
async def get_staff_role(query: types.CallbackQuery, state: FSMContext):
    if query.data != 'other_role':
        await state.update_data(staff_role=query.data)
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer(const.FOR_WHAT_ACS,
                                   reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.for_what)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer('Введите роль: ', reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.another_role)


async def get_another_role(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'obj_name' not in data:
        await state.update_data(staff_role=message.text)
        await message.answer(const.FOR_WHAT_ACS, reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.for_what)
    else:
        await state.update_data(staff_role=message.text)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(OpenAcs.sure)


async def get_reason(message: types.Message, state: FSMContext):
    await state.update_data(for_what=message.text)
    await message.answer(
        'Укажите название объекта, к которому нужен доступ сотруднику: ',
        reply_markup=kb.exit_kb())
    await state.set_state(OpenAcs.obj_name)


async def get_obj_name(message: types.Message, state: FSMContext):
    await state.update_data(obj_name=message.text)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=kb.sure())
    await state.set_state(OpenAcs.sure)


@dp.callback_query_handler(state=OpenAcs.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(OpenAcs.edit)
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
        await state.set_state(OpenAcs.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='staff_name')
        await query.message.answer(
            'Укажите ФИО сотрудника', reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='what_acs')
        await query.message.answer('Укажите, доступ к чему нужен сотруднику',
                                   reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='staff_role')
        storage_man_button = types.InlineKeyboardButton(
            'Кладовщик центрального склада', callback_data='Кладовщик ЦС')
        other_button = types.InlineKeyboardButton(
            'Другое', callback_data='other_role')
        new_kb = kb.choose_your_role().add(
            storage_man_button).add(other_button).add(kb.exit_button)
        await query.message.answer(
            'Выберите роль сотрудника', reply_markup=new_kb)
        await state.set_state(OpenAcs.staff_role_edit)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='for_what')
        await query.message.answer(
            const.FOR_WHAT_ACS, reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    elif query.data == '9':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='obj_name')
        await query.message.answer(
            'Укажите название объекта, к которому нужен доступ сотруднику: ',
            reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'note':
        await state.update_data(note=message.document.file_id)
    elif point == 'staff_name':
        await state.update_data(staff_name=message.text)
    elif point == 'what_acs':
        await state.update_data(what_acs=message.text)
    elif point == 'other_role':
        await state.update_data(other_role=message.text)
    elif point == 'for_what':
        await state.update_data(for_what=message.text)
    elif point == 'obj_name':
        await state.update_data(obj_name=message.text)
    print(await state.get_data())
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(OpenAcs.sure)


@dp.callback_query_handler(state=OpenAcs.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(OpenAcs.sure)


@dp.callback_query_handler(state=OpenAcs.staff_role_edit)
async def get_staff_role_edit(query: types.CallbackQuery, state: FSMContext):
    if query.data != 'other_role':
        await state.update_data(staff_role=query.data)
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(OpenAcs.sure)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer('Введите роль: ', reply_markup=kb.exit_kb())
        await state.set_state(OpenAcs.another_role)


def register(dp: Dispatcher):
    dp.register_message_handler(
        get_note, state=OpenAcs.note, content_types=['document'])
    dp.register_message_handler(get_name, state=OpenAcs.staff_name)
    dp.register_message_handler(get_acs, state=OpenAcs.what_acs)
    dp.register_message_handler(get_another_role, state=OpenAcs.another_role)
    dp.register_message_handler(get_reason, state=OpenAcs.for_what)
    dp.register_message_handler(get_obj_name, state=OpenAcs.obj_name)
    dp.register_message_handler(edit,
                                state=OpenAcs.edit,
                                content_types=['text', 'document'])
