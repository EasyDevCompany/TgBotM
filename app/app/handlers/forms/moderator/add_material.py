import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import AddMat
from app.utils import const, get_data
from app.utils.const import EDIT_STORAGE, LOAD_DOC, EXCEL_DOC, SURPLUS, LOAD_EXCEL, RESERVE, FIO, ROLE
from dependency_injector.wiring import inject, Provide
from app.services.application import ApplicationService
from app.core.container import Container
from app.models.application import Application


async def get_note(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(field_one=message.document.file_id)
        await message.answer(EDIT_STORAGE,
                             reply_markup=kb.exit_kb())
        await state.set_state(AddMat.storage)
    else:
        await message.answer(LOAD_DOC)
        await state.set_state(AddMat.note)


async def get_storage(message: types.Message, state: FSMContext):
    await state.update_data(field_two=message.text)
    await message.answer(EXCEL_DOC,
                         reply_markup=kb.exit_kb())
    await state.set_state(AddMat.excel)


async def get_excel(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(field_three=message.document.file_id)
        new_kb = kb.reserve_or_leave().add(kb.exit_button)
        await message.answer(SURPLUS, reply_markup=new_kb)
        await state.set_state(AddMat.myc)
    else:
        await message.answer(LOAD_EXCEL)
        await state.set_state(AddMat.excel)


@inject
async def get_choise(query: types.CallbackQuery, state: FSMContext,
                     application: ApplicationService = Provide[Container.application_service]):
    await state.update_data(field_four=query.data)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    if query.data == 'Резервировать':
        await query.message.answer(RESERVE,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddMat.obj)
    elif query.data == 'Оставить на своб. остатках':
        new_kb = kb.sure().add(kb.exit_button)
        await state.update_data(field_five='--')
        data = await state.get_data()
        if 'admin' not in data:
            await get_data.send_data(query=query, state=state)
            await query.message.answer(const.SURE, reply_markup=new_kb)
            await state.set_state(AddMat.sure)
        else:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_four': data['field_four'],
                                             'field_five': data['field_five']})
            await query.message.answer(const.CHANGE_SUCCESS)
            await state.finish()


@inject
async def get_obj(message: types.Message, state: FSMContext,
                  application: ApplicationService = Provide[Container.application_service]):
    await state.update_data(field_five=message.text)
    new_kb = kb.sure().add(kb.exit_button)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(message=message, state=state)
        await message.answer(const.SURE,
                             reply_markup=new_kb)
        await state.set_state(AddMat.sure)
    else:
        if 'field_one' in data:
            black_list = {'admin'}
            new_data = {key: val for key, val in data.items() if key not in black_list}
            unused = ['field_six', 'field_seven', 'field_eight', 'field_nine']
            for i in unused:
                new_data[i] = None
            await application.update(data['admin'], obj_in=new_data)
            await message.answer(const.CHANGE_SUCCESS)
            await state.finish()
        else:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_four': data['field_four'],
                                             'field_five': data['field_five']})
            await message.answer(const.CHANGE_SUCCESS)
            await state.finish()


async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(AddMat.edit)
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
        await state.update_data(change='note')
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage')
        await query.message.answer(EDIT_STORAGE,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='excel')
        await query.message.answer(
            EXCEL_DOC,
            reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='choise')
        new_kb = kb.reserve_or_leave().add(kb.exit_button)
        await query.message.answer(SURPLUS, reply_markup=new_kb)
        await state.set_state(AddMat.myc)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='obj')
        await query.message.answer(RESERVE,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddMat.edit)
    await query.answer()


@inject
async def edit(message: types.Message, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'note':
        await state.update_data(field_one=message.document.file_id)
    elif point == 'storage':
        await state.update_data(field_two=message.text)
    elif point == 'excel':
        await state.update_data(field_three=message.document.file_id)
    elif point == 'obj':
        await state.update_data(field_five=message.text)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(AddMat.sure)
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
        await message.answer(const.CHANGE_SUCCESS)
        await state.finish()


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
        await state.set_state(AddMat.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'role': data['role']})
        await query.message.answer(const.CHANGE_SUCCESS)
        await state.finish()


def register(dp: Dispatcher):
    dp.register_message_handler(get_note,
                                state=AddMat.note, content_types=['any'])
    dp.register_message_handler(get_storage, state=AddMat.storage)
    dp.register_message_handler(get_excel,
                                state=AddMat.excel, content_types=['any'])
    dp.register_message_handler(get_obj, state=AddMat.obj)
    dp.register_message_handler(edit,
                                state=AddMat.edit,
                                content_types=['text', 'document'])
    dp.register_callback_query_handler(get_choise, state=AddMat.myc)
    dp.register_callback_query_handler(correct, state=AddMat.sure)
    dp.register_callback_query_handler(get_role, state=AddMat.edit)
