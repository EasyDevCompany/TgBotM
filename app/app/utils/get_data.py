async def send_data(state, query=None, message=None):
    data = await state.get_data()
    if 'change' in data:
        del data['change']
    msg = ''
    for v in data.values():
        if v == 'tech' or v == 'adm':
            continue
        msg += f'{v[0]}: {v[1]}\n'
    if query is not None:
        await query.message.answer(msg)
    else:
        await message.answer(msg)
