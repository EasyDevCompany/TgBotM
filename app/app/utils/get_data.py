async def send_data(state, query=None, message=None):
    data = await state.get_data()
    msg = ''
    for k, v in data.items():
        msg += f'{k}: {v}\n'
    if query is not None:
        await query.message.answer(msg)
    else:
        await message.answer(msg)
