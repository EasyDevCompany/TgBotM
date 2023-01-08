from .base import CustomModelView
from app.models.user import User
from flask_login import current_user


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

    def get_pk_value(self, model):
        user = current_user
        if user.role == User.UsersRoles.super_user:
            return model.id
