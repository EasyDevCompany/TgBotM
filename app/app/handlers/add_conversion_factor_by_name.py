from aiogram import types
from aiogram.dispatcher import FSMContext


async def add_conversion_factor(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'conversion_factor':
        async with state.proxy() as data:
            data['choose_request'] = "Добавление коэффицента пересчета по наименованию"
        await state.set_state(AddConversionFactorByName.specify_name_factor)
        await query.message.answer(CONVERSION_FACTOR)


async def specify_name_factor(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['specify_name_factor'] = message.text
    await state.set_state(AddConversionFactorByName.old_new_unit)
    await message.answer("Укажите старую единицу измерения и новую (на которую необходимо поменять)")


async def old_new_unit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['old_new_unit'] = message.text
    await state.set_state(AddConversionFactorByName.ratio_old_to_new_unit)
    await message.answer("Укажите соотношение старой единицы измерения к новой")


async def ratio_old_to_new_unit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ratio_old_to_new_unit'] = message.text
    await state.set_state(AddConversionFactorByName.finaly)
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Ваши Ф.И.О.', md.code(data['fio'])),
            md.text('Ваша роль в ЭДО', md.code(data['role'])),
            md.text('Тип запроса который вы выбрали', md.code(data['choose_request'] )),
            md.text('Наименование в котором необходимо внести коэффициент перерасчета', md.code(data['specify_name_factor'])),
            md.text('Старая и новая единица измерения', md.code(data['old_new_unit'])),
            md.text('Соотношение старой единицы измерения к новои', md.code(data['ratio_old_to_new_unit'])),
            sep='\n',
        ),
        reply_markup=ans_yes_no,
        parse_mode=ParseMode.MARKDOWN,
    )
