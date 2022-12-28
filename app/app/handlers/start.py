from dependency_injector.wiring import inject, Provide

from core.container import Container

from models.telegram_user import TelegramUser
from services.tg_user_service import TelegramUserService

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from utils import const
import keyboards.inline_keyboard as kb
from loader import dp, bot
from loguru import logger
from states.base import BaseStates
import states.tgbot_states as my_states


@dp.callback_query_handler(text='exit', state='*')
async def cancel(query: types. CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.finish()
    await query.message.answer(const.START_MESSAGE, reply_markup=kb.start_work)
    await query.answer()


@inject
async def start(
        message: types.Message,
        tg_user_service: TelegramUserService = Provide[
            Container.telegram_user_service]
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
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
    await state.set_state(BaseStates.fio)


async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    new_kb = kb.choose_your_role().add(kb.exit_button)
    await message.answer('Выберите свою роль',
                         reply_markup=new_kb)
    await state.set_state(BaseStates.role)


@dp.callback_query_handler(state=BaseStates.role)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(role=query.data)
    new_kb = kb.main_kb().add(kb.exit_button)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Выберите тип запроса',
                               reply_markup=new_kb)
    await state.set_state(BaseStates.request_type)


@dp.callback_query_handler(state=BaseStates.request_type)
async def get_request_type(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(request_type=query.data)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    if query.data == 'add_subobject':
        await query.message.answer(const.ADD_SUBOBJECTS,
                                   reply_markup=kb.add_subobjects_kb())
        await state.set_state(my_states.AddObj.chapter)
    elif query.data == 'change_status':
        await query.message.answer(const.CHANGE_STATUS_APPLICATION)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.ChangeStatus.note)
    elif query.data == 'edit_type_work':
        await query.message.answer(const.EDIT_SUBOBJECT)
        await query.message.answer(const.EDIT_SUBOBJECT_TYPE_WORK, reply_markup=kb.exit_kb())
        await state.set_state(my_states.EditViewWork.edit_sub_object_type_work)
    elif query.data == 'add_type_work':
        await query.message.answer(const.ADD_TYPE_WORK)
        await query.message.answer(const.SELECT_SUBOBJECT, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddViewWork.edit_sub_object)
    elif query.data == 'add_coef':
        await query.message.answer(const.CONVERSION_FACTOR)
        await query.message.answer(const.UPDATE_COEF, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddCoef.update_coef)
    elif query.data == 'update_storage':
        await query.message.answer(const.UPDATE_STORAGE)
        await query.message.answer(const.NUMBER_BID, reply_markup=kb.exit_kb())
        await state.set_state(my_states.UpdateStorage.number_bid)
    elif query.data == 'add_names':
        await query.message.answer(const.ADD_NAMING)
        await query.message.answer(const.SECTION_MATERIAL, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddNaming.section_material)
    elif query.data == 'edit_subobject':
        await query.message.answer(const.EDIT_SUBOBJECT)
        await query.message.answer(const.SELECT_SUBOBJECT, reply_markup=kb.exit_kb())
        await state.set_state(my_states.UpdateSubObject.select_subobject)
    elif query.data == 'add_materials':
        await query.message.answer(const.ADD_MATERIALS)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddMat.note)
    elif query.data == 'add_EDO':
        await query.message.answer(const.ADD_EDO)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.AddObjAdm.note)
    elif query.data == 'open_access':
        await query.message.answer(const.OPEN_EDO)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.OpenAcs.note)
    elif query.data == 'edit_incorrect_move_admin':
        await query.message.answer(const.EDIT_MOV)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.EditMoveAdm.note)
    elif query.data == 'edit_shipment':
        await query.message.answer(const.EDIT_SHIP)
        await query.message.answer(const.NOTE, reply_markup=kb.exit_kb())
        await state.set_state(my_states.EditShpmnt.note)
    elif query.data == 'edit_incorrect_move':
        await state.set_state(my_states.EditMove.note)


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(get_name, state=BaseStates.fio)
