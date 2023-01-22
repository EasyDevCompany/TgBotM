import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import EditShpmnt
from app.utils import const, get_data
from app.utils import const_edit_shpmnt as text
from app.utils.const import REQUEST_NUMBER, LOAD_DOC, \
    R_NUMBER_ERROR, INCOME_STORAGE, WHAT_EDIT_REQUEST, WHAT_EDIT, FIO, \
    ROLE, NUMBER_REQUEST_IF, ACCEPT_SENDING
from dependency_injector.wiring import inject, Provide
from app.services.application import ApplicationService
from app.core.container import Container
from logger import logger
from app.models.application import Application


@inject
async def skip(query: types. CallbackQuery, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    if 'admin' not in data:
        await state.update_data(field_seven=const.NO_EXTRA)
        await bot.delete_message(query.message.chat.id, query.message.message_id)
        new_kb = kb.sure().add(kb.exit_button)
        await get_data.send_data(query=query, state=state)
        await query.message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(EditShpmnt.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'field_seven': const.NO_EXTRA})
        await query.message.answer(const.CHANGE_SUCCESS)
        ticket = await application.get(data['admin'])
        await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
        await state.finish()


async def get_note(message: types.Message, state: FSMContext):
    if message.content_type != 'document' and message.content_type != 'photo':
        await message.answer(LOAD_DOC)
        await state.set_state(EditShpmnt.note)
    else:
        if message.content_type == 'document':
            await state.update_data(field_one=message.document.file_id)
        elif message.content_type == 'photo':
            await state.update_data(field_one=message.photo[0].file_id)
        await message.answer(REQUEST_NUMBER, reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.number_ticket)


