import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot, dp
from app.states.base import BaseStates
from app.states.tgbot_states import AddObj
from app.utils import const, get_data


@dp.callback_query_handler(state=AddObj.chapter)
async def get_chapter(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(chapter=['Глава', query.data])
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Укажите раздел: ', reply_markup=kb.exit_kb())
    await state.set_state(AddObj.section)


async def get_section(message: types.Message, state: FSMContext):
    await state.update_data(section=['Раздел', message.text])
    await message.answer('Укажите название подобъекта: ',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddObj.subobject_name)


async def get_subobject_name(message: types.Message, state: FSMContext):
    await state.update_data(subobject_name=['Название подобъекта',
                                            message.text])
    await message.answer('Укажите cортировку: ', reply_markup=kb.exit_kb())
    await state.set_state(AddObj.sort)


async def get_sort(message: types.Message, state: FSMContext):
    await state.update_data(sort=['Сортировка', message.text])
    new_kb = kb.add_subsystem_kb().add(kb.exit_button)
    await message.answer(
        'Укажите подсистемы, в которых подобъект будет отображаться',
        reply_markup=new_kb)
    await state.set_state(AddObj.subsystems)


raw_message = const.YOUR_CHOISE
message_id = ''


@dp.callback_query_handler(state=AddObj.subsystems)
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
        raw_message = const.YOUR_CHOISE
        await get_data.send_data(query=query, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE,
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
        await state.update_data(name=['ФИО', message.text])
    elif point == 'section':
        await state.update_data(section=['Раздел', message.text])
    elif point == 'subobject_name':
        await state.update_data(subobject_name=['Название подобъекта',
                                                message.text])
    elif point == 'sort':
        await state.update_data(sort=['Сортировка', message.text])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(AddObj.sure)


@dp.callback_query_handler(state=AddObj.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=['Роль', query.data])
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddObj.sure)


@dp.callback_query_handler(state=AddObj.edit_chapter)
async def get_chapter_edit(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(chapter=['Глава', query.data])
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddObj.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_section, state=AddObj.section)
    dp.register_message_handler(get_subobject_name,
                                state=AddObj.subobject_name)
    dp.register_message_handler(get_sort, state=AddObj.sort)
    dp.register_message_handler(edit, state=AddObj.edit)
    dp.register_callback_query_handler(get_chapter, state=AddObj.chapter)
    dp.register_callback_query_handler(get_subsystems, state=AddObj.subsystems)
    dp.register_callback_query_handler(correct, state=AddObj.sure)
    dp.register_callback_query_handler(get_role, state=AddObj.edit)
    dp.register_callback_query_handler(get_chapter_edit, state=AddObj.edit_chapter)

