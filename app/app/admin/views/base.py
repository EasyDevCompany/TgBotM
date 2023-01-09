from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app.models.user import User
from loguru import logger
from flask import abort


class AdminModelView(ModelView):
    def is_accessible(self):
        user = current_user
        if user.role == User.UsersRoles.super_user:
            return user.is_authenticated


class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
