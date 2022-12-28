from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from loader import bot, dp
from states.tgbot_states import UpdateSubObject


async def get_sub_object(message: types.Message, state: FSMContext):
    await state.update_data(sub_obj=message.text)
    await message.answer('Укажите наименование вида работ',
                         reply_markup=kb.exit_kb())
    await state.set_state(UpdateSubObject.select_type_work)


async def get_type_work(message: types.Message, state: FSMContext):
    await state.update_data(type_work=message.text)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=kb.sure())
    await state.set_state(UpdateSubObject.sure)


@dp.callback_query_handler(text='edit', state=UpdateSubObject.sure)
async def edit_data(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Выберите номер пункта для корректировки: ',
                               reply_markup=kb.choose_number())


def register(dp: Dispatcher):
    dp.register_message_handler(get_sub_object, state=UpdateSubObject.select_subobject)
    dp.register_message_handler(get_type_work, state=UpdateSubObject.select_subobject)
