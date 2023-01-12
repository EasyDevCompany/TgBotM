from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.utils import const
from app.states.application import GetApplication
from app.keyboards import inline_keyboard
from app.keyboards import clallback_data

from app.services.application import ApplicationService
from app.services.tg_user_service import TelegramUserService

from app.models.application import Application

from loguru import logger

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


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
async def return_application(
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
        one=application.field_one,
        two=application.field_two,
        three=application.field_three,
        four=application.field_four,
        five=application.field_five,
        six=application.field_six,
        seven=application.field_seven,
        eight=application.field_eight,
        nine=application.field_nine
        ), reply_markup=await inline_keyboard.application(application_id=application.id)
    )
    logger.info(f"{application.application_status}")
    await state.finish()


@inject
async def request_done(
        callback_query: types.CallbackQuery,
        callback_data: dict,
        application_service: ApplicationService = Provide[Container.application_service],
        tg_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    await callback_query.message.delete_reply_markup()
    application_id = callback_data.get("data")
    user = await tg_user_service.get_or_create(obj_in=callback_query.from_user.id)
    await application_service.update(
        application_id=int(application_id),
        obj_in={
            "recipient_user_id": user.id,
            "recipient_user": user,
            "application_status": Application.ApplicationStatus.success
        }
    )
    await callback_query.message.answer(const.STATUS_CHANGE_DONE)


def register_chat_handler(dp: Dispatcher):
    dp.register_message_handler(get_application, commands=["application"])
    dp.register_message_handler(return_application, state=GetApplication.application_id)
    dp.register_callback_query_handler(
        request_done,
        clallback_data.application_callback.filter(type="done")
    )
