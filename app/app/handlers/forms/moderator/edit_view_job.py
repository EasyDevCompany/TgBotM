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
    new_kb = kb.add_subsystem_kb().add(kb.exit_button)
    await message.answer(
        'Укажите подсистемы, в которых вид работ будет отображаться',
        reply_markup=new_kb)
    await state.set_state(EditViewWork.edit_sub_systems)


raw_message = 'Ваш выбор: '
message_id = ''


@dp.callback_query_handler(state=EditViewWork.edit_sub_systems)
async def get_subsystems(query: types.CallbackQuery, state: FSMContext):
    global raw_message
    global message_id
    new_kb = kb.accept().add(kb.exit_button)
    if raw_message == 'Ваш выбор: ' and query.data != 'accept':
        raw_message += query.data
        msg = await query.message.answer(raw_message, reply_markup=new_kb)
        message_id = msg.message_id
    elif query.data != 'accept':
        raw_message += ', ' + query.data
        await bot.edit_message_text(raw_message,
                                    query.message.chat.id,
                                    message_id, reply_markup=new_kb)
    else:
        await state.update_data(subsystems=raw_message[11:])
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        raw_message = 'Ваш выбор: '
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer('Вы уверены, что все данные верны?',
                                   reply_markup=new_kb)
        await state.set_state(EditViewWork.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_edit_sub_object_type_work,
                                state=EditViewWork.edit_sub_object_type_work)
    dp.register_message_handler(get_edit_type_work,
                                state=EditViewWork.edit_type_work)
    dp.register_message_handler(get_edit_sort, state=EditViewWork.edit_sort)
