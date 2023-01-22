from aiogram import types
from app.utils import const
from logger import logger
from app.loader import bot
from app.core.config import settings
from app.keyboards.inline_keyboard import in_chnl_kb, user_edit
from aiogram.dispatcher import FSMContext
from app.services.application import ApplicationService
from app.services.tg_user_service import TelegramUserService
from dependency_injector.wiring import inject, Provide
from app.models.application import Application
from app.core.container import Container


async def send_data(state, query=None, message=None):
    data = await state.get_data()
    if 'change' in data:
        del data['change']
    try:
        del data['message_id']
    except:
        pass
    msg = ''
    list_of_val = []
    for i in data.values():
        if i != 'moderator' and i != 'administrator':
            list_of_val.append(i)
    for i, v in enumerate(list_of_val):
        msg += f'{i+1}: {v}\n'
    if query is not None:
        if data['request_type'] in ['Смена статуса заявки',
                                    'Корректировка оформленной накладной',
                                    'Добавление объекта в ЭДО',
                                    "Открытие доступов Эдо для сотрудников",
                                    'Редактирование некорректного перемещения']:
            try:
                await query.message.answer_photo(data['field_one'])
            except:
                await query.message.answer_document(data['field_one'])
        elif data['request_type'] == 'Добавление материалов на свободный остаток':
            media = types.MediaGroup()
            try:
                await query.message.answer_photo(data['field_one'])
            except:
                await query.message.answer_document(data['field_one'])
            try:
                await query.message.answer_photo(data['field_three'])
            except:
                await query.message.answer_document(data['field_three'])
                await query.message.answer_media_group(media=media)
        elif data['request_type'] == 'Добавление наименований':
            if data['field_six'] != '---':
                try:
                    await query.message.answer_photo(data['field_six'])
                except:
                    await query.message.answer_document(data['field_six'])
        elif data['request_type'] == 'Корректировка поставок':
            if data['field_seven'] != const.NO_EXTRA:
                try:
                    await query.message.answer_photo(data['field_one'])
                except:
                    await query.message.answer_document(data['field_one'])
                list_ids = data['field_seven'].split(', ')
                for i in list_ids:
                    try:
                        await query.message.answer_photo(i)
                    except:
                        await query.message.answer_document(i)
        await query.message.answer(msg)
    else:
        if data['request_type'] in ['Смена статуса заявки',
                                    'Корректировка оформленной накладной',
                                    'Добавление объекта в ЭДО',
                                    "Открытие доступов Эдо для сотрудников",
                                    'Редактирование некорректного перемещения']:
            try:
                await message.answer_photo(data['field_one'])
            except:
                await message.answer_document(data['field_one'])
        elif data['request_type'] == 'Добавление материалов на свободный остаток':
            try:
                await message.answer_photo(data['field_one'])
            except:
                await message.answer_document(data['field_one'])
            try:
                await message.answer_photo(data['field_three'])
            except:
                await message.answer_document(data['field_three'])
        elif data['request_type'] == 'Добавление наименований':
            if data['field_six'] != '---':
                try:
                    await message.answer_photo(data['field_six'])
                except:
                    await message.answer_document(data['field_six'])
        elif data['request_type'] == 'Корректировка поставок':
            if data['field_seven'] != const.NO_EXTRA:
                try:
                    await message.answer_photo(data['field_one'])
                except:
                    await message.answer_document(data['field_one'])
                list_ids = data['field_seven'].split(', ')
                for i in list_ids:
                    try:
                        await message.answer_photo(i)
                    except:
                        await message.answer_document(i)
        await message.answer(msg)


