from .base import AdminModelView


class UsersViews(AdminModelView):
    column_list = [
        "id",
        "login",
        "password",
        "role"
    ]
    column_filters = ["role"]
