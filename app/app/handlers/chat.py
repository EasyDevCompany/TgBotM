from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from dependency_injector.wiring import Provide, inject
from loader import bot
from logger import logger
from app.states.application import GetApplication, GetComment, EditApplication
import app.keyboards.inline_keyboard as kb
import app.states.tgbot_states as my_states
from app.core.config import settings
from app.core.container import Container
from app.models.application import Application
from app.services.application import ApplicationService
from app.services.tg_user_service import TelegramUserService
from app.states.base import Admin
from app.utils import const, get_data
from app.utils.const import NO_NEW_BIDS, NEW_COMMENT, SELECT_ITEM, BID_ACCEPT, BID_PROCESSED
from app.models.telegram_user import UserType
from app.keyboards import clallback_data
from app.keyboards import inline_keyboard
from aiogram.utils.exceptions import BadRequest


@inject
async def get_application(
        message: types.Message,
        state: FSMContext,
        tg_user_service: TelegramUserService = Provide[Container.telegram_user_service],
):
    user_id = message.from_user.id
    if not await tg_user_service.user_permission(user_id=user_id):
        return await message.answer(const.HASE_NOT_PERMISSION)
    await message.answer(const.GET_ID, reply_markup=inline_keyboard.cancel_keyboard)
    await state.set_state(GetApplication.application_id)


@inject
async def application_view(
        message: types.Message,
        state: FSMContext,
        application_service: ApplicationService = Provide[Container.application_service]
):
    if not message.text.isdigit():
        return await message.answer(const.NOT_TEXT)
    user_id = message.from_user.id
    application = await application_service.get_application_for_user(
        user_id=user_id,
        application_id=int(message.text)
    )
    if application is None:
        return await message.answer(const.APPLICATION_ERROR)
    await message.answer(const.SEND_APPLICATION.format(
        application_id=application.id,
        role=application.role,
        request_type=application.request_type,
        one=F"1) {application.field_one}",
        two=f"2) {application.field_two}",
        three=f"3) {application.field_three}",
        four="" if application.field_four is None else f"4) {application.field_four}",
        five="" if application.field_five is None else f"5) {application.field_five}",
        six="" if application.field_six is None else f"6) {application.field_six}",
        seven="" if application.field_seven is None else f"7) {application.field_seven}",
        eight="" if application.field_eight is None else f"8) {application.field_eight}",
        nine="" if application.field_nine is None else f"9) {application.field_nine}"
        ), reply_markup=await inline_keyboard.application(application_id=application.id)
    )
    user_id = message.from_user.id
    if application.request_type == Application.RequestType.change_status_application:
        try:
            await bot.send_document(user_id, application.field_one)
        except BadRequest as _exc:
            logger.error(_exc)
    elif application.request_type == Application.RequestType.add_naming:
        try:
            await bot.send_document(user_id, application.field_six)
        except BadRequest as _exc:
            logger.error(_exc)
    elif application.request_type == Application.RequestType.add_material:
        try:
            await bot.send_document(user_id, application.field_one)
            await bot.send_document(user_id, application.field_three)
        except BadRequest as _exc:
            logger.error(_exc)
    elif application.request_type == Application.RequestType.add_edo:
        try:
            await bot.send_document(user_id, application.field_one)
            await bot.send_document(user_id, application.field_two)
            await bot.send_document(user_id, application.field_three)
            await bot.send_document(user_id, application.field_five)
        except BadRequest as _exc:
            logger.error(_exc)
    elif application.request_type == Application.RequestType.open_edo:
        try:
            await bot.send_document(user_id, application.field_one)
        except BadRequest as _exc:
            logger.error(_exc)
    elif application.request_type == Application.RequestType.edit_some_moving:
        try:
            await bot.send_document(user_id, application.field_one)
        except BadRequest as _exc:
            logger.error(_exc)
    elif application.request_type == Application.RequestType.adjustment_of_supplies:
        try:
            await bot.send_document(user_id, application.field_one)
            await bot.send_document(user_id, application.field_seven)
        except BadRequest as _exc:
            logger.error(_exc)
    await state.finish()


