from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from states.tgbot_states import AddObj
from loader import dp, bot


@dp.callback_query_handler(state=AddObj.chapter)
async def get_chapter(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(chapter=query.data)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Укажите раздел: ', reply_markup=kb.exit_kb())
    await state.set_state(AddObj.section)


async def get_section(message: types.Message, state: FSMContext):
    await state.update_data(section=message.text)
    await message.answer('Укажите название подобъекта: ',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddObj.subobject_name)


async def get_subobject_name(message: types.Message, state: FSMContext):
    await state.update_data(subobject_name=message.text)
    await message.answer('Укажите cортировку: ', reply_markup=kb.exit_kb())
    await state.set_state(AddObj.sort)


async def get_sort(message: types.Message, state: FSMContext):
    await state.update_data(sort=message.text)
    new_kb = kb.add_subsystem_kb().add(kb.exit_button)
    await message.answer(
        'Укажите подсистемы, в которых подобъект будет отображаться',
        reply_markup=new_kb)
    await state.set_state(AddObj.subsystems)


raw_message = 'Ваш выбор: '
message_id = ''


@dp.callback_query_handler(state=AddObj.subsystems)
async def get_subobject(query: types.CallbackQuery, state: FSMContext):
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
        await state.update_data(subsystems=raw_message)
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        raw_message = 'Ваш выбор: '
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer('Вы уверены, что все данные верны?',
                                   reply_markup=new_kb)
        await state.set_state(AddObj.sure)


@dp.callback_query_handler(text='edit', state=AddObj.sure)
async def edit_data(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Выберите номер пункта для корректировки: ',
                               reply_markup=kb.choose_number())


def register(dp: Dispatcher):
    dp.register_message_handler(get_section, state=AddObj.section)
    dp.register_message_handler(get_subobject_name,
                                state=AddObj.subobject_name)
    dp.register_message_handler(get_sort, state=AddObj.sort)
