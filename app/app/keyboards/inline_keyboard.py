
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.utils import const_add_subobjects as const
from app.utils import const as main_const
from app.models.application import Application
from telegram_bot_pagination import InlineKeyboardPaginator
from aiogram.utils.callback_data import CallbackData
from aiogram import types
from loguru import logger

start_work = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Начать работу",
        callback_data="start_work"
    )
)

start_support = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Начать поддержку",
        callback_data="start_support"
    )
)

exit_button = InlineKeyboardButton(text='Отмена', callback_data="exit")
skip_button = InlineKeyboardButton(text='Пропустить', callback_data='skip')
send_file_btn = InlineKeyboardButton('Отправить', callback_data='send_file')


def genmarkup(data):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    for i in range(1, len(data)):
        keyboard.add(InlineKeyboardButton(i, callback_data=i))
    return keyboard


def another_genmarkup(count):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    for i in range(1, count + 1):
        keyboard.add(InlineKeyboardButton(i, callback_data=i))
    return keyboard


exit_button = InlineKeyboardButton(text='Отмена', callback_data="exit")
skip_button = InlineKeyboardButton(text='Пропустить', callback_data='skip')


def genmarkup(data):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    for i in range(1, len(data)):
        keyboard.add(InlineKeyboardButton(i, callback_data=i))
    return keyboard


def choose_your_role():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Бухгалтер',
                              callback_data=Application.Role.accountant)

    b2 = InlineKeyboardButton(text='Кладовщик',
                              callback_data=Application.Role.storekeeper)
    b3 = InlineKeyboardButton(text='Супервайзер',
                              callback_data=Application.Role.supervisor)
    b4 = InlineKeyboardButton(text='Прораб',
                              callback_data=Application.Role.foreman)
    b5 = InlineKeyboardButton(text='Начальник Участка',
                              callback_data=Application.Role.section_chief)
    b6 = InlineKeyboardButton(text='Куратор',
                              callback_data=Application.Role.curator)
    b7 = InlineKeyboardButton(text='Начальник Отдела',
                              callback_data=Application.Role.department_head)
    b8 = InlineKeyboardButton(text='Начальник управления ДИК',
                              callback_data=Application.Role.head_of_dec_department)
    b9 = InlineKeyboardButton(text='Сотрудник снабжения',
                              callback_data=Application.Role.supply_officer)
    b10 = InlineKeyboardButton(text='Сотрудник ПТО',
                               callback_data=Application.Role.supply_pto)
    b11 = InlineKeyboardButton(text='Утверждающий счета',
                               callback_data=Application.Role.account_approve)
    b12 = InlineKeyboardButton(text='Руководитель проекта',
                               callback_data=Application.Role.project_manager)
    b13 = InlineKeyboardButton(
        text='Начальник Административно-Хозяйственного управления',
        callback_data=Application.Role.head_of_the_administrative_and_economic_department)
    keyboard.row(b1, b2)
    keyboard.row(b3, b4)
    keyboard.row(b5, b6)
    keyboard.row(b7, b8)
    keyboard.row(b9, b10)
    keyboard.row(b11, b12)
    keyboard.row(b13)
    return keyboard


def create_ticket():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Создать запрос',
                              callback_data='create_ticket')
    keyboard.row(b1)
    return keyboard


def main_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Корректировка оформленной накладной',
                              callback_data='adjustment_invoice')
    b2 = InlineKeyboardButton(text='Смена статуса заявки',
                              callback_data='change_status')
    b3 = InlineKeyboardButton(
        text='Добавление коэффициента пересчёта по наименованию',
        callback_data='add_coef')
    b4 = InlineKeyboardButton(
        text='Корректировка склада в заявке', callback_data='update_storage')
    b5 = InlineKeyboardButton(
        text='Добавление наименований', callback_data='add_names')
    b6 = InlineKeyboardButton(
        text='Редактирование видов работ', callback_data='edit_type_work')
    b7 = InlineKeyboardButton(
        text='Добавление видов работ', callback_data='add_type_work')
    b8 = InlineKeyboardButton(
        text='Редактирование подобъектов', callback_data='edit_subobject')
    b9 = InlineKeyboardButton(
        text='Добавление подобъектов', callback_data='add_subobject')
    b10 = InlineKeyboardButton(
        text='Добавление материалов на свободный остаток',
        callback_data='add_materials')
    b11 = InlineKeyboardButton(
        text='Добавление объекта в ЭДО', callback_data='add_EDO')
    b12 = InlineKeyboardButton(
        text='Открытие доступов в ЭДО для сотрудников',
        callback_data='open_access')
    b13 = InlineKeyboardButton(
        text='Редактирование некорректного перемещения',
        callback_data='edit_incorrect_move_admin')
    b14 = InlineKeyboardButton(
        text='Корректировка поставок', callback_data='edit_shipment')
    keyboard.row(b1)
    keyboard.row(b2)
    keyboard.row(b3)
    keyboard.row(b4)
    keyboard.row(b5)
    keyboard.row(b6)
    keyboard.row(b7)
    keyboard.row(b8)
    keyboard.row(b9)
    keyboard.row(b10)
    keyboard.row(b11)
    keyboard.row(b12)
    keyboard.row(b13)
    keyboard.row(b14)
    return keyboard