async def send_data_channel(channel=None, ticket=None, user_id=None, state=None, edit=False):
    msg = ''
    if channel == 'admin':
        msg += 'А' + f'{ticket.id}\n'
    elif channel == 'support':
        msg += 'Т' + f'{ticket.id}\n'
    msg += f'1){ticket.name}\n'
    msg += f'2){ticket.role}\n'
    msg += f'3){ticket.request_type}\n'
    msg += f'4){ticket.field_one}\n'
    msg += f'5){ticket.field_two}\n'
    if ticket.field_three is not None:
        msg += f'6){ticket.field_three}\n'
    if ticket.field_four is not None:
        msg += f'7){ticket.field_four}\n'
    if ticket.field_five is not None:
        msg += f'8){ticket.field_five}\n'
    if ticket.field_six is not None:
        msg += f'9){ticket.field_six}\n'
    if ticket.field_seven is not None:
        msg += f'10){ticket.field_seven}\n'
    if ticket.field_eight is not None:
        msg += f'11){ticket.field_eight}\n'
    if ticket.field_nine is not None:
        msg += f'12){ticket.field_nine}\n'
    if ticket.request_type == 'Корректировка поставок':
        if ticket.field_seven != const.NO_EXTRA:
            if user_id is not None:
                try:
                    await bot.send_photo(user_id, ticket.field_one)
                except:
                    await bot.send_document(user_id, ticket.field_one)
                list_ids = ticket.field_seven.split(', ')
                for i in list_ids:
                    try:
                        await bot.send_photo(user_id, i)
                    except:
                        await bot.send_document(user_id, i)
            else:
                try:
                    await bot.send_photo(settings.ADMIN_CHAT_ID, ticket.field_one)
                except:
                    await bot.send_document(settings.ADMIN_CHAT_ID, ticket.field_one)
                list_ids = ticket.field_seven.split(', ')
                for i in list_ids:
                    try:
                        await bot.send_photo(settings.ADMIN_CHAT_ID, i)
                    except:
                        await bot.send_document(settings.ADMIN_CHAT_ID, i)
    elif ticket.request_type == 'Добавление материалов на свободный остаток':
        if user_id is not None:
            try:
                await bot.send_photo(user_id, ticket.field_one)
            except:
                await bot.send_document(user_id, ticket.field_one)
            try:
                await bot.send_photo(user_id, ticket.field_three)
            except:
                await bot.send_document(user_id, ticket.field_three)
        else:
            try:
                await bot.send_photo(settings.SUPPORT_CHAT_ID, ticket.field_one)
            except:
                await bot.send_document(settings.SUPPORT_CHAT_ID, ticket.field_one)
            try:
                await bot.send_photo(settings.SUPPORT_CHAT_ID, ticket.field_three)
            except:
                await bot.send_document(settings.SUPPORT_CHAT_ID, ticket.field_three)
    elif ticket.request_type in ['Добавление объекта в ЭДО',
                                 'Открытие доступов Эдо для сотрудников',
                                 'Редактирование некорректного перемещения']:
        if user_id is not None:
            try:
                await bot.send_photo(user_id, ticket.field_one)
            except:
                await bot.send_document(user_id, ticket.field_one)
        else:
            try:
                await bot.send_photo(settings.ADMIN_CHAT_ID, ticket.field_one)
            except:
                await bot.send_document(settings.ADMIN_CHAT_ID, ticket.field_one)
    elif ticket.request_type in ['Корректировка оформленной накладной',
                                 'Смена статуса заявки']:
        if user_id is not None:
            try:
                await bot.send_photo(user_id, ticket.field_one)
            except:
                await bot.send_document(user_id, ticket.field_one)
        else:
            try:
                await bot.send_photo(settings.SUPPORT_CHAT_ID, ticket.field_one)
            except:
                await bot.send_document(settings.SUPPORT_CHAT_ID, ticket.field_one)
    elif ticket.request_type == 'Добавление наименований':
        if ticket.field_six != '---':
            if user_id is not None:
                try:
                    await bot.send_photo(user_id, ticket.field_six)
                except:
                    await bot.send_document(user_id, ticket.field_six)
            else:
                try:
                    await bot.send_photo(settings.SUPPORT_CHAT_ID, ticket.field_six)
                except:
                    await bot.send_document(settings.SUPPORT_CHAT_ID, ticket.field_six)
    if user_id is not None:
        if edit:
            await state.finish()
            await bot.send_message(user_id,
                                   msg, reply_markup=user_edit(ticket=ticket))
        else:
            await state.finish()
            await bot.send_message(user_id,
                                   msg, reply_markup=in_chnl_kb(ticket=ticket))
    if channel == 'admin':
        await bot.send_message(settings.ADMIN_CHAT_ID,
                               msg, reply_markup=in_chnl_kb(ticket=ticket))
    elif channel == 'support':
        await bot.send_message(settings.SUPPORT_CHAT_ID,
                               msg, reply_markup=in_chnl_kb(ticket=ticket))
