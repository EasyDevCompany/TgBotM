import keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.base import BaseStates
from states.tgbot_states import AddObj
from utils import const, get_data
from dependency_injector.wiring import inject, Provide
from app.services.application import ApplicationService
from app.core.container import Container
from app.models.application import Application



@dp.callback_query_handler(state=AddObj.chapter)
async def get_chapter(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(field_one=query.data)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Укажите раздел: ', reply_markup=kb.exit_kb())
    await state.set_state(AddObj.section)


async def get_section(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    await message.answer('Укажите название подобъекта: ',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddObj.subobject_name)


async def get_subobject_name(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    await message.answer('Укажите cортировку: ', reply_markup=kb.exit_kb())
    await state.set_state(AddObj.sort)


async def get_sort(message: types.Message, state: FSMContext):
    await state.update_data(field_four=message.text)
    new_kb = kb.add_subsystem_kb().add(kb.exit_button)
    await message.answer(
        'Укажите подсистемы, в которых подобъект будет отображаться',
        reply_markup=new_kb)
    await state.set_state(AddObj.subsystems)


@dp.callback_query_handler(state=AddObj.subsystems)
async def get_subsystems(query: types.CallbackQuery, state: FSMContext):
    new_kb = kb.accept().add(kb.exit_button)
    data = await state.get_data()
    if query.data != 'accept' and 'field_five' not in data:
        await state.update_data(field_five=query.data)
        data = await state.get_data()
        msg = await query.message.answer(data['field_five'], reply_markup=new_kb)
        await state.update_data(message_id=msg.message_id)
    elif query.data != 'accept':
        data = await state.get_data()
        await state.update_data(field_five=data['field_five'] + ', ' + query.data)
        new_data = await state.get_data()
        await bot.edit_message_text(new_data['field_five'],
                                    query.message.chat.id,
                                    new_data['message_id'], reply_markup=new_kb)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
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
        await state.update_data(field_five='')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.add_subsystem_kb().add(kb.exit_button)
        await query.message.answer(
            'Укажите подсистемы, в которых вид работ будет отображаться',
            reply_markup=new_kb)
        await state.set_state(AddObj.subsystems_edit)
    await query.answer()


@inject
async def edit(message: types.Message, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'section':
        await state.update_data(field_two=message.text)
    elif point == 'subobject_name':
        await state.update_data(field_three=message.text)
    elif point == 'sort':
        await state.update_data(field_four=message.text)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(AddObj.sure)
    else:
        if 'name' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'name': data['name']})
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
        await message.answer(const.CHANGE_SUCCESS)
        await state.finish()


@dp.callback_query_handler(state=AddObj.edit)
@inject
async def get_role(query: types.CallbackQuery, state: FSMContext,
                   application: ApplicationService = Provide[Container.application_service]):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(query=query, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE,
                                   reply_markup=new_kb)
        await state.set_state(AddObj.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'role': data['role']})
        await query.message.answer(const.CHANGE_SUCCESS)
        await state.finish()


@dp.callback_query_handler(state=AddObj.edit_chapter)
@inject
async def get_chapter_edit(query: types.CallbackQuery, state: FSMContext,
                           application: ApplicationService = Provide[Container.application_service]):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(field_one=query.data)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(query=query, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(AddObj.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'field_one': data['field_one']})
        await query.message.answer(const.CHANGE_SUCCESS)
        await state.finish()


@dp.callback_query_handler(state=AddObj.subsystems_edit)
@inject
async def get_subsystems_edit(query: types.CallbackQuery, state: FSMContext,
                              application: ApplicationService = Provide[Container.application_service]):
    new_kb = kb.accept().add(kb.exit_button)
    data = await state.get_data()
    if query.data != 'accept' and data['field_five'] == '':
        await state.update_data(field_five=query.data)
        data = await state.get_data()
        msg = await query.message.answer(data['field_five'], reply_markup=new_kb)
        await state.update_data(message_id=msg.message_id)
    elif query.data != 'accept':
        data = await state.get_data()
        await state.update_data(field_five=data['field_five'] + ', ' + query.data)
        new_data = await state.get_data()
        await bot.edit_message_text(new_data['field_five'],
                                    query.message.chat.id,
                                    new_data['message_id'], reply_markup=new_kb)
    else:
        data = await state.get_data()
        if 'admin' not in data:
            await bot.delete_message(
                query.message.chat.id, query.message.message_id)
            await get_data.send_data(query=query, state=state)
            new_kb = kb.sure().add(kb.exit_button)
            await query.message.answer(const.SURE, reply_markup=new_kb)
            await state.set_state(AddObj.sure)
        else:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_five': data['field_five']})
            await query.message.answer(const.CHANGE_SUCCESS)
            await state.finish()
    await query.answer()


def register(dp: Dispatcher):
    dp.register_message_handler(get_section, state=AddObj.section)
    dp.register_message_handler(get_subobject_name,
                                state=AddObj.subobject_name)
    dp.register_message_handler(get_sort, state=AddObj.sort)
    dp.register_message_handler(edit, state=AddObj.edit)
