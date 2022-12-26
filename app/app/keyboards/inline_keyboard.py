from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_inline_paginations.paginator import Paginator
from loader import dp


start_work = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Начать работу",
        callback_data="start_work"
    )
)


def choose_your_role():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Бухгалтер', callback_data='1')
    b2 = InlineKeyboardButton(text='Кладовщик', callback_data='2')
    b3 = InlineKeyboardButton(text='Супервайзер', callback_data='3')
    b4 = InlineKeyboardButton(text='Прораб', callback_data='4')
    b5 = InlineKeyboardButton(text='Начальник Участка', callback_data='5')
    b6 = InlineKeyboardButton(text='Куратор', callback_data='6')
    b7 = InlineKeyboardButton(text='Начальник Отдела', callback_data='7')
    b8 = InlineKeyboardButton(text='Начальник управления ДИК', callback_data='8')
    b9 = InlineKeyboardButton(text='Сотрудник снабжения', callback_data='9')
    b10 = InlineKeyboardButton(text='Сотрудник ПТО', callback_data='10')
    b11 = InlineKeyboardButton(text='Утверждающий счета', callback_data='11')
    b12 = InlineKeyboardButton(text='Руководитель проекта', callback_data='12')
    b13 = InlineKeyboardButton(text='Начальник Административно-Хозяйственного управления', callback_data='13')
    keyboard.row(b1, b2)
    keyboard.row(b3, b4)
    keyboard.row(b5, b6)
    keyboard.row(b7, b8)
    keyboard.row(b9, b10)
    keyboard.row(b11, b12)
    keyboard.row(b13)
    return keyboard


role = Paginator(data=choose_your_role(), size=3, dp=dp)


def create_ticket():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Создать запрос', callback_data='create_ticket')
    keyboard.row(b1)
    return keyboard


def tech_or_admin():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Тех.поддержка', callback_data='tech')
    b2 = InlineKeyboardButton(text='Администатор', callback_data='admin')
    keyboard.row(b1, b2)
    return keyboard

def tech_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Смена статуса заявки', callback_data='change_status')
    b2 = InlineKeyboardButton(text='Добавление коэффициента пересчёта по наименованию', callback_data='add_coef')
    b3 = InlineKeyboardButton(text='Корректировка склада в заявке', callback_data='update_storage')
    b4 = InlineKeyboardButton(text='Добавление наименований', callback_data='add_names')
    b5 = InlineKeyboardButton(text='Редактирование видов работ', callback_data='edit_type_work')
    b6 = InlineKeyboardButton(text='Добавление видов работ', callback_data='add_type_work')
    b7 = InlineKeyboardButton(text='Редактирование подобъектов', callback_data='edit_subobject')
    b8 = InlineKeyboardButton(text='Редактирование некорректного перемещения', callback_data='edit_incorrect_move')
    b9 = InlineKeyboardButton(text='Добавление подобъектов', callback_data='add_subobject')
    b10 = InlineKeyboardButton(text='Добавление материалов на свободный остаток', callback_data='add_materials')
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


tech = Paginator(data=tech_kb(), size=4, dp=dp)


def admin_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Добавление объекта в ЭДО', callback_data='add_EDO')
    b2 = InlineKeyboardButton(text='Открытие доступов в ЭДО для сотрудников', callback_data='open_access')
    b3 = InlineKeyboardButton(text='Редактирование некорректного перемещения', callback_data='edit_incorrect_move_admin')
    b4 = InlineKeyboardButton(text='Корректировка поставок', callback_data='edit_shipment')
    keyboard.row(b1)
    keyboard.row(b2)
    keyboard.row(b3)
    keyboard.row(b4)
    return keyboard
