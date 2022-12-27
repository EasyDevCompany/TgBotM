from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from states.tgbot_states import AddMat
from loader import dp
from utils import const


async def get_note(message: types.Message, state: FSMContext):
    await state.update_data(note=message.document.file_id)
    await message.answer('Выберите склад, куда необходимо добавить остатки: ')
    await state.set_state(AddMat.storage)


async def get_storage(message: types.Message, state: FSMContext):
    await state.update_data(storage=message.text)
    await message.answer('Excel файл с данными по наименованиям по формату: ')
    await state.set_state(AddMat.excel)


async def get_excel(message: types.Message, state: FSMContext):
    await state.update_data(excel=message.document.file_id)
    await message.answer('Укажите, необходимо ли добавлять остатки на резерв '
                         'или на свободные остатки',
                         reply_markup=kb.reserve_or_leave())
    await state.set_state(AddMat.myc)


@dp.callback_query_handler(state=AddMat.myc)
async def get_choise(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(choise=query.data)
    if query.data == 'reserve':
        await query.message.answer('Если остатки на резерве, то на какой '
                                   'объект их необходимо резервировать')
        await state.set_state(AddMat.obj)
    elif query.data == 'leave':
        print(await state.get_data())
        await query.message.answer(
            const.START_MESSAGE, reply_markup=kb.start_work)


async def get_obj(message: types.Message, state: FSMContext):
    await state.update_data(obj=message.text)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=kb.sure())
    await state.set_state(AddMat.sure)


@dp.callback_query_handler(text='edit', state=AddMat.sure)
async def edit_data(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Выберите номер пункта для корректировки: ',
                               reply_markup=kb.choose_number())


def register(dp: Dispatcher):
    dp.register_message_handler(get_note,
                                state=AddMat.note, content_types=['document'])
    dp.register_message_handler(get_storage, state=AddMat.storage)
    dp.register_message_handler(get_excel,
                                state=AddMat.excel, content_types=['document'])
    dp.register_message_handler(get_obj, state=AddMat.obj)
