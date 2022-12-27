from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from states.tgbot_states import OpenAcs
from loader import dp, bot
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
async def get_role(query: types.CallbackQuery, state: FSMContext):
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
    await state.update_data(staff_role=message.text)
    await message.answer(const.FOR_WHAT_ACS, reply_markup=kb.exit_kb())
    await state.set_state(OpenAcs.for_what)


async def get_reason(message: types.Message, state: FSMContext):
    await state.update_data(for_what=message.text)
    await message.answer(
        'Укажите название объекта, к которому нужен доступ сотруднику: ',
        reply_markup=kb.exit_kb())
    await state.set_state(OpenAcs.obj_name)


async def get_obj_name(message: types.Message, state: FSMContext):
    await state.update_data(obj_name=message.text)
    print(await state.get_data())
    await message.answer(const.START_MESSAGE, reply_markup=kb.start_work)


def register(dp: Dispatcher):
    dp.register_message_handler(
        get_note, state=OpenAcs.note, content_types=['document'])
    dp.register_message_handler(get_name, state=OpenAcs.staff_name)
    dp.register_message_handler(get_acs, state=OpenAcs.what_acs)
    dp.register_message_handler(get_another_role, state=OpenAcs.another_role)
    dp.register_message_handler(get_reason, state=OpenAcs.for_what)
    dp.register_message_handler(get_obj_name, state=OpenAcs.obj_name)