def add_subobjects_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(
        text=const.CHAPTERS['prepare'],
        callback_data='Подготовка терр. ст-ва')
    b2 = InlineKeyboardButton(
        text=const.CHAPTERS['main_objects'],
        callback_data='Основные объекты ст-ва')
    b3 = InlineKeyboardButton(
        text=const.CHAPTERS['extra_objects'],
        callback_data='Об-ты подсобного и обслуживающего')
    b4 = InlineKeyboardButton(
        text=const.CHAPTERS['energy_objects'],
        callback_data='Объекты энергетического хоз-ва')
    b5 = InlineKeyboardButton(
        text=const.CHAPTERS['transport_objects'],
        callback_data='Объекты трансп. хоз-ва и связи')
    b6 = InlineKeyboardButton(
        text=const.CHAPTERS['zhkh_objects'],
        callback_data='Наружные сети и сооружения')
    b7 = InlineKeyboardButton(
        text=const.CHAPTERS['green_objects'],
        callback_data='Благо-во и озеленение территории')
    b8 = InlineKeyboardButton(
        text=const.CHAPTERS['temp_objects'],
        callback_data='Временные здания и сооружения')
    b9 = InlineKeyboardButton(
        text=const.CHAPTERS['other_work'],
        callback_data='Прочие работы и затраты')
    b10 = InlineKeyboardButton(
        text=const.CHAPTERS['another_payments'],
        callback_data='Другие затраты')
    keyboard.row(b1)
    keyboard.row(b2)
    keyboard.row(b3)
    keyboard.row(b4)
    keyboard.row(b5)
    keyboard.row(b6)
    keyboard.row(b7)
    keyboard.row(b8)
    keyboard.row(b9)
    keyboard.row(b10)
    return keyboard


def add_subsystem_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['main'],
        callback_data='Основные')
    b2 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['support'],
        callback_data='Вспомогательные')
    b3 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['tools'],
        callback_data='Инструменты')
    b4 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['transport'],
        callback_data='Транспорт')
    b5 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['other'],
        callback_data='Прочие материалы')
    b6 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['robe'],
        callback_data='Спецодежда')
    b7 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['furniture'],
        callback_data='Мебель')
    b8 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['office'],
        callback_data='Канцелярия')
    b9 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['givers'],
        callback_data='Давальческие')
    b10 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['out'],
        callback_data='Вывоз')
    b11 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['machines'],
        callback_data='Механизмы')
    b12 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['ROP'],
        callback_data='РОП')
    b13 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['MBO'],
        callback_data='МБО')
    b14 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['IT'],
        callback_data='ИТ')
    b15 = InlineKeyboardButton(
        text=const.SUBSYSTEMS['ALL'],
        callback_data='Все подсистемы')
    keyboard.row(b1)
    keyboard.row(b2)
    keyboard.row(b3)
    keyboard.row(b4)
    keyboard.row(b5)
    keyboard.row(b6)
    keyboard.row(b7)
    keyboard.row(b8)
    keyboard.row(b9)
    keyboard.row(b10)
    keyboard.row(b11)
    keyboard.row(b12)
    keyboard.row(b13)
    keyboard.row(b14)
    keyboard.row(b15)
    return keyboard


def accept():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b = InlineKeyboardButton(
        text='Подтвердить',
        callback_data='accept')
    keyboard.row(b)
    return keyboard


def sure():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(
        text='Нет, отредактировать пункт', callback_data='edit'
    )
    b2 = InlineKeyboardButton(
        text='Да, отправить запрос в работу', callback_data='send'
    )
    keyboard.row(b1)
    keyboard.row(b2)
    return keyboard


def choose_number():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='1', callback_data='1')
    b2 = InlineKeyboardButton(text='2', callback_data='2')
    b3 = InlineKeyboardButton(text='3', callback_data='3')
    b4 = InlineKeyboardButton(text='4', callback_data='4')
    b5 = InlineKeyboardButton(text='5', callback_data='5')
    b6 = InlineKeyboardButton(text='6', callback_data='6')
    b7 = InlineKeyboardButton(text='7', callback_data='7')
    b8 = InlineKeyboardButton(text='8', callback_data='8')
    b9 = InlineKeyboardButton(text='9', callback_data='9')
    keyboard.row(b1)
    keyboard.row(b2)
    keyboard.row(b3)
    keyboard.row(b4)
    keyboard.row(b5)
    keyboard.row(b6)
    keyboard.row(b7)
    keyboard.row(b8)
    keyboard.row(b9)
    return keyboard


