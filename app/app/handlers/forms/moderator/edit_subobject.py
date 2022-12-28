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
    new_kb = kb.sure().add(kb.exit_button)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=new_kb)
    await state.set_state(UpdateSubObject.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_sub_object,
                                state=UpdateSubObject.select_subobject)
    dp.register_message_handler(get_type_work,
                                state=UpdateSubObject.select_type_work)
