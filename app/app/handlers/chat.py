from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.utils import const
from app.states.application import GetApplication, GetComment
from app.keyboards import inline_keyboard
from app.keyboards import clallback_data

from app.services.application import ApplicationService
from app.services.tg_user_service import TelegramUserService

from app.models.application import Application

from loguru import logger

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from app.loader import bot


@inject
async def get_application(
        message: types.Message,
        state: FSMContext,
        tg_user_service: TelegramUserService = Provide[Container.telegram_user_service],
):
    user_id = message.from_user.id
    if not await tg_user_service.user_permission(user_id=user_id):
        return await message.answer(const.HASE_NOT_PERMISSION)
    await message.answer(const.GET_ID)
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
    await state.finish()


@inject
async def change_status(
        callback_query: types.CallbackQuery,
        callback_data: dict,
        application_service: ApplicationService = Provide[Container.application_service],
        tg_user_service: TelegramUserService = Provide[Container.telegram_user_service]
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
    user = await tg_user_service.get_or_create(obj_in=callback_query.from_user.id)
    application = await application_service.update(
        application_id=int(application_id),
        obj_in={
            "recipient_user_id": user.id,
            "recipient_user": user,
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
        tg_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    async with state.proxy() as data:
        application_id = data.get("application_id")
    await message.answer(const.COMMENT_SEND)
    user = await tg_user_service.get_or_create(obj_in=message.from_user.id)
    application = await application_service.update(
        application_id=int(application_id),
        obj_in={
            "recipient_user_id": user.id,
            "recipient_user": user,
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
    await state.finish()


def register_chat_handler(dp: Dispatcher):
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