def reserve_or_leave():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Резервировать', callback_data='Резервировать')
    b2 = InlineKeyboardButton(text='Оставить на свободных остатках',
                              callback_data='Оставить на своб. остатках')
    keyboard.row(b1)
    keyboard.row(b2)
    return keyboard


def storage_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Уже существующий склад',
                              callback_data='exist_storage')
    b2 = InlineKeyboardButton(text='Новый склад', callback_data='new_storage')
    keyboard.row(b1)
    keyboard.row(b2)
    return keyboard


def exit_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.row(exit_button)
    return keyboard


def status_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Выдан', callback_data='Выдан')
    b2 = InlineKeyboardButton(text='Принят', callback_data='Принят')
    keyboard.row(b1)
    keyboard.row(b2)
    return keyboard


def reason_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Выбрано неверное наименование',
                              callback_data='Неверное имя')
    b2 = InlineKeyboardButton(text='Указан неверный объём',
                              callback_data='Неверный объём')
    b3 = InlineKeyboardButton(text='Добавлены не соответствующие файлы',
                              callback_data='Некорректные файлы')
    b4 = InlineKeyboardButton(text='Перемещение оформили не на тот склад',
                              callback_data='Не тот склад')
    b5 = InlineKeyboardButton(text='Другое',
                              callback_data='Другое')
    keyboard.row(b1)
    keyboard.row(b2)
    keyboard.row(b3)
    keyboard.row(b4)
    keyboard.row(b5)
    return keyboard


def what_edit():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Выбрано неверное наименование',
                              callback_data='Неверное имя')
    b2 = InlineKeyboardButton(text='Указан неверный объём',
                              callback_data='Неверный объём')
    b3 = InlineKeyboardButton(text='Выбран неправильный склад',
                              callback_data='Неправильный склад')
    b4 = InlineKeyboardButton(text='Указана неверная дата',
                              callback_data='Неверная дата')
    b5 = InlineKeyboardButton(text='Указан неверный поставщик',
                              callback_data='Неверный поставщик')
    b6 = InlineKeyboardButton(text='Указаны неверные дата и номер накладной',
                              callback_data='Неверные дата и накладная')
    b7 = InlineKeyboardButton(text='Прикреплена неверная накладная',
                              callback_data='Неверная накладная')
    b8 = InlineKeyboardButton(
        text='Прикреплён неверный паспорт/сертификат качества',
        callback_data='Неверный паспорт/сертификат')
    b9 = InlineKeyboardButton(text='Другое',
                              callback_data='Другое')
    keyboard.row(b1)
    keyboard.row(b2)
    keyboard.row(b3)
    keyboard.row(b4)
    keyboard.row(b5)
    keyboard.row(b6)
    keyboard.row(b7)
    keyboard.row(b8)
    keyboard.row(b9)
    return keyboard


def adj_inv():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Наименование',
                              callback_data='Наименование')
    b2 = InlineKeyboardButton(text='Единицу измерения',
                              callback_data='Единицу измерения')
    b3 = InlineKeyboardButton(text='Количество материалов',
                              callback_data='Количество материалов')
    keyboard.row(b1)
    keyboard.row(b2)
    keyboard.row(b3)
    return keyboard


class MyPaginator(InlineKeyboardPaginator):
    first_page_label = '<<'
    previous_page_label = '<'
    current_page_label = '-{}-'
    next_page_label = '>'
    last_page_label = '>>'


cb_admin = CallbackData("admin", "action", "id", "user_id")


