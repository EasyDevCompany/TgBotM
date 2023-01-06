from .base import CustomModelView


class ApplicationView(CustomModelView):
    column_list = [
        'id',
        'role',
        'date',
        'user_id',
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
