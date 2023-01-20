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
        if i != 'moderator' and i != 'admin':
            list_of_val.append(i)
    for i, v in enumerate(list_of_val):
        msg += f'{i+1}: {v}\n'
    if query is not None:
        if data['request_type'] in ['Смена статуса заявки',
                                    'Корректировка оформленной накладной',
                                    'Добавление объекта в ЭДО',
                                    "Открытие доступов Эдо для сотрудников",
                                    'Редактирование некорректного перемещения']:
            await query.message.answer_document(data['field_one'])
        elif data['request_type'] == 'Добавление материалов на свободный остаток':
            media = types.MediaGroup()
            media.attach_document(types.InputMediaDocument(data['field_one']))
            media.attach_document(types.InputMediaDocument(data['field_three']))
            await query.message.answer_media_group(media=media)
        elif data['request_type'] == 'Добавление наименований':
            if data['field_six'] != '---':
                await query.message.answer_document(data['field_six'])
        elif data['request_type'] == 'Корректировка поставок':
            if data['field_seven'] != const.NO_EXTRA:
                await query.message.answer_document(data['field_one'])
                list_ids = data['field_seven'].split(', ')
                for i in list_ids:
                    await query.message.answer_document(i)
        await query.message.answer(msg)
    else:
        if data['request_type'] in ['Смена статуса заявки',
                                    'Корректировка оформленной накладной',
                                    'Добавление объекта в ЭДО',
                                    "Открытие доступов Эдо для сотрудников",
                                    'Редактирование некорректного перемещения']:
            await message.answer_document(data['field_one'])
        elif data['request_type'] == 'Добавление материалов на свободный остаток':
            media = types.MediaGroup()
            media.attach_document(types.InputMediaDocument(data['field_one']))
            media.attach_document(types.InputMediaDocument(data['field_three']))
            await message.answer_media_group(media=media)
        elif data['request_type'] == 'Добавление наименований':
            if data['field_six'] != '---':
                await message.answer_document(data['field_six'])
        elif data['request_type'] == 'Корректировка поставок':
            if data['field_seven'] != const.NO_EXTRA:
                await message.answer_document(data['field_one'])
                list_ids = data['field_seven'].split(', ')
                for i in list_ids:
                    await message.answer_document(i)
        await message.answer(msg)


async def send_data_channel(channel=None, ticket=None, user_id = None, state=None, edit=False):
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
                await bot.send_document(user_id, ticket.field_one)
                list_ids = ticket.field_seven.split(', ')
                for i in list_ids:
                    await bot.send_document(user_id, i)
            else:
                await bot.send_document(settings.ADMIN_CHAT_ID, ticket.field_one)
                list_ids = ticket.field_seven.split(', ')
                for i in list_ids:
                    await bot.send_document(settings.ADMIN_CHAT_ID, i)
    elif ticket.request_type == 'Добавление материалов на свободный остаток':
        media = types.MediaGroup()
        media.attach_document(types.InputMediaDocument(ticket.field_one))
        media.attach_document(types.InputMediaDocument(ticket.field_three))
        if user_id is not None:
            await bot.send_media_group(user_id, media=media)
        else:
            await bot.send_media_group(settings.SUPPORT_CHAT_ID, media=media)
    elif ticket.request_type in ['Добавление объекта в ЭДО',
                                 'Открытие доступов Эдо для сотрудников',
                                 'Редактирование некорректного перемещения']:
        if user_id is not None:
            await bot.send_document(user_id, ticket.field_one)
        else:
            await bot.send_document(settings.ADMIN_CHAT_ID, ticket.field_one)
    elif ticket.request_type in ['Корректировка оформленной накладной',
                                 'Смена статуса заявки']:
        if user_id is not None:
            await bot.send_document(user_id, ticket.field_one)
        else:
            await bot.send_document(settings.SUPPORT_CHAT_ID, ticket.field_one)
    elif ticket.request_type == 'Добавление наименований':
        if ticket.field_six != '---':
            if user_id is not None:
                await bot.send_document(user_id, ticket.field_six)
            else:
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
