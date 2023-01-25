from aiogram import types
from .clallback_data import application_callback

start_work = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(
        text="Начать работу",
        callback_data="start_work"
    )
)


async def application(application_id: int):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="Взять в работу",
            callback_data=application_callback.new(
                data=f"{application_id}",
                type="in_work"
            )
        ),
        types.InlineKeyboardButton(
            text="Вернуть сотруднику для корректировки запроса",
            callback_data=application_callback.new(
                data=f"{application_id}",
                type="return"
            )
        ),
        types.InlineKeyboardButton(
            text="Запрос обработан",
            callback_data=application_callback.new(
                data=f"{application_id}",
                type="done"
            )
        )
    )

    return keyboard

cancel_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        callback_data='cancel',
        text='Отменить'
    )
)


async def edit(application_id: int):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    return keyboard.add(
        types.InlineKeyboardButton(
            text="Редактировать",
            callback_data=application_callback.new(
                data=f"{application_id}",
                type="edit"
            )
        )
    )


async def edit_field(field_count: int):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for field_num in range(1, field_count + 1):
        keyboard.add(
            types.InlineKeyboardButton(
                text=f"{field_num}",
                callback_data=f"{field_num}"
                )
            )
    return keyboard
