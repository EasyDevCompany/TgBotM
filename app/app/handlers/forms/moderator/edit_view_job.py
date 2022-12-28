from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from loader import dp, bot
from states.tgbot_states import EditViewWork


async def get_edit_sub_object_type_work(message: types.Message, state: FSMContext):
    await state.update_data(sub_object_type_work=message.text)
    await message.answer('Укажите вид работ',
                         reply_markup=kb.exit_kb())
    await state.set_state(EditViewWork.edit_type_work)


async def get_edit_type_work(message: types.Message, state: FSMContext):
    await state.update_data(type_work=message.text)
    await message.answer('Укажите сортировку',
                         reply_markup=kb.exit_kb())
    await state.set_state(EditViewWork.edit_sort)


async def get_edit_sort(message: types.Message, state: FSMContext):
    await state.update_data(sort=message.text)
    new_kb = kb.sub_systems_kb().add(kb.exit_button)
    await message.answer('Укажите подсистемы, в которых вид работ будет отображаться',
                         reply_markup=new_kb)
    await state.set_state(EditViewWork.edit_sub_systems)


@dp.callback_query_handler(state=EditViewWork.edit_sub_systems)
async def get_edit_sub_systems(message: types.Message, state: FSMContext):
    await state.update_data(sub_systems=message.text)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=kb.sure())
    await state.set_state(EditViewWork.sure)


@dp.callback_query_handler(text='edit', state=EditViewWork.sure)
async def edit_data(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Выберите номер пункта для корректировки: ',
                               reply_markup=kb.choose_number())


def register(dp: Dispatcher):
    dp.register_message_handler(get_edit_sub_object_type_work, state=EditViewWork.edit_sub_object_type_work)
    dp.register_message_handler(get_edit_type_work, state=EditViewWork.edit_type_work)
    dp.register_message_handler(get_edit_sort, state=EditViewWork.edit_sort)
    dp.register_message_handler(get_edit_sub_systems, state=EditViewWork.edit_sub_systems)