import keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.base import BaseStates
from states.tgbot_states import EditViewWork
from utils import const, get_data
from dependency_injector.wiring import inject, Provide
from app.services.application import ApplicationService
from app.core.container import Container
from app.models.application import Application


async def get_edit_sub_object_type_work(message: types.Message,
                                        state: FSMContext):
    await state.update_data(field_one=message.text)
    await message.answer('Укажите вид работ',
                         reply_markup=kb.exit_kb())
    await state.set_state(EditViewWork.edit_type_work)


async def get_edit_type_work(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    await message.answer('Укажите сортировку',
                         reply_markup=kb.exit_kb())
    await state.set_state(EditViewWork.edit_sort)


async def get_edit_sort(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    new_kb = kb.add_subsystem_kb().add(kb.exit_button)
    await message.answer(
        'Укажите подсистемы, в которых вид работ будет отображаться',
        reply_markup=new_kb)
    await state.set_state(EditViewWork.edit_sub_systems)


@dp.callback_query_handler(state=EditViewWork.edit_sub_systems)
async def get_subsystems(query: types.CallbackQuery, state: FSMContext):
    new_kb = kb.accept().add(kb.exit_button)
    data = await state.get_data()
    if query.data != 'accept' and 'field_four' not in data:
        await state.update_data(field_four=query.data)
        data = await state.get_data()
        msg = await query.message.answer(
            data['field_four'], reply_markup=new_kb)
        await state.update_data(message_id=msg.message_id)
    elif query.data != 'accept':
        data = await state.get_data()
        await state.update_data(
            field_four=data['field_four'] + ', ' + query.data)
        new_data = await state.get_data()
        await bot.edit_message_text(new_data['field_four'],
                                    query.message.chat.id,
                                    new_data['message_id'],
                                    reply_markup=new_kb)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await get_data.send_data(query=query, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await query.message.answer(const.SURE,
                                   reply_markup=new_kb)
        await state.set_state(EditViewWork.sure)
    await query.answer()


@dp.callback_query_handler(state=EditViewWork.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(EditViewWork.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(EditViewWork.edit)
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
        await state.update_data(change='sub_object_type_work')
        await query.message.answer(
            const.EDIT_SUBOBJECT_TYPE_WORK, reply_markup=kb.exit_kb())
        await state.set_state(EditViewWork.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='type_work')
        await query.message.answer('Укажите вид работ',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditViewWork.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='sort')
        await query.message.answer('Укажите сортировку',
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditViewWork.edit)
    elif query.data == '7':
        await state.update_data(field_four='')
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        new_kb = kb.add_subsystem_kb().add(kb.exit_button)
        await query.message.answer(
            'Укажите подсистемы, в которых вид работ будет отображаться',
            reply_markup=new_kb)
        await state.set_state(EditViewWork.subsystems_edit)
    await query.answer()


@inject
async def edit(message: types.Message, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'sub_object_type_work':
        await state.update_data(field_one=message.text)
    elif point == 'type_work':
        await state.update_data(field_two=message.text)
    elif point == 'sort':
        await state.update_data(field_three=message.text)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(EditViewWork.sure)
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
        await message.answer(const.CHANGE_SUCCESS)
        await state.finish()


@dp.callback_query_handler(state=EditViewWork.edit)
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
        await state.set_state(EditViewWork.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'role': data['role']})
        await query.message.answer(const.CHANGE_SUCCESS)
        await state.finish()


@dp.callback_query_handler(state=EditViewWork.subsystems_edit)
@inject
async def get_subsystems_edit(query: types.CallbackQuery, state: FSMContext,
                              application: ApplicationService = Provide[Container.application_service]):
    new_kb = kb.accept().add(kb.exit_button)
    data = await state.get_data()
    if query.data != 'accept' and data['field_four'] == '':
        await state.update_data(field_four=query.data)
        data = await state.get_data()
        msg = await query.message.answer(data['field_four'], reply_markup=new_kb)
        await state.update_data(message_id=msg.message_id)
    elif query.data != 'accept':
        data = await state.get_data()
        await state.update_data(field_four=data['field_four'] + ', ' + query.data)
        new_data = await state.get_data()
        await bot.edit_message_text(new_data['field_four'],
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
            await state.set_state(EditViewWork.sure)
        else:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_four': data['field_four']})
            await query.message.answer(const.CHANGE_SUCCESS)
            await state.finish()
    await query.answer()


def register(dp: Dispatcher):
    dp.register_message_handler(get_edit_sub_object_type_work,
                                state=EditViewWork.edit_sub_object_type_work)
    dp.register_message_handler(get_edit_type_work,
                                state=EditViewWork.edit_type_work)
    dp.register_message_handler(get_edit_sort, state=EditViewWork.edit_sort)
    dp.register_message_handler(edit, state=EditViewWork.edit)
