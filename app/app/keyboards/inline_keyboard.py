from aiogram import types


start_work = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(
        text="Начать работу",
        callback_data="start_work"
    )
)


# клавиатура с ролями
from aiogram import types


start_work = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(
        text="Начать работу",
        callback_data="start_work"
    )
)


# клавиатура с ролями

accountant = types.InlineKeyboardButton(text="Бухгалтер", callback_data="accountant")
storekeeper = types.InlineKeyboardButton(text="Кладовщик", callback_data="storekeeper")
supervisor = types.InlineKeyboardButton(text="Супервайзер", callback_data="supervisor")
foreman = types.InlineKeyboardButton(text="Прораб", callback_data="foreman")
section_chief = types.InlineKeyboardButton(text="Начальник участка", callback_data="section_chief")
curator = types.InlineKeyboardButton(text="Куратор", callback_data="curator")
department_head = types.InlineKeyboardButton(text="Начальник отдела", callback_data="department_head")
head_of_dec_department = types.InlineKeyboardButton(text="Начальник управления ДИК",
                                                    callback_data="head_of_dec_department")
supply_officer = types.InlineKeyboardButton(text="Сотрудник снабжения", callback_data="supply_officer")
supply_pto = types.InlineKeyboardButton(text="Сотрудник ПТО", callback_data="supply_pto")
account_approve = types.InlineKeyboardButton(text="Утверждающий счета", callback_data="account_approve")
project_manager = types.InlineKeyboardButton(text="Руководитель отдела", callback_data="project_manager")
head_of_the_administrative_and_economic_department = types.InlineKeyboardButton(
    text="Начальник Административно Хозяйственного управления",
    callback_data="head_of_the_administrative_and_economic_department")

role_button_markup = types.InlineKeyboardMarkup(row_width=1)

list_button_roles_callback = (
    ('Бухгалтер', "accountant"),
    ('Кладовщик', "storekeeper"),
    ('Супервайзер', "supervisor"),
    ('Прораб', "foreman"),
    ('Начальник участка', "section_chief"),
    ('Куратор', "curator"),
    ('Начальник отдела', "department_head"),
    ('Начальник управления ДИК', "head_of_dec_department"),
    ('Сотрудник снабжения', 'supply_officer'),
    ("Сотрудник ПТО", 'supply_pto'),
    ("Утверждающий счета",  'account_approve'),
    ("Руководитель отдела", 'project_manager'),
    ("Начальник Административно Хозяйственного управления", 'head_of_the_administrative_and_economic_department'),
)
row_roles = (types.InlineKeyboardButton(text, callback_data=data) for text, data in list_button_roles_callback)
role_button_markup.add(*row_roles)

# клавиатура с запросами

change_status_application = types.InlineKeyboardButton(text="Смена статуса заявки", callback_data="change_status_application")
conversion_factor = types.InlineKeyboardButton(text="Добавление коэффицента пересчета", callback_data="conversion_factor")
warehouse_adjustments = types.InlineKeyboardButton(text="Корректировки склада в заявке", callback_data="warehouse_adjustments")
add_naming = types.InlineKeyboardButton(text="Добавление наименований", callback_data="add_naming")
edit_view_job = types.InlineKeyboardButton(text="Добавление видов работ", callback_data="edit_view_job")
edit_subobject = types.InlineKeyboardButton(text="Редактирование подобъектов", callback_data="edit_subobject")
editing_some_movement = types.InlineKeyboardButton(text="Редактирование некорректного перемещения", callback_data="editing_some_movement")
add_subobject = types.InlineKeyboardButton(text="Добавление подобъектов", callback_data="add_subobject")
add_material = types.InlineKeyboardButton(text="Добавление материалов на свободный остаток", callback_data="add_material")
add_edo = types.InlineKeyboardButton(text="Добавление объекта в ЭДО", callback_data="add_edo")
open_edo = types.InlineKeyboardButton(text="Открытие доступов Эдо для сотрудников", callback_data="open_edo")
edit_some_moving = types.InlineKeyboardButton(text="Редактирование некорректного перемещения", callback_data="edit_some_moving")
adjustment_of_supplies = types.InlineKeyboardButton(text="Корректировка поставок", callback_data="adjustment_of_supplies")

request_button_markup = types.InlineKeyboardMarkup(row_width=1)

list_button_requests_callback = (
    ('Смена статуса заявки', "change_status_application"),
    ('Добавление коэффицента пересчета', "conversion_factor"),
    ('Корректировки склада в заявке', "warehouse_adjustments"),
    ('Добавление наименований', "add_naming"),
    ('Добавление видов работ', "edit_view_job"),
    ('Редактирование подобъектов', "edit_subobject"),
    ('Редактирование некорректного перемещения', "editing_some_movement"),
    ('Добавление подобъектов', "add_subobject"),
    ('Добавление материалов на свободный остаток', 'add_material'),
    ("Добавление объекта в ЭДО", 'add_edo'),
    ("Открытие доступов Эдо для сотрудников",  'open_edo'),
    ("Редактирование некорректного перемещения", 'edit_some_moving'),
    ("Корректировка поставок", 'adjustment_of_supplies'),
)

row_requests = (types.InlineKeyboardButton(text, callback_data=data) for text, data in list_button_requests_callback)
request_button_markup.add(*row_requests)

# клавиатура для запроса служебной записки

file_official_notes = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(
        text="Файл служебной записки",
        callback_data="file_official_notes"
    )
)

# клавиатура финала

ans_yes_no = types.InlineKeyboardMarkup(row_width=1)

text_and_data = (
    ('Да', 'yes'),
    ('Нет', 'no'),
)

ans = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
ans_yes_no.add(*ans)