@inject
async def change_status(
        callback_query: types.CallbackQuery,
        callback_data: dict,
        application_service: ApplicationService = Provide[Container.application_service],
):
    await callback_query.message.delete_reply_markup()
    application_id = callback_data.get("data")
    data = callback_data.get("type")
    if data == "in_work":
        status = Application.ApplicationStatus.in_work
        message = "Взята в работу!"
    else:
        status = Application.ApplicationStatus.success
        message = "Заявка обработана!"
    application = await application_service.update(
        application_id=int(application_id),
        user_id=callback_query.from_user.id,
        obj_in={
            "application_status": status
        }
    )
    await callback_query.message.answer(const.STATUS_CHANGE_DONE.format(message=message))
    await bot.send_message(
        application.sender_user.user_id,
        const.MESSAGE_FOR_SENDER.format(
            application_id=int(application_id),
            application_type=application.request_type
        )
    )


@inject
async def return_application(
        callback_query: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext
):
    await callback_query.message.delete_reply_markup()
    async with state.proxy() as data:
        data["application_id"] = callback_data.get("data")
    await callback_query.message.answer(const.RETURN_COMMENT)
    await state.set_state(GetComment.comment)


@inject
async def get_comment_send_message(
        message: types.Message,
        state: FSMContext,
        application_service: ApplicationService = Provide[Container.application_service],
):
    async with state.proxy() as data:
        application_id = data.get("application_id")
    await message.answer(const.COMMENT_SEND)
    application = await application_service.update(
        application_id=int(application_id),
        user_id=message.from_user.id,
        obj_in={
            "application_status": Application.ApplicationStatus.return_application
        }
    )
    await bot.send_message(
        application.sender_user.user_id,
        const.MESSAGE_FOR_SENDER_IF_RETURN.format(
            application_id=application_id,
            role=application.role,
            request_type=application.request_type,
            one=F"1) {application.field_one}",
            two=f"2) {application.field_two}",
            three=f"3) {application.field_three}",
            four="" if application.field_four is None else f"4) {application.field_four}",
            five="" if application.field_five is None else f"5) {application.field_five}",
            six="" if application.field_six is None else f"6) {application.field_six}",
            seven="" if application.field_seven is None else f"7) {application.field_seven}",
            eight="" if application.field_eight is None else f"8) {application.field_eight}",
            nine="" if application.field_nine is None else f"9) {application.field_nine}"
        ), reply_markup=await inline_keyboard.edit(application_id=application_id)
    )
    await bot.send_message(application.sender_user.user_id, f"Комментарий к заявке: {message.text}")
    await state.finish()


async def cancel_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.delete()
    await callback_query.message.answer('Отменено!')


@inject
async def edit_application(
        callback_query: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        application_service: ApplicationService = Provide[Container.application_service]
):
    await callback_query.message.delete_reply_markup()
    application_id = callback_data.get("data")
    application = await application_service.get(application_id=application_id)
    if application.field_four is None:
        field_count = 3
    elif application.field_five is None:
        field_count = 4
    elif application.field_six is None:
        field_count = 5
    elif application.field_seven is None:
        field_count = 6
    elif application.field_eight is None:
        field_count = 7
    elif application.field_nine is None:
        field_count = 8
    else:
        field_count = 9
    async with state.proxy() as data:
        data["application_id"] = application_id
    await callback_query.message.answer(
        const.CHOOSE_FIELD,
        reply_markup=await inline_keyboard.edit_field(field_count=field_count)
    )
    await state.set_state(EditApplication.field)


async def get_field(
        callback_query: types.CallbackQuery,
        state: FSMContext,
):
    edited_field = callback_query.data
    async with state.proxy() as data:
        data["edited_field"] = edited_field
    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(const.WHAT_EDIT)
    await state.set_state(EditApplication.new_text)


@inject
async def edited_and_save(
        message: types.Message,
        state: FSMContext,
        application_service: ApplicationService = Provide[Container.application_service]
):
    async with state.proxy() as data:
        application_id = data.get("application_id")
        edited_field = data.get("edited_field")
    if int(edited_field) == 1:
        obj_in = {"field_one": message.text}
    elif int(edited_field) == 2:
        obj_in = {"field_two": message.text}
    elif int(edited_field) == 3:
        obj_in = {"field_three": message.text}
    elif int(edited_field) == 4:
        obj_in = {"field_four": message.text}
    elif int(edited_field) == 5:
        obj_in = {"field_five": message.text}
    elif int(edited_field) == 6:
        obj_in = {"field_six": message.text}
    elif int(edited_field) == 7:
        obj_in = {"field_seven": message.text}
    elif int(edited_field) == 8:
        obj_in = {"field_eight": message.text}
    else:
        obj_in = {"field_nine": message.text}
    application = await application_service.update(
        application_id=int(application_id),
        obj_in=obj_in
    )
    await message.answer(const.CHANGE_SAVED)
    await bot.send_message(
        application.recipient_user.user_id,
        const.SENDER_CHANGE_APPLICATION_MESSAGE.format(
            application_id=application_id
        )
    )
    await state.finish()


