from dependency_injector.wiring import inject, Provide

from app.core.container import Container

from app.models.telegram_user import TelegramUser
from app.services.tg_user_service import TelegramUserService

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from app.utils import const
import keyboards.inline_keyboard as kb
from states.tgbot_states import EditMove
from loader import dp
from loguru import logger


@inject
async def start(
        message: types.Message,
        tg_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    await tg_user_service.get_or_create(
        obj_in={
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "user_type": TelegramUser.UserType.employee
        }
    )
    await message.answer(
        const.START_MESSAGE,
        reply_markup=kb.inline_keyboard.start_work
    )


@dp.callback_query_handler(text='create_ticket')
async def create_ticket(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Введите ФИО')
    await state.set_state(EditMove.name)


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())

