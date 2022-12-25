from aiogram import types

start_work = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(
        text="Начать работу",
        callback_data="start_work"
    )
)