@inject
async def admin(message: types.Message,
                application: ApplicationService = Provide[Container.application_service],
                tg_user_service: TelegramUserService = Provide[Container.telegram_user_service]):
    if not await tg_user_service.check_permission_for_user(user_id=message.from_user.id,
                                                           user_type=UserType.administrator):
        return await message.answer(const.HASE_NOT_PERMISSION)
    tickets = await application.applications_for(
        UserType.administrator)
    new_tickets = []
    for ticket in tickets:
        if ticket.recipient_user is not None:
            if ticket.application_status != Application.ApplicationStatus.success and str(
                    ticket.recipient_user.user_id) == str(message.from_user.id):
                new_tickets.append(ticket)
    try:
        await kb.admin_btns_tickets(message=message, tickets=new_tickets)
    except:
        await message.answer(const.NO_NEW_BIDS)


@inject
async def moder(message: types.Message,
                application: ApplicationService = Provide[Container.application_service],
                tg_user_service: TelegramUserService = Provide[Container.telegram_user_service]):
    if not await tg_user_service.check_permission_for_user(user_id=message.from_user.id,
                                                           user_type=UserType.technical_support):
        return await message.answer(const.HASE_NOT_PERMISSION)
    tickets = await application.applications_for(
        UserType.technical_support)
    new_tickets = []
    for ticket in tickets:
        if ticket.recipient_user is not None:
            if ticket.application_status != Application.ApplicationStatus.success and str(
                    ticket.recipient_user.user_id) == str(message.from_user.id):
                new_tickets.append(ticket)
    try:
        await kb.moder_btns_tickets(message=message, tickets=new_tickets)
    except:
        await message.answer(const.NO_NEW_BIDS)


@inject
async def admin_page_callback(call: types.CallbackQuery,
                              application: ApplicationService = Provide[Container.application_service]):
    page = int(call.data.split('#')[1])
    tickets = await application.applications_for(
        UserType.administrator)
    new_tickets = []
    for ticket in tickets:
        if ticket.recipient_user is not None:
            if ticket.application_status != Application.ApplicationStatus.success and str(
                    ticket.recipient_user.user_id) == str(call.from_user.id):
                new_tickets.append(ticket)
    await kb.admin_btns_tickets(call.message, new_tickets, page)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@inject
async def moder_page_callback(call: types.CallbackQuery,
                              application: ApplicationService = Provide[Container.application_service]):
    page = int(call.data.split('#')[1])
    tickets = await application.applications_for(
        UserType.technical_support)
    new_tickets = []
    for ticket in tickets:
        if ticket.recipient_user is not None:
            if ticket.application_status != Application.ApplicationStatus.success and str(
                    ticket.recipient_user.user_id) == str(call.from_user.id):
                new_tickets.append(ticket)
    await kb.moder_btns_tickets(call.message, new_tickets, page)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@inject
async def comeback(query: types.CallbackQuery, callback_data: dict,
                   state: FSMContext,
                   application: ApplicationService = Provide[Container.application_service]):
    number = callback_data['id']
    user_id = callback_data['user_id']
    await application.update(number,
                             user_id=query.from_user.id,
                             obj_in={'application_status': Application.ApplicationStatus.return_application})
    await state.update_data(number=number, user_id=user_id)
    if str(query.message.chat.id) == str(settings.ADMIN_CHAT_ID) or str(query.message.chat.id) == str(settings.SUPPORT_CHAT_ID):
        await bot.delete_message(query.message.chat.id, query.message.message_id)
        ticket = await application.get(number)
        await get_data.send_data_channel(ticket=ticket, user_id=query.from_user.id, state=state)
    else:
        await query.message.answer(NEW_COMMENT)
        await state.set_state(Admin.comment)
    await query.answer()


@inject
async def get_comment(message: types.Message, state: FSMContext,
                      application: ApplicationService = Provide[Container.application_service]):
    admin_data = await state.get_data()
    ticket = await application.get(admin_data['number'])
    await bot.send_message(admin_data['user_id'], message.text)
    await get_data.send_data_channel(ticket=ticket, user_id=admin_data['user_id'], edit=True, state=state)
    await state.finish()


