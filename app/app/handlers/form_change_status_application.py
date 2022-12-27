from aiogram import types
from aiogram.dispatcher import FSMContext

from app.app.keyboards.inline_keyboard import start_work, role_button_markup, request_button_markup, \
    file_official_notes, ans_yes_no
from app.app.loader import dp, bot
from app.app.states.base import BaseStates, ChangeStatusApplication
from app.app.utils.const import START_MESSAGE, CHANGE_STATUS_APPLICATION


async def start(message: types.Message):
    await message.answer(START_MESSAGE, reply_markup=start_work)


async def name(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(BaseStates.fio)
    await query.message.answer('Введите Ф.И.О.')


async def name_invalid(message: types.Message, state: FSMContext):
    await state.set_state(BaseStates.fio)
    await message.answer('Введите пожалуйста Ф.И.О только буквами')


async def role(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text
    await state.set_state(BaseStates.role)
    await message.answer("Выберите свою роль в ЭДО", reply_markup=role_button_markup)


async def type_application(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'accountant':
        async with state.proxy() as data:
            data['role'] = 'Бухгалтер'
        await state.set_state(BaseStates.request_type)
        await query.message.answer('Вид заявки', reply_markup=request_button_markup)


async def change_status_application(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'change_status_application':
        async with state.proxy() as data:
            data['requst_type'] = "Смена статуса заявки"
        await state.set_state(ChangeStatusApplication.add_file)
        await query.message.answer(CHANGE_STATUS_APPLICATION, reply_markup=file_official_notes)


async def added_file(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'file_official_notes':
        await state.set_state(ChangeStatusApplication.request_number)
        await query.message.answer('Добавьте файл с документом')


async def write_number_application_invalid(message: types.Message, state: FSMContext):
    await state.set_state(ChangeStatusApplication.request_status)
    await message.answer("Номер заявки может быть только цифрами, укажите номер заявки")


async def write_number_application(message: types.Message, state: FSMContext):
    document = message.document.file_id
    async with state.proxy() as data:
        data['add_file'] = document
    await state.set_state(ChangeStatusApplication.request_status)
    await message.answer("Файл добавлен, укажите номер заявки")


async def write_status_application_invalid(message: types.Message, state: FSMContext):
    await state.set_state(ChangeStatusApplication.request_status)
    await message.answer("Статус заявки не включает в себя цифры")


async def write_status_application(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['request_number'] = message.text
    await state.set_state(ChangeStatusApplication.check_result)
    await message.answer("Укажите, какой статус необходимо поставить заявке?")


async def check_result(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['request_status'] = message.text
        await state.set_state(ChangeStatusApplication.finaly_result)

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Ваши Ф.И.О.', md.code(data['fio'])),
                md.text('Ваша роль в ЭДО', md.code(data['role'])),
                md.text('Тип запроса который вы выбрали', md.code(data['requst_type'])),
                md.text('Документ', md.code(data['add_file'])),
                md.text('Номер заявки', md.code(data['request_number'])),
                md.text('Статус заявки', md.code(data['request_status'])),
                sep='\n',
            ),
            reply_markup=ans_yes_no,
            parse_mode=ParseMode.MARKDOWN,
        )


async def finally_result(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'yes':
        await state.finish()
        await query.message.answer("Запрос отправлен в работу")
    if answer_data == 'no':
        await state.finish()
        await query.message.answer("Отредактируйте пункты", reply_markup=start_work)

