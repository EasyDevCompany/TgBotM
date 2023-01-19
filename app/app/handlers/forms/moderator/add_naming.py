import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import AddNaming
from app.utils import const, get_data
from app.utils.const import SUB_PART, GROUP_MAT, NAME_MAT, UNIT_OF_MEASUREMENT, COUPLE, LOAD_OR_MISS, FIO, ROLE
from dependency_injector.wiring import inject, Provide
from app.services.application import ApplicationService
from app.core.container import Container
from app.models.application import Application
from logger import logger


@inject
async def skip(query: types. CallbackQuery, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    if 'admin' not in data:
        await state.update_data(field_six='---')
        await bot.delete_message(query.message.chat.id, query.message.message_id)
        await get_data.send_data(query=query, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(AddNaming.sure)
        await query.answer()
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'field_six': '---'})
        await query.message.answer(const.CHANGE_SUCCESS)
        await state.finish()


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


@inject
async def get_add_several_naming(message: types.Message, state: FSMContext,
                                 application: ApplicationService = Provide[Container.application_service]):
    if message.content_type == 'document':
        await state.update_data(field_six=message.document.file_id)
        data = await state.get_data()
        if 'admin' not in data:
            await get_data.send_data(message=message, state=state)
            new_kb = kb.sure().add(kb.exit_button)
            await message.answer(const.SURE, reply_markup=new_kb)
            await state.set_state(AddNaming.sure)
        else:
            black_list = {'admin'}
            new_data = {key: val for key, val in data.items() if key not in black_list}
            unused = ['field_seven', 'field_eight', 'field_nine']
            for i in unused:
                new_data[i] = None
            logger.info(new_data)
            await application.update(data['admin'], obj_in=new_data)
            await message.answer(const.CHANGE_SUCCESS)
            await state.finish()
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
        data = await state.get_data()
        if 'admin' in data:
            await bot.delete_message(query.message.chat.id,
                                     query.message.message_id)
            await query.message.answer(text=FIO, reply_markup=kb.exit_kb())
            await state.set_state(BaseStates.fio)
        else:
            await bot.delete_message(
                query.message.chat.id, query.message.message_id)
            await state.finish()
            await query.message.answer(text=FIO, reply_markup=kb.exit_kb())
            await state.set_state(BaseStates.fio)
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


@inject
async def edit(message: types.Message, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
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
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(AddNaming.sure)
    else:
        if 'name' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'name': data['name']})
        elif 'field_one' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_one': data['field_one']})
        elif 'field_two' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_two': data['field_two']})
        elif 'field_three' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_three': data['field_three']})
        elif 'field_four' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_four': data['field_four']})
        elif 'field_five' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_five': data['field_five']})
        elif 'field_six' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_six': data['field_six']})
        await message.answer(const.CHANGE_SUCCESS)
        await state.finish()


@inject
async def get_role(query: types.CallbackQuery, state: FSMContext,
                   application: ApplicationService = Provide[Container.application_service]):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    data = await state.get_data()
    logger.info(data)
    if 'admin' not in data:
        await get_data.send_data(query=query, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE,
                                   reply_markup=new_kb)
        await state.set_state(AddNaming.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'role': data['role']})
        await query.message.answer(const.CHANGE_SUCCESS)
        await state.finish()


def register(dp: Dispatcher):
    dp.register_callback_query_handler(get_role, state=AddNaming.edit)
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
    