@inject
async def user_edit_ticket(query: types.CallbackQuery,
                           state: FSMContext,
                           callback_data: dict,
                           application: ApplicationService = Provide[Container.application_service]):
    await state.finish()
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
                     'sender_user',
                     'recipient_user_id', 'recipient_user'] and v is not None:
            count_buttons += 1
    await state.update_data(admin=number)
    if ticket.request_type == 'Добавление объекта в ЭДО':
        await state.set_state(my_states.AddObjAdm.sure)
    elif ticket.request_type == 'Корректировка поставок':
        await state.set_state(my_states.EditShpmnt.sure)
    elif ticket.request_type == 'Редактирование некорректного перемещения':
        await state.set_state(my_states.EditMoveAdm.sure)
    elif ticket.request_type == 'Открытие доступов Эдо для сотрудников':
        await state.set_state(my_states.OpenAcs.sure)
    elif ticket.request_type == 'Смена статуса заявки':
        await state.set_state(my_states.ChangeStatus.sure)
    elif ticket.request_type == 'Добавление материалов на свободный остаток':
        await state.set_state(my_states.AddMat.sure)
    elif ticket.request_type == 'Добавление коэффицента пересчета':
        await state.set_state(my_states.AddCoef.sure)
    elif ticket.request_type == 'Корректировки склада в заявке':
        await state.set_state(my_states.UpdateStorage.sure)
    elif ticket.request_type == 'Добавление наименований':
        await state.set_state(my_states.AddNaming.sure)
    elif ticket.request_type == 'Редактирование видов работ':
        await state.set_state(my_states.EditViewWork.sure)
    elif ticket.request_type == 'Добавление видов работ':
        await state.set_state(my_states.AddViewWork.sure)
    elif ticket.request_type == 'Редактирование подобъектов':
        await state.set_state(my_states.UpdateSubObject.sure)
    elif ticket.request_type == 'Корректировка оформленной накладной':
        await state.set_state(my_states.AdjInv.sure)
    elif ticket.request_type == 'Добавление подобъектов':
        await state.set_state(my_states.AddObj.sure)
    logger.info(await state.get_state())
    await query.message.answer(
        SELECT_ITEM,
        reply_markup=kb.another_genmarkup(count_buttons))
    await query.answer()


@inject
async def take_to_work(query: types.CallbackQuery,
                       callback_data: dict,
                       application: ApplicationService = Provide[Container.application_service]):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    number = callback_data['id']
    user_id = callback_data['user_id']
    await application.update(
        number, obj_in={
            'application_status': Application.ApplicationStatus.in_work},
        user_id=query.from_user.id)
    await bot.send_message(user_id, BID_ACCEPT)
    await query.answer()


@inject
async def success(query: types.CallbackQuery,
                  callback_data: dict,
                  application: ApplicationService = Provide[Container.application_service]):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    number = callback_data['id']
    user_id = callback_data['user_id']
    await application.update(
        number, obj_in={
            'application_status': Application.ApplicationStatus.success})
    await bot.send_message(user_id, BID_PROCESSED)
    await query.answer()


def register_chat_handler(dp: Dispatcher):
    dp.register_message_handler(admin, Command('admin'))
    dp.register_message_handler(get_comment, state=Admin.comment)
    dp.register_callback_query_handler(comeback, kb.cb_admin.filter(action='comeback'))
    dp.register_callback_query_handler(admin_page_callback, lambda call: call.data.split('#')[0] == 'ticket')
    dp.register_callback_query_handler(moder_page_callback, lambda call: call.data.split('#')[0] == 'moderticket')
    dp.register_callback_query_handler(user_edit_ticket, kb.cb_admin.filter(action='edit'))
    dp.register_callback_query_handler(take_to_work, kb.cb_admin.filter(action='take_to_work'))
    dp.register_callback_query_handler(success, kb.cb_admin.filter(action='success'))
    dp.register_message_handler(moder, Command('moderator'))
    dp.register_message_handler(get_application, commands=["application"])
    dp.register_message_handler(application_view, state=GetApplication.application_id)
    dp.register_callback_query_handler(
        change_status,
        clallback_data.application_callback.filter(type="done")
    )
    dp.register_callback_query_handler(
        change_status,
        clallback_data.application_callback.filter(type="in_work")
    )
    dp.register_callback_query_handler(
        return_application,
        clallback_data.application_callback.filter(type="return")
    )
    dp.register_message_handler(get_comment_send_message, state=GetComment.comment)
    dp.register_callback_query_handler(cancel_button, text='cancel', state='*')
    dp.register_callback_query_handler(
        edit_application,
        clallback_data.application_callback.filter(type="edit")
    )
    dp.register_callback_query_handler(get_field, state=EditApplication.field)
    dp.register_message_handler(edited_and_save, state=EditApplication.new_text)


