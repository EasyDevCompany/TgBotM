# async def send_data(state, query=None, message=None):
#     data = await state.get_data()
#     if 'change' in data:
#         del data['change']
#     elif 'message_id' in data:
#         del data['message_id']
#     msg = ''
#     list_of_val = []
#     for i in data.values():
#         if i != 'moderator' and i != 'admin' and i is not None:
#             list_of_val.append(i)
#     for i, v in enumerate(list_of_val):
#         msg += f'{i + 1}: {v}\n'
#     if query is not None:
#         await query.message.answer(msg)
#     else:
#         await message.answer(msg)


from aiogram import types
from app.utils import const
from logger import logger


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
    logger.info(data.values())
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
                try:
                    media = data['field_seven']
                    media.attach_document(types.InputMediaDocument(data['field_one']))
                    await query.message.answer_media_group(data['field_seven'])
                except:
                    await query.message.answer_document(data['field_seven'])
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
                try:
                    media = data['field_seven']
                    media.attach_document(types.InputMediaDocument(data['field_one']))
                    await message.answer_media_group(data['field_seven'])
                except:
                    await message.answer_document(data['field_seven'])
        await message.answer(msg)
