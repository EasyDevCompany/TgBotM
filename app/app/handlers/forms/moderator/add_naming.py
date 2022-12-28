from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards.inline_keyboard as kb
from loader import bot, dp
from states.tgbot_states import AddNaming


async def get_section_material(message: types.Message, state: FSMContext):
    await state.update_data(section_material=message.text)
    await message.answer('Укажите подраздел для материала',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddNaming.subsection_material)


async def get_subsection_material(message: types.Message, state: FSMContext):
    await state.update_data(subsection_material=message.text)
    await message.answer('Укажите группу для материала',
                         reply_markup=kb.exit_kb())
    await state.set_state(AddNaming.group_material)


async def get_group_material(message: types.Message, state: FSMContext):
    await state.update_data(group_material=message.text)
    await message.answer('Укажите название наименования материала',
                         reply_markup=kb.sure())
    await state.set_state(AddNaming.name_material)


async def get_name_material(message: types.Message, state: FSMContext):
    await state.update_data(name_material=message.text)
    await message.answer('Укажите единицу измерения материала',
                         reply_markup=kb.sure())
    await state.set_state(AddNaming.unit_of_measureament)


async def get_unit_of_measureament(message: types.Message, state: FSMContext):
    await state.update_data(unit_of_measureament=message.text)
    await message.answer('Если необходимо добавить несколько наименований материалов, прикрепите таблицу по шаблону',
                         reply_markup=kb.sure())
    await state.set_state(AddNaming.add_several_naming)


async def get_add_several_naming(message: types.Message, state: FSMContext):
    await state.update_data(several_naming=message.document.file_id)
    await message.answer('Вы уверены, что все данные верны?',
                         reply_markup=kb.sure())
    await state.set_state(AddNaming.sure)


@dp.callback_query_handler(text='edit', state=AddNaming.sure)
async def edit_data(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer('Выберите номер пункта для корректировки: ',
                               reply_markup=kb.choose_number())


def register(dp: Dispatcher):

    dp.register_message_handler(get_section_material, state=AddNaming.section_material)
    dp.register_message_handler(get_subsection_material, state=AddNaming.subsection_material)
    dp.register_message_handler(get_group_material, state=AddNaming.group_material)
    dp.register_message_handler(get_name_material, state=AddNaming.name_material)
    dp.register_message_handler(get_unit_of_measureament, state=AddNaming.unit_of_measureament)
    dp.register_message_handler(get_add_several_naming, state=AddNaming.add_several_naming, content_types=['document'])
