from .base import CustomModelView


class ApplicationView(CustomModelView):
    column_list = [
        "id",
        "user_id",
        "date",
        "role",
        "request_answered",
        "request_type",
        "field_one",
        "field_two",
        "field_four",
        "field_five",
        "six_field",
        "seven_field",
        "eight_field",
        "nine_field"
    ]

    column_filters = [
        "date",
        "role",
        "request_answered",
        "request_type"
    ]
