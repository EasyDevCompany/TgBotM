import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import AddNaming
from app.utils import const, get_data
from app.utils.const import SUB_PART, GROUP_MAT, NAME_MAT, UNIT_OF_MEASUREMENT, COUPLE, LOAD_OR_MISS, FIO, ROLE, R_TYPE


async def skip(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(field_six=None)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE, reply_markup=new_kb)
    await state.set_state(AddNaming.sure)
    await query.answer()


async def get_section_material(message: types.Message, state: FSMContext):
    await state.update_data(field_one=message.text)
    await message.answer(SUB_PART,
                         reply_markup=kb.exit_kb())
    await state.set_state(AddNaming.subsection_material)


async def get_subsection_material(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    await message.answer(GROUP_MAT,
                         reply_markup=kb.exit_kb())
    await state.set_state(AddNaming.group_material)


async def get_group_material(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    await message.answer(NAME_MAT,
                         reply_markup=kb.exit_kb())
    await state.set_state(AddNaming.name_material)


async def get_name_material(message: types.Message, state: FSMContext):
    await state.update_data(field_four=message.text)
    await message.answer(UNIT_OF_MEASUREMENT,
                         reply_markup=kb.exit_kb())
    await state.set_state(AddNaming.unit_of_measureament)


async def get_unit_of_measureament(message: types.Message, state: FSMContext):
    await state.update_data(field_five=message.text)
    new_kb = kb.exit_kb().add(kb.skip_button)
    await message.answer(COUPLE, reply_markup=new_kb)
    await state.set_state(AddNaming.add_several_naming)


async def get_add_several_naming(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(field_six=message.document.file_id)
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE,
                             reply_markup=new_kb)
        await state.set_state(AddNaming.sure)
    else:
        await message.answer(LOAD_OR_MISS)
        await state.set_state(AddNaming.add_several_naming)


async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(AddNaming.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(AddNaming.edit)
    elif query.data == '3':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='request_type')
        new_kb = kb.main_kb().add(kb.exit_button)
        await query.message.answer(R_TYPE,
                                   reply_markup=new_kb)
        await state.set_state(BaseStates.request_type)
    elif query.data == '4':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='section_material')
        await query.message.answer(
            const.SECTION_MATERIAL, reply_markup=kb.exit_kb())
        await state.set_state(AddNaming.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='subsection_material')
        await query.message.answer(SUB_PART,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddNaming.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='group_material')
        await query.message.answer(GROUP_MAT,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddNaming.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name_material')
        await query.message.answer(NAME_MAT,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddNaming.edit)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='unit_of_measureament')
        await query.message.answer(UNIT_OF_MEASUREMENT,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddNaming.edit)
    elif query.data == '9':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='several_naming')
        new_kb = kb.exit_kb().add(kb.skip_button)
        await query.message.answer(COUPLE, reply_markup=new_kb)
        await state.set_state(AddNaming.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'section_material':
        await state.update_data(field_one=message.text)
    elif point == 'subsection_material':
        await state.update_data(field_two=message.text)
    elif point == 'group_material':
        await state.update_data(field_three=message.text)
    elif point == 'name_material':
        await state.update_data(field_four=message.text)
    elif point == 'unit_of_measureament':
        await state.update_data(field_five=message.text)
    elif point == 'several_naming':
        await state.update_data(field_six=message.document.file_id)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(AddNaming.sure)


async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddNaming.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_section_material,
                                state=AddNaming.section_material)
    dp.register_message_handler(get_subsection_material,
                                state=AddNaming.subsection_material)
    dp.register_message_handler(get_group_material,
                                state=AddNaming.group_material)
    dp.register_message_handler(get_name_material,
                                state=AddNaming.name_material)
    dp.register_message_handler(get_unit_of_measureament,
                                state=AddNaming.unit_of_measureament)
    dp.register_message_handler(get_add_several_naming,
                                state=AddNaming.add_several_naming,
                                content_types=['any'])
    dp.register_message_handler(edit,
                                state=AddNaming.edit,
                                content_types=['text', 'document'])
    dp.register_callback_query_handler(skip, state=[AddNaming.add_several_naming,
                                                    AddNaming.edit])
    dp.register_callback_query_handler(correct, state=AddNaming.sure)
    dp.register_callback_query_handler(get_role, state=AddNaming.edit)