async def admin_btns_tickets(message, tickets, page=1):
    kb = MyPaginator(len(tickets),
                     current_page=page,
                     data_pattern='ticket#{page}')
    kb.add_before(
        InlineKeyboardButton(text='Взять в работу',
                             callback_data=cb_admin.new(
                                 action='take_to_work',
                                 id=f'{tickets[page - 1].id}',
                                 user_id=f'{tickets[page - 1].sender_user.user_id}'
                             )))
    kb.add_before(InlineKeyboardButton(
        text='Вернуть сотруднику для корректировки запроса',
        callback_data=cb_admin.new(
            action='comeback',
            id=f'{tickets[page - 1].id}',
            user_id=f'{tickets[page - 1].sender_user.user_id}')))
    kb.add_before(InlineKeyboardButton(
        text='Запрос обработан',
        callback_data=cb_admin.new(action='success',
                                   id=f'{tickets[page - 1].id}',
                                   user_id=f'{tickets[page - 1].sender_user.user_id}')))
    msg = ''
    msg += f'1){tickets[page - 1].name}\n'
    msg += f'2){tickets[page - 1].role}\n'
    msg += f'3){tickets[page - 1].request_type}\n'
    msg += f'4){tickets[page - 1].field_one}\n'
    msg += f'5){tickets[page - 1].field_two}\n'
    if tickets[page - 1].field_three is not None:
        msg += f'6){tickets[page - 1].field_three}\n'
    if tickets[page - 1].field_four is not None:
        msg += f'7){tickets[page - 1].field_four}\n'
    if tickets[page - 1].field_five is not None:
        msg += f'8){tickets[page - 1].field_five}\n'
    if tickets[page - 1].field_six is not None:
        msg += f'9){tickets[page - 1].field_six}\n'
    if tickets[page - 1].field_seven is not None:
        msg += f'10){tickets[page - 1].field_seven}\n'
    if tickets[page - 1].field_eight is not None:
        msg += f'11){tickets[page - 1].field_eight}\n'
    if tickets[page - 1].field_nine is not None:
        msg += f'12){tickets[page - 1].field_nine}\n'
    if tickets[page - 1].request_type == 'Корректировка поставок':
        if tickets[page - 1].field_seven != main_const.NO_EXTRA:
            logger.info(tickets[page-1].field_seven)
            await message.answer_document(tickets[page-1].field_one)
            list_ids = tickets[page-1].field_seven.split(', ')
            for i in list_ids:
                await message.answer_document(i)
    else:
        await message.answer_document(tickets[page - 1].field_one)
    await message.answer(msg, reply_markup=kb.markup)


async def moder_btns_tickets(message, tickets, page=1):
    kb = MyPaginator(len(tickets),
                     current_page=page,
                     data_pattern='moderticket#{page}')
    kb.add_before(
        InlineKeyboardButton(text='Взять в работу',
                             callback_data=cb_admin.new(
                                 action='take_to_work',
                                 id=f'{tickets[page - 1].id}',
                                 user_id=f'{tickets[page - 1].sender_user.user_id}'
                             )))
    kb.add_before(InlineKeyboardButton(
        text='Вернуть сотруднику для корректировки запроса',
        callback_data=cb_admin.new(
            action='comeback',
            id=f'{tickets[page - 1].id}',
            user_id=f'{tickets[page - 1].sender_user.user_id}')))
    kb.add_before(InlineKeyboardButton(
        text='Запрос обработан',
        callback_data=cb_admin.new(action='success',
                                   id=f'{tickets[page - 1].id}',
                                   user_id=f'{tickets[page - 1].sender_user.user_id}')))
    msg = ''
    msg += f'1){tickets[page - 1].name}\n'
    msg += f'2){tickets[page - 1].role}\n'
    msg += f'3){tickets[page - 1].request_type}\n'
    msg += f'4){tickets[page - 1].field_one}\n'
    msg += f'5){tickets[page - 1].field_two}\n'
    if tickets[page - 1].field_three is not None:
        msg += f'6){tickets[page - 1].field_three}\n'
    if tickets[page - 1].field_four is not None:
        msg += f'7){tickets[page - 1].field_four}\n'
    if tickets[page - 1].field_five is not None:
        msg += f'8){tickets[page - 1].field_five}\n'
    if tickets[page - 1].field_six is not None:
        msg += f'9){tickets[page - 1].field_six}\n'
    if tickets[page - 1].field_seven is not None:
        msg += f'10){tickets[page - 1].field_seven}\n'
    if tickets[page - 1].field_eight is not None:
        msg += f'11){tickets[page - 1].field_eight}\n'
    if tickets[page - 1].field_nine is not None:
        msg += f'12){tickets[page - 1].field_nine}\n'
    if tickets[page - 1].request_type == 'Добавление материалов на свободный остаток':
        media = types.MediaGroup()
        media.attach_document(types.InputMediaDocument(tickets[page - 1].field_one))
        media.attach_document(types.InputMediaDocument(tickets[page - 1].field_three))
        await message.answer_media_group(media=media)
    elif tickets[page - 1].request_type in ['Корректировка оформленной накладной',
                                            'Смена статуса заявки', ]:
        await message.answer_document(tickets[page - 1].field_one)
    elif tickets[page - 1].request_type == 'Добавление наименований':
        if tickets[page - 1].field_six != '---':
            await message.answer_document(tickets[page - 1].field_six)
    await message.answer(msg, reply_markup=kb.markup)


def user_edit(ticket):
    kb = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Редактировать',
                                  callback_data=cb_admin.new(
                                      action='edit',
                                      id=ticket.id,
                                      user_id=ticket.sender_user_id))
    kb.row(button)
    return kb
