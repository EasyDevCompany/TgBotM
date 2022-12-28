from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from loader import bot, dp
from states.tgbot_states import AddCoef


async def get_coef(message: types.Message, state: FSMContext):
    await state.update_data(coef=message.text)
    await message.answer('Укажите старую единицу измерения и новую (на которую необходимо поменять)',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddCoef.old_new)


async def get_old_new(message: types.Message, state: FSMContext):
    await state.update_data(old_new=message.text)
    await message.answer('Укажите соотношение старой единицы измерения к новой)',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddCoef.ratio)


async def get_ratio(message: types.Message, state: FSMContext):
    await state.update_data(ratio=message.text)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=kb.sure())
    await state.set_state(AddCoef.sure)


# @dp.callback_query_handler(text='edit', state=AddCoef.sure)
# async def edit_data(query: types.CallbackQuery, state: FSMContext):
#     await bot.delete_message(query.message.chat.id, query.message.message_id)
#     await query.message.answer('Выберите номер пункта для корректировки: ',
#                                reply_markup=kb.choose_number())


def register(dp: Dispatcher):
    dp.register_message_handler(get_coef, state=AddCoef.update_coef)
    dp.register_message_handler(get_old_new, state=AddCoef.old_new)
    dp.register_message_handler(get_ratio, state=AddCoef.ratio)
