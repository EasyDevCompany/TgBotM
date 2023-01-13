async def send_data(state, query=None, message=None):
    data = await state.get_data()
    if 'change' in data:
        del data['change']
    elif 'message_id' in data:
        del data['message_id']
    msg = ''
    list_of_val = []
    for i in data.values():
        if i != 'moderator' and i != 'admin' and i is not None:
            list_of_val.append(i)
    for i, v in enumerate(list_of_val):
        msg += f'{i + 1}: {v}\n'
    if query is not None:
        await query.message.answer(msg)
    else:
        await message.answer(msg)
