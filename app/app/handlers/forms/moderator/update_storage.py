from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from loader import bot, dp
from states.tgbot_states import UpdateStorage


async def get_number_bid(message: types.Message, state: FSMContext):
    await state.update_data(number_bid=message.text)
    await message.answer('Укажите новый склад доставки',
                         reply_markup=kb.exit_kb())
    await state.set_state(UpdateStorage.new_storage)


async def get_new_storage(message: types.Message, state: FSMContext):
    await state.update_data(new_storage=message.text)
    await message.answer('Укажите контактное лицо (Ф.И.О.)',
                         reply_markup=kb.exit_kb())
    await state.set_state(UpdateStorage.fio)


async def get_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer(
        'Укажите адрес актуального склада (на который нужно поменять)')
    await state.set_state(UpdateStorage.address_storage)


async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=kb.sure())
    await state.set_state(UpdateStorage.sure)


def register(dp: Dispatcher):
    dp.register_message_handler(get_number_bid, state=UpdateStorage.number_bid)
    dp.register_message_handler(get_new_storage, state=UpdateStorage.new_storage)
    dp.register_message_handler(get_fio, state=UpdateStorage.fio)
    dp.register_message_handler(get_address, state=UpdateStorage.address_storage)
