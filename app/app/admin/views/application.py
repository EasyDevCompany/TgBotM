from .base import CustomModelView
from app.models.user import User
from flask_login import current_user
from app.models.application import Application


class ApplicationView(CustomModelView):
    page_size = 30
    can_view_details = True
    column_list = [
        'id',
        'role',
        'date',
        'sender_user_id',
        'recipient_user_id',
        'application_status',
        'request_answered',
        'request_type',
        'field_one',
        'field_two',
        'field_three',
        'field_four',
        'field_five',
        'field_six',
        'field_seven',
        'field_eight',
        'field_nine'
    ]
    column_filters = [
        "application_status",
        "request_answered",
        "date",
        "role",
        "request_type"
    ]

    def get_pk_value(self, model):
        user = current_user
        if user.role == User.UsersRoles.moderator:
            if model.request_answered == Application.RequestAnswered.moderator:
                return model.id
        elif user.role == User.UsersRoles.admin:
            if model.request_answered == Application.RequestAnswered.admin:
                return model.id
        else:
            return model.id
