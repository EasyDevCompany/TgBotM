import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot
from app.states.base import BaseStates
from app.states.tgbot_states import AddCoef
from app.utils import const, get_data
from app.utils.const import EDIT_NEW_OLD, RATIO_OLD_NEW, UNIT_ERROR, RATIO_ERROR, FIO, ROLE, R_TYPE
from dependency_injector.wiring import inject, Provide
from app.services.application import ApplicationService
from app.core.container import Container
from app.models.application import Application


async def get_coef(message: types.Message, state: FSMContext):
    await state.update_data(field_one=message.text)
    await message.answer(EDIT_NEW_OLD,
                         reply_markup=kb.exit_kb())
    await state.set_state(AddCoef.old_new)


async def get_old_new(message: types.Message, state: FSMContext):
    if not message.text.isalpha():
        await state.update_data(field_two=message.text)
        await message.answer(RATIO_OLD_NEW,
                             reply_markup=kb.exit_kb())
        await state.set_state(AddCoef.ratio)
    else:
        await message.answer(UNIT_ERROR)
        await state.set_state(AddCoef.old_new)


@inject
async def get_ratio(message: types.Message, state: FSMContext,
                    application: ApplicationService = Provide[Container.application_service]):
    if not message.text.isalpha():
        await state.update_data(field_three=message.text)
        data = await state.get_data()
        if 'admin' not in data:
            await get_data.send_data(message=message, state=state)
            new_kb = kb.sure().add(kb.exit_button)
            await message.answer(const.SURE, reply_markup=new_kb)
            await state.set_state(AddCoef.sure)
        else:
            black_list = {'admin'}
            new_data = {key: val for key, val in data.items() if key not in black_list}
            unused = ['field_four', 'field_five', 'field_six', 'field_seven', 'field_eight', 'field_nine']
            for i in unused:
                new_data[i] = None
            await application.update(data['admin'], obj_in=new_data)
            await message.answer(const.CHANGE_SUCCESS)
            await state.finish()
    else:
        await message.answer(RATIO_ERROR)
        await state.set_state(AddCoef.ratio)


async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer(FIO, reply_markup=kb.exit_kb())
        await state.set_state(AddCoef.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer(ROLE,
                                   reply_markup=new_kb)
        await state.set_state(AddCoef.edit)
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
        await state.update_data(change='coef')
        await query.message.answer(
            const.UPDATE_COEF, reply_markup=kb.exit_kb())
        await state.set_state(AddCoef.edit)
    elif query.data == '5':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='old_new')
        await query.message.answer(EDIT_NEW_OLD,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddCoef.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='ratio')
        await query.message.answer(RATIO_OLD_NEW,
                                   reply_markup=kb.exit_kb())
        await state.set_state(AddCoef.edit)
    await query.answer()


@inject
async def edit(message: types.Message, state: FSMContext,
               application: ApplicationService = Provide[Container.application_service]):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=['ФИО', message.text])
    elif point == 'coef':
        await state.update_data(field_one=message.text)
    elif point == 'old_new':
        await state.update_data(field_two=message.text)
    elif point == 'ratio':
        await state.update_data(field_three=message.text)
    data = await state.get_data()
    if 'admin' not in data:
        await get_data.send_data(message=message, state=state)
        new_kb = kb.sure().add(kb.exit_button)
        await message.answer(const.SURE, reply_markup=new_kb)
        await state.set_state(AddCoef.sure)
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
        await state.set_state(AddCoef.sure)
    else:
        await application.update(data['admin'],
                                 obj_in={'application_status': Application.ApplicationStatus.in_work,
                                         'role': data['role']})
        await query.message.answer(const.CHANGE_SUCCESS)
        await state.finish()


def register(dp: Dispatcher):
    dp.register_message_handler(get_coef, state=AddCoef.update_coef)
    dp.register_message_handler(get_old_new, state=AddCoef.old_new)
    dp.register_message_handler(get_ratio, state=AddCoef.ratio)
    dp.register_message_handler(edit, state=AddCoef.edit)
    dp.register_callback_query_handler(correct, state=AddCoef.sure)
    dp.register_callback_query_handler(get_role, state=AddCoef.edit)
