from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from loader import dp, bot
from states.tgbot_states import ChangeStatus


async def get_note(message: types.Message, state: FSMContext):
    await state.update_data(note=message.document.file_id)
    await message.answer('Укажите номер заявки',
                         reply_markup=kb.exit_kb())
    await state.set_state(ChangeStatus.number_bid)


async def get_number_bid(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer('Укажите какой статус необходимо поставить заявке',
                         reply_markup=kb.exit_kb())
    await state.set_state(ChangeStatus.status_in_bid)


async def get_status_in_bid(message: types.Message, state: FSMContext):
    await state.update_data(status=message.text)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=kb.sure())
    await state.set_state(ChangeStatus.sure)


@dp.callback_query_handler(text='edit', state=ChangeStatus.sure)
async def edit_data(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Выберите номер пункта для корректировки: ',
                               reply_markup=kb.choose_number())


def register(dp: Dispatcher):
    dp.register_message_handler(get_note,
                                state=ChangeStatus.note, content_types=['document'])
    dp.register_message_handler(get_number_bid, state=ChangeStatus.number_bid)
    dp.register_message_handler(get_status_in_bid, state=ChangeStatus.status_in_bid)

