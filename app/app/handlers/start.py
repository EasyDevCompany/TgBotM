from dependency_injector.wiring import inject, Provide

from core.container import Container

from models.telegram_user import TelegramUser
from services.tg_user_service import TelegramUserService

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from utils import const
import keyboards.inline_keyboard as kb
from loader import dp
from loguru import logger
from states.base import BaseStates
import states.tgbot_states as my_states


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
        reply_markup=kb.start_work
    )


@dp.callback_query_handler(text='start_work')
async def create_ticket(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Введите ФИО')
    await state.set_state(BaseStates.fio)


async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Выберите свою роль',
                         reply_markup=kb.choose_your_role())
    await state.set_state(BaseStates.role)


@dp.callback_query_handler(state=BaseStates.role)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(role=query.data)
    print(await state.get_data())
    await query.message.answer('Выберите тип запроса',
                               reply_markup=kb.main_kb())
    await state.set_state(BaseStates.request_type)


@dp.callback_query_handler(state=BaseStates.request_type)
async def get_request_type(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(request_type=query.data)
    print(query.data)
    if query.data == 'add_subobject':
        await query.message.answer(const.ADD_SUBOBJECTS,
                                   reply_markup=kb.add_subobjects_kb())
        await state.set_state(my_states.AddObj.chapter)
    elif query.data == 'add_materials':
        await query.message.answer(const.ADD_MATERIALS)
        await query.message.answer('Файл служебной записки: ')
        await state.set_state(my_states.AddMat.note)
    elif query.data == 'add_EDO':
        await query.message.answer(const.ADD_EDO)
        await query.message.answer('Файл служебной записки: ')
        await state.set_state(my_states.AddObjAdm.note)
    elif query.data == 'open_access':
        await state.set_state(my_states.OpenAcs.note)
    elif query.data == 'edit_incorrect_move_admin':
        await state.set_state(my_states.EditMoveAdm.note)
    elif query.data == 'edit_shipment':
        await state.set_state(my_states.EditShpmnt.note)
    elif query.data == 'edit_incorrect_move':
        await state.set_state(my_states.EditMove.note)


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(get_name, state=BaseStates.fio)
