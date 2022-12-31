from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import const_add_subobjects as const


start_work = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Начать работу",
        callback_data="start_work"
    )
)


exit_button = InlineKeyboardButton(text='Отмена', callback_data="exit")
skip_button = InlineKeyboardButton(text='Пропустить', callback_data='skip')


def genmarkup(data):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    for i in range(1, len(data) + 1):
        keyboard.add(InlineKeyboardButton(i, callback_data=i))
    return keyboard


def choose_your_role():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Бухгалтер', callback_data='Бухгалтер')
    b2 = InlineKeyboardButton(text='Кладовщик', callback_data='Кладовщик')
    b3 = InlineKeyboardButton(text='Супервайзер', callback_data='Супервайзер')
    b4 = InlineKeyboardButton(text='Прораб', callback_data='Прораб')
    b5 = InlineKeyboardButton(text='Начальник Участка',
                              callback_data='Начальник Участка')
    b6 = InlineKeyboardButton(text='Куратор', callback_data='Куратор')
    b7 = InlineKeyboardButton(text='Начальник Отдела',
                              callback_data='Начальник Отдела')
    b8 = InlineKeyboardButton(text='Начальник управления ДИК',
                              callback_data='Начальник управления ДИК')
    b9 = InlineKeyboardButton(text='Сотрудник снабжения',
                              callback_data='Сотрудник снабжения')
    b10 = InlineKeyboardButton(text='Сотрудник ПТО',
                               callback_data='Сотрудник ПТО')
    b11 = InlineKeyboardButton(text='Утверждающий счета',
                               callback_data='Утверждающий счета')
    b12 = InlineKeyboardButton(text='Руководитель проекта',
                               callback_data='Руководитель проекта')
    b13 = InlineKeyboardButton(
        text='Начальник Административно-Хозяйственного управления',
        callback_data='Начальник АХУ')
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
        callback_data='prepare')
    b2 = InlineKeyboardButton(
        text=const.CHAPTERS['main_objects'],
        callback_data='main_objects')
    b3 = InlineKeyboardButton(
        text=const.CHAPTERS['extra_objects'],
        callback_data='extra_objects')
    b4 = InlineKeyboardButton(
        text=const.CHAPTERS['energy_objects'],
        callback_data='energy_objects')
    b5 = InlineKeyboardButton(
        text=const.CHAPTERS['transport_objects'],
        callback_data='transport_objects')
    b6 = InlineKeyboardButton(
        text=const.CHAPTERS['zhkh_objects'],
        callback_data='zhkh_objects')
    b7 = InlineKeyboardButton(
        text=const.CHAPTERS['green_objects'],
        callback_data='green_objects')
    b8 = InlineKeyboardButton(
        text=const.CHAPTERS['temp_objects'],
        callback_data='temp_objects')
    b9 = InlineKeyboardButton(
        text=const.CHAPTERS['other_work'],
        callback_data='other_work')
    b10 = InlineKeyboardButton(
        text=const.CHAPTERS['another_payments'],
        callback_data='another_payments')
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
    b1 = InlineKeyboardButton(text='Резервировать', callback_data='reserve')
    b2 = InlineKeyboardButton(text='Оставить на свободных остатках',
                              callback_data='leave')
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
                              callback_data='invoice_name')
    b2 = InlineKeyboardButton(text='Единицу измерения',
                              callback_data='measurement_unit')
    b3 = InlineKeyboardButton(text='Количество материалов',
                              callback_data='quantity_material')
    keyboard.row(b1)
    keyboard.row(b2)
    keyboard.row(b3)
    return keyboard
