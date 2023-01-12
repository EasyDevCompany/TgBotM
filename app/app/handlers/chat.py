from aiogram.dispatcher.filters import Command
import app.keyboards.inline_keyboard as kb
from loader import dp, bot
from aiogram import types, Dispatcher
from app.services.application import ApplicationService
from dependency_injector.wiring import inject, Provide
from app.models.application import Application
from states.base import Admin
import states.tgbot_states as my_states
from aiogram.dispatcher import FSMContext
from logger import logger

from app.core.container import Container


@inject
async def admin(message: types.Message,
                application: ApplicationService = Provide[Container.application_service]):
    try:
        tickets = await application.applications_for(
            Application.RequestAnswered.admin)
        await kb.admin_btns_tickets(message=message, tickets=tickets)
    except:
        await message.answer('Нет новых заявок')


@inject
async def moder(message: types.Message,
                application: ApplicationService = Provide[Container.application_service]):
    try:
        tickets = await application.applications_for(
            Application.RequestAnswered.moderator)
        await kb.moder_btns_tickets(message=message, tickets=tickets)
    except:
        await message.answer('Нет новых заявок')


@dp.callback_query_handler(lambda call: call.data.split('#')[0]=='ticket')
@inject
async def admin_page_callback(call: types.CallbackQuery,
                              application: ApplicationService = Provide[Container.application_service]):
    page = int(call.data.split('#')[1])
    tickets = await application.applications_for(
        Application.RequestAnswered.admin)
    await call.message.answer(call.data)
    await kb.admin_btns_tickets(call.message, tickets, page)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(lambda call: call.data.split('#')[0]=='moderticket')
@inject
async def moder_page_callback(call: types.CallbackQuery,
                              application: ApplicationService = Provide[Container.application_service]):
    page = int(call.data.split('#')[1])
    tickets = await application.applications_for(
        Application.RequestAnswered.moderator)
    await kb.moder_btns_tickets(call.message, tickets, page)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(kb.cb_admin.filter(action='comeback'))
async def comeback(query: types.CallbackQuery,
                   callback_data: dict,
                   state: FSMContext):
    number = callback_data['id']
    user_id = callback_data['user_id']
    await state.update_data(number=number, user_id=user_id)
    await query.message.answer('Введите комментарий')
    await state.set_state(Admin.comment)


@inject
async def get_comment(message: types.Message, state: FSMContext,
                      application: ApplicationService = Provide[Container.application_service]):
    admin_data = await state.get_data()
    ticket = await application.get(admin_data['number'])
    msg = ''
    msg += f'1){ticket.name}\n'
    msg += f'2){ticket.role}\n'
    msg += f'3){ticket.request_type}\n'
    msg += f'4){ticket.field_one}\n'
    msg += f'5){ticket.field_two}\n'
    msg += f'6){ticket.field_three}\n'
    if ticket.field_four is not None:
        msg += f'7){ticket.field_four}\n'
    if ticket.field_five is not None:
        msg += f'8){ticket.field_five}\n'
    if ticket.field_six is not None:
        msg += f'9){ticket.field_six}\n'
    if ticket.field_seven is not None:
        msg += f'10){ticket.field_seven}\n'
    if ticket.field_eight is not None:
        msg += f'11){ticket.field_eight}\n'
    if ticket.field_nine is not None:
        msg += f'12){ticket.field_nine}\n'
    await bot.send_message(admin_data['user_id'],
                           msg, reply_markup=kb.user_edit(ticket))
    await bot.send_message(admin_data['user_id'], message.text)
    await state.finish()


@dp.callback_query_handler(kb.cb_admin.filter(action='edit'))
@inject
async def user_edit_ticket(query: types.CallbackQuery,
                           state: FSMContext,
                           callback_data: dict,
                           application: ApplicationService = Provide[Container.application_service]):
    number = callback_data['id']
    await application.update(
        number, obj_in={
            'application_status': Application.ApplicationStatus.return_application})
    ticket = await application.get(number)
    count_buttons = 0
    for k, v in ticket.__dict__.items():
        if k not in ['id', 'date',
                     'application_status',
                     'request_answered',
                     '_sa_instance_state',
                     'sender_user_id',
                     'recipient_user_id'] and v is not None:
            count_buttons += 1
    await state.update_data(admin=number)
    if ticket.request_type == 'add_edo':
        await state.set_state(my_states.AddObjAdm.sure)
    elif ticket.request_type == 'adjustment_of_supplies':
        await state.set_state(my_states.EditShpmnt.sure)
    elif ticket.request_type == 'edit_some_moving':
        await state.set_state(my_states.EditMoveAdm.sure)
    elif ticket.request_type == 'open_edo':
        await state.set_state(my_states.OpenAcs.sure)
    elif ticket.request_type == 'change_status_application':
        await state.set_state(my_states.ChangeStatus.sure)
    elif ticket.request_type == 'add_material':
        await state.set_state(my_states.AddMat.sure)
    elif ticket.request_type == 'conversion_factor':
        await state.set_state(my_states.AddCoef.sure)
    elif ticket.request_type == 'warehouse_adjustments':
        await state.set_state(my_states.UpdateStorage.sure)
    elif ticket.request_type == 'add_naming':
        await state.set_state(my_states.AddNaming.sure)
    elif ticket.request_type == 'edit_view_job':
        await state.set_state(my_states.EditViewWork.sure)
    elif ticket.request_type == 'add_view_job':
        await state.set_state(my_states.AddViewWork.sure)
    elif ticket.request_type == 'edit_subobject':
        await state.set_state(my_states.UpdateSubObject.sure)
    elif ticket.request_type == 'adjustment_invoice':
        await state.set_state(my_states.AdjInv.sure)
    elif ticket.request_type == 'add_subobject':
        await state.set_state(my_states.AddObj.sure)
    await query.message.answer(
        'Выбери пункт редактирования',
        reply_markup=kb.another_genmarkup(count_buttons))


@dp.callback_query_handler(kb.cb_admin.filter(action='take_to_work'))
@inject
async def take_to_work(query: types.CallbackQuery,
                       callback_data: dict,
                       application: ApplicationService = Provide[Container.application_service]):
    number = callback_data['id']
    user_id = callback_data['user_id']
    await application.update(
        number, obj_in={
            'application_status': Application.ApplicationStatus.in_work},
        user_id=query.from_user.id)
    await bot.send_message(user_id, 'Ваша заявка принята')


@dp.callback_query_handler(kb.cb_admin.filter(action='success'))
@inject
async def success(query: types.CallbackQuery,
                  callback_data: dict,
                  application: ApplicationService = Provide[Container.application_service]):
    number = callback_data['id']
    user_id = callback_data['user_id']
    await application.update(
        number, obj_in={
            'application_status': Application.ApplicationStatus.success})
    await bot.send_message(user_id, 'Ваша заявка обработана')


def register_chat_handler(dp: Dispatcher):
    dp.register_message_handler(admin, Command('admin'))
    dp.register_message_handler(moder, Command('moderator'))
    dp.register_message_handler(get_comment, state=Admin.comment)
