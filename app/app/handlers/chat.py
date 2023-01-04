from dependency_injector.wiring import inject, Provide

from app.core.container import Container

from app.models.telegram_user import TelegramUser
from app.services.tg_user_service import TelegramUserService

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from app.utils import const
import app.keyboards.inline_keyboard as kb
from app.loader import dp, bot
from loguru import logger
from app.states.base import BaseStates
import app.states.admin_or_moderator as my_states


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
        const.START_SUPPORT,
        reply_markup=kb.start_support
    )


@dp.callback_query_handler(text='start_support')
async def create_ticket(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
    await state.set_state(BaseStates.fio)


def register_start_support_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start_support'])
