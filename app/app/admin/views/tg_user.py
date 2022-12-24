from .base import CustomModelView


class TelegramUserView(CustomModelView):
    column_list = [
        "id",
        "user_id",
        "username",
        "first_name",
        "registration_date",
        "last_action",
        "user_type"
    ]

    column_filters = ["user_type", "last_action", "registration_date"]