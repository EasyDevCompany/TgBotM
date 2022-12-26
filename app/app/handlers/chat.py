from aiogram import types
from aiogram.dispatcher import FSMContext

from app.app.keyboards.inline_keyboard import start_work, role_button_markup, request_button_markup, \
    file_official_notes, ans_yes_no
from app.app.loader import dp
from app.app.states.base import BaseStates, ChangeSatusApplication
from app.app.utils.const import START_MESSAGE, CHANGE_STATUS_APPLICATION


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(START_MESSAGE, reply_markup=start_work)


@dp.callback_query_handler(text='start_work')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'start_work':
        await state.set_state(BaseStates.fio)
        await query.message.answer('Введите Ф.И.О.')

# Вопрос - как добавить кнопку отмены _____________________________________________________________


@dp.message_handler(state=BaseStates.fio)
async def name(message: types.Message, state: FSMContext):

    await state.set_state(BaseStates.role)
    await message.answer("Выберите свою роль в ЭДО", reply_markup=role_button_markup)


@dp.callback_query_handler(state=BaseStates.role)
async def role(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'accountant':
        await state.set_state(BaseStates.request_type)
        await query.message.answer('Вид заявки', reply_markup=request_button_markup)


@dp.callback_query_handler(state=BaseStates.request_type)
async def role(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'change_status_application':
        await state.set_state(ChangeSatusApplication.add_file)
        await query.message.answer(CHANGE_STATUS_APPLICATION, reply_markup=file_official_notes)


# Вопрос - как загрузить файл? ________________________________________________________________________________________


@dp.callback_query_handler(text='file_official_notes')
@dp.callback_query_handler(state=ChangeSatusApplication.add_file)
async def role(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'file_official_notes':
        await state.set_state(ChangeSatusApplication.request_number)
        await query.message.answer('Добавить файл')

# Вопрос - какую валидацию должна проходить номер заявки? _____________________________________________________________


@dp.message_handler(state=ChangeSatusApplication.request_number)
async def name(message: types.Message, state: FSMContext):

    await state.set_state(ChangeSatusApplication.request_status)
    await message.answer("Укажите номер заявки")

# Вопрос - статус должен быть выпадающим списком или человек сам пишет?________________________________________________


@dp.message_handler(state=ChangeSatusApplication.request_status)
async def name(message: types.Message, state: FSMContext):

    await state.set_state(ChangeSatusApplication.check_result)
    await message.answer("Укажите, какой статус необходимо поставить заявке")

# Вопрос - как вывести все поля которые пользователь ввел в чате?_____________________________________________________


@dp.message_handler(state=ChangeSatusApplication.check_result)
async def name(message: types.Message, state: FSMContext):

    await state.set_state(ChangeSatusApplication.finaly_result)
    await message.answer("Вы уверены что все данные верны?", reply_markup=ans_yes_no)


@dp.callback_query_handler(text='yes')
@dp.callback_query_handler(text='no')
@dp.callback_query_handler(state=ChangeSatusApplication.finaly_result)
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'yes':
        await state.finish()
        await query.message.reply("Спасибо за обращение")
    if answer_data == 'no':
        await query.message.reply("Вернемся на шаг назад")
