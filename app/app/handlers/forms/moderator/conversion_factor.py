import app.keyboards.inline_keyboard as kb
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.loader import bot, dp
from app.states.base import BaseStates
from app.states.tgbot_states import AddCoef
from app.utils import const, get_data


async def get_coef(message: types.Message, state: FSMContext):
    await state.update_data(coef=message.text)
    await message.answer(
        'Укажите старую единицу измерения и новую'
        '(на которую необходимо поменять)',
        reply_markup=kb.exit_kb())
    await state.set_state(AddCoef.old_new)


async def get_old_new(message: types.Message, state: FSMContext):
    await state.update_data(old_new=message.text)
    await message.answer(
        'Укажите соотношение старой единицы измерения к новой)',
        reply_markup=kb.exit_kb())
    await state.set_state(AddCoef.ratio)


async def get_ratio(message: types.Message, state: FSMContext):
    await state.update_data(ratio=message.text)
    await get_data.send_data(message=message, state=state)
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=new_kb)
    await state.set_state(AddCoef.sure)


@dp.callback_query_handler(state=AddCoef.sure)
async def correct(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='name')
        await query.message.answer('Введите ФИО', reply_markup=kb.exit_kb())
        await state.set_state(AddCoef.edit)
    elif query.data == '2':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='role')
        new_kb = kb.choose_your_role().add(kb.exit_button)
        await query.message.answer('Выберите свою роль',
                                   reply_markup=new_kb)
        await state.set_state(AddCoef.edit)
    elif query.data == '3':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='request_type')
        new_kb = kb.main_kb().add(kb.exit_button)
        await query.message.answer('Выберите тип запроса',
                                   reply_markup=new_kb)
        await state.set_state(BaseStates.request_type)
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
        await query.message.answer(
            'Укажите старую единицу измерения и новую'
            '(на которую необходимо поменять)',
            reply_markup=kb.exit_kb())
        await state.set_state(AddCoef.edit)
    elif query.data == '6':
        await bot.delete_message(
            query.message.chat.id, query.message.message_id)
        await state.update_data(change='ratio')
        await query.message.answer(
            'Укажите соотношение старой единицы измерения к новой)',
            reply_markup=kb.exit_kb())
        await state.set_state(AddCoef.edit)
    await query.answer()


async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    point = data['change']
    if point == 'name':
        await state.update_data(name=message.text)
    elif point == 'coef':
        await state.update_data(coef=message.text)
    elif point == 'old_new':
        await state.update_data(old_new=message.text)
    elif point == 'ratio':
        await state.update_data(ratio=message.text)
    print(await state.get_data())
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(message=message, state=state)
    await message.answer(const.SURE,
                         reply_markup=new_kb)
    await state.set_state(AddCoef.sure)


@dp.callback_query_handler(state=AddCoef.edit)
async def get_role(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.update_data(role=query.data)
    new_kb = kb.sure().add(kb.exit_button)
    await get_data.send_data(query=query, state=state)
    await query.message.answer(const.SURE,
                               reply_markup=new_kb)
    await state.set_state(AddCoef.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_coef, state=AddCoef.update_coef)
    dp.register_message_handler(get_old_new, state=AddCoef.old_new)
    dp.register_message_handler(get_ratio, state=AddCoef.ratio)
    dp.register_message_handler(edit, state=AddCoef.edit)
    dp.register_callback_query_handler(correct, state=AddCoef.sure)
    dp.register_callback_query_handler(get_role, state=AddCoef.edit)
