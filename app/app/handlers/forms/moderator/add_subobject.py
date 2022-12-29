import keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.base import BaseStates
from states.tgbot_states import AddObj
from utils import const


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
        await state.set_state(AddObj.sure)
    await query.answer()


@dp.callback_query_handler(state=AddObj.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(AddObj.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(AddObj.edit)
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
        await state.update_data(change='chapter')
        new_kb = kb.add_subobjects_kb().add(kb.exit_button)
        await query.message.answer(
            const.SET_CHAPTER, reply_markup=new_kb)
        await state.set_state(AddObj.edit_chapter)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='section')
        await query.message.answer('Раздел для материала',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObj.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='subobject_name')
        await query.message.answer('Укажите название подобъекта',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObj.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='sort')
        await query.message.answer('Укажите сортировку',
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddObj.edit)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.add_subsystem_kb().add(kb.exit_button)
        await query.message.answer(
            'Укажите подсистемы, в которых вид работ будет отображаться',
            reply_markup=new_kb)
        await state.set_state(AddObj.subsystems)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'section':
        await state.update_data(section=message.text)
    elif point == 'subobject_name':
        await state.update_data(subobject_name=message.text)
    elif point == 'sort':
        await state.update_data(sort=message.text)
    print(await state.get_data())
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(AddObj.sure)


@dp.callback_query_handler(state=AddObj.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddObj.sure)


@dp.callback_query_handler(state=AddObj.edit_chapter)
async def get_chapter_edit(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(chapter=query.data)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    new_kb = kb.sure().add(kb.exit_button)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddObj.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_section, state=AddObj.section)
    dp.register_message_handler(get_subobject_name,
                                state=AddObj.subobject_name)
    dp.register_message_handler(get_sort, state=AddObj.sort)
    dp.register_message_handler(edit, state=AddObj.edit)
