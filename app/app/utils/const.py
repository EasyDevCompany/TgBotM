START_MESSAGE = "Здравствуйте, данный бот помогает вам создавать запросы для" \
                " обработки администратором или сотрудником технической поддержки.\n\n" \
                "Что умеет этот бот:\n" \
                "• создание запросов для обработки сотрудником тех. поддержки/администратором в ЭДО\n" \
                "• отслеживание статуса готовности\n" \
                "• связь с сотрудником, обрабатывающим запрос\n" \
                "• возможность корректировать свой запрос\n" \
                "• возможность отменить некорректный запрос\n\n" \
                "Чтобы начать работу, нажмите кнопку «Начать работу»"

HASE_NOT_PERMISSION = "Увас нет прав для совершения этих действий"
GET_ID = "Отправьте id заявки, которую хотите рассмотреть."
NOT_TEXT = "ID заявки не должен быть текстом"
APPLICATION_ERROR = "Заявка, которую вы пытаетесь рассмотреть принадлежит не вашему статусу, либо ее не существует"
SEND_APPLICATION = "ID заявки: {application_id}\n\n" \
                   "Роль: {role}\n" \
                   "Тип заявки: {request_type}\n"\
                   "{one}\n"\
                   "{two}\n"\
                   "{three}\n"\
                   "{four}\n"\
                   "{five}\n"\
                   "{six}\n"\
                   "{seven}\n"\
                   "{eight}\n"\
                   "{nine}\n"\

STATUS_CHANGE_DONE = "Статус заявки изменен: {message}"
MESSAGE_FOR_SENDER = """
Статус вашей заявки изменен.
Уникальный id заявки: {application_id}
Тип заявки: {application_type}
"""
RETURN_COMMENT = """
Напишите комментарий к заявке, чтобы по нему
пользователь мог изменить заявку.
"""
COMMENT_SEND = "Комметарий отправлен!"
MESSAGE_FOR_SENDER_IF_RETURN = """
Ваша заявка была возращени для доработки,
отредактируйте ее, чтобы вернуть ее в работу.

Уникальный ID заявки: {application_id}
Ваша роль: {role}
Тип заявки: {request_type}
{one}
{two}
{three}
{four}
{five}
{six}
{seven}
{eight}
{nine}
"""

CHOOSE_FIELD = """
Выберите поле, которое хотите отредактировать:
"""

WHAT_EDIT = """
Исправьте выбранное вами поле в соответсвии с комментарием:
"""

CHANGE_SAVED = """
Изменения сохранены!
"""

SENDER_CHANGE_APPLICATION_MESSAGE = """
Заявитель внес изменения в заявку, просмотрите!
ID заявки: {application_id}
"""