async def get_ticket(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(field_two=message.text)
        await message.answer(text.NUM_INVOICE, reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.number_invoice)
    else:
        await state.set_state(EditShpmnt.number_ticket)
        await message.answer(R_NUMBER_ERROR)


async def get_invoice(message: types.Message, state: FSMContext):
    await state.update_data(field_three=message.text)
    await message.answer(INCOME_STORAGE, reply_markup=kb.exit_kb())
    await state.set_state(EditShpmnt.storage)


async def get_storage(message: types.Message, state: FSMContext):
    await state.update_data(field_four=message.text)
    new_kb = kb.what_edit().add(kb.exit_button)
    await message.answer(WHAT_EDIT_REQUEST, reply_markup=new_kb)
    await state.set_state(EditShpmnt.what_edit)


async def get_changes(query: types.CallbackQuery, state: FSMContext):
    if query.data != 'Другое':
        await state.update_data(field_five=query.data)
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer(const.DESCRIPTION_ERROR,
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.description)
    else:
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await query.message.answer(WHAT_EDIT,
                                   reply_markup=kb.exit_kb())
        await query.message.answer(const.DESCRIPTION_ERROR,
                                   reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.description)


@inject
async def get_another_changes(message: types.Message, state: FSMContext,
                              application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    if 'admin' not in data:
        if 'extra_file' not in data:
            await state.update_data(field_five=message.text)
            await message.answer(const.DESCRIPTION_ERROR,
                                reply_markup=kb.exit_kb())
            await state.set_state(EditShpmnt.description)
        else:
            await state.update_data(field_five=message.text)
            await get_data.send_data(message=message, state=state)
            new_kb = kb.sure().add(kb.exit_button)
            await message.answer(const.SURE, reply_markup=new_kb)
            await state.set_state(EditShpmnt.sure)

    else:
        await application.update(data['admin'], obj_in={'application_status': Application.ApplicationStatus.in_work,
                                                        'field_five': message.text})
        await state.finish()


async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(field_six=message.text)
    new_kb = kb.exit_kb().add(kb.skip_button)
    await message.answer(text.EXTRA_FILE, reply_markup=new_kb)
    await state.set_state(EditShpmnt.extra_files)


@inject
async def get_extra_files(message: types.Message,
                          state: FSMContext):
    data = await state.get_data()
    new_kb = kb.accept().add(kb.send_file_btn)
    if 'field_seven' not in data:
        try:
            await state.update_data(field_seven=message.photo[0].file_id)
        except:
            await state.update_data(field_seven=message.document.file_id)
        await message.answer(ACCEPT_SENDING,
                             reply_markup=new_kb)
        await state.set_state(EditShpmnt.more_extra)
    else:
        try:
            await state.update_data(field_seven=data['field_seven'] + ', ' + message.photo[0].file_id)
        except:
            await state.update_data(field_seven=data['field_seven'] + ', ' + message.document.file_id)
        await message.answer(ACCEPT_SENDING,
                             reply_markup=new_kb)
        await state.set_state(EditShpmnt.more_extra)


@inject
async def more_extra(query: types.CallbackQuery,
                     state: FSMContext,
                     application: ApplicationService = Provide[Container.application_service]):
    if query.data != 'accept':
        new_kb = kb.exit_kb().add(kb.skip_button)
        await query.message.answer(text.EXTRA_FILE, reply_markup=new_kb)
        await state.set_state(EditShpmnt.extra_files)
    else:
        data = await state.get_data()
        if 'admin' not in data:
            await get_data.send_data(query=query, state=state)
            new_kb = kb.sure().add(kb.exit_button)
            await query.message.answer(const.SURE, reply_markup=new_kb)
            await state.set_state(EditShpmnt.sure)
        else:
            if 'field_one' in data:
                black_list = {'admin'}
                new_data = {key: val for key, val in data.items() if key not in black_list}
                unused = ['field_eight', 'field_nine']
                for i in unused:
                    new_data[i] = None
                logger.info(new_data)
                await application.update(data['admin'], obj_in=new_data)
                await query.message.answer(const.CHANGE_SUCCESS)
                ticket = await application.get(data['admin'])
                await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
                await state.finish()
            else:
                await application.update(data['admin'], obj_in={'application_status': Application.ApplicationStatus.in_work,
                                                                'field_seven': data['field_seven']})
                await query.message.answer(const.CHANGE_SUCCESS)
                ticket = await application.get(data['admin'])
                await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
                await state.finish()
    await query.answer()


async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(EditShpmnt.edit)
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
        await query.message.answer(
            const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_ticket')
        await query.message.answer(NUMBER_REQUEST_IF, reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='number_invoice')
        await query.message.answer(text.NUM_INVOICE, reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '7':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='storage')
        await query.message.answer(INCOME_STORAGE, reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '8':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='what_edit')
        new_kb = kb.what_edit().add(kb.exit_button)
        await query.message.answer(WHAT_EDIT_REQUEST, reply_markup=new_kb)
        await state.set_state(EditShpmnt.what_edit_correct)
    elif query.data == '9':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='description')
        await query.message.answer(
            const.DESCRIPTION_ERROR,
            reply_markup=kb.exit_kb())
        await state.set_state(EditShpmnt.edit)
    elif query.data == '10':
        new_kb = kb.exit_kb().add(kb.skip_button)
        await query.message.answer(text.EXTRA_FILE, reply_markup=new_kb)
        await state.set_state(EditShpmnt.extra_files)
    await query.answer()


@inject
async def edit(message: types.Message, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'note':
        try:
            await state.update_data(field_one=message.photo[0].file_id)
        except:
            await state.update_data(field_one=message.document.file_id)
    elif point == 'number_ticket':
        await state.update_data(field_two=message.text)
    elif point == 'number_invoice':
        await state.update_data(field_three=message.text)
    elif point == 'storage':
        await state.update_data(field_four=message.text)
    elif point == 'description':
        await state.update_data(field_six=message.text)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(EditShpmnt.sure)
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
        elif 'field_six' in data:
            await application.update(data['admin'],
                                     obj_in={'application_status': Application.ApplicationStatus.in_work,
                                             'field_six': data['field_six']})
        await message.answer(const.CHANGE_SUCCESS)
        ticket = await application.get(data['admin'])
        await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
        await state.finish()


@inject
async def get_role(query: types.CallbackQuery, state: FSMContext,
                   application: ApplicationService = Provide[Container.application_service]):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    data = await state.get_data()
    if 'admin' not in data:
        new_kb = kb.sure().add(kb.exit_button)
        await get_data.send_data(query=query, state=state)
        await query.message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(EditShpmnt.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'role': data['role']})
        await query.message.answer(const.CHANGE_SUCCESS)
        ticket = await application.get(data['admin'])
        await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
        await state.finish()


@inject
async def get_changes_edit(query: types.CallbackQuery, state: FSMContext,
                               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    if 'admin' not in data:
        if query.data != 'Другое':
            await state.update_data(field_five=query.data)
            await bot.delete_message(query.message.chat.id,
                                     query.message.message_id)
            await get_data.send_data(query=query, state=state)
            new_kb = kb.sure().add(kb.exit_button)
            await query.message.answer(const.SURE, reply_markup=new_kb)
            await state.set_state(EditShpmnt.sure)
        else:
            await bot.delete_message(
                query.message.chat.id, query.message.message_id)
            await query.message.answer(WHAT_EDIT,
                                        reply_markup=kb.exit_kb())
            await state.set_state(EditShpmnt.another_what_edit)
    else:
        if query.data != 'Другое':
            await state.update_data(field_five=query.data)
            await bot.delete_message(query.message.chat.id,
                                        query.message.message_id)
            data = await state.get_data()
            await application.update(data['admin'],
                                        obj_in={'application_status': Application.ApplicationStatus.in_work,
                                                'field_five': data['field_five']})
            await query.message.answer(const.CHANGE_SUCCESS)
            ticket = await application.get(data['admin'])
            await bot.send_message(ticket.recipient_user.user_id, f'{const.USER_EDIT_TICKET}' + f' №А{ticket.id}')
            await state.finish()
        else:
            await bot.delete_message(
                query.message.chat.id, query.message.message_id)
            await query.message.answer(WHAT_EDIT,
                                        reply_markup=kb.exit_kb())
            await state.set_state(EditShpmnt.another_what_edit)


def register(dp: Dispatcher):
    dp.register_message_handler(
        get_note, state=EditShpmnt.note, content_types=['any'])
    dp.register_message_handler(get_ticket, state=EditShpmnt.number_ticket)
    dp.register_message_handler(get_invoice, state=EditShpmnt.number_invoice)
    dp.register_message_handler(get_storage, state=EditShpmnt.storage)
    dp.register_message_handler(
        get_another_changes, state=EditShpmnt.another_what_edit)
    dp.register_message_handler(get_description, state=EditShpmnt.description)
    dp.register_message_handler(
        get_extra_files,
        state=EditShpmnt.extra_files, content_types=['any'])
    dp.register_message_handler(edit,
                                state=EditShpmnt.edit,
                                content_types=['any'])
    dp.register_callback_query_handler(skip, text='skip', state=EditShpmnt.extra_files)
    dp.register_callback_query_handler(get_changes, state=EditShpmnt.what_edit)
    dp.register_callback_query_handler(correct, state=EditShpmnt.sure)
    dp.register_callback_query_handler(get_role, state=EditShpmnt.edit)
    dp.register_callback_query_handler(get_changes_edit, state=EditShpmnt.what_edit_correct)
    dp.register_callback_query_handler(more_extra, state=EditShpmnt.more_extra)
