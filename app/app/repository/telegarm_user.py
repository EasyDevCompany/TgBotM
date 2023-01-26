from .base import RepositoryBase
from app.models.telegram_user import UserType, TelegramUser
from sqlalchemy import or_


class RepositoryTelegramUser(RepositoryBase[TelegramUser]):
    def check_permission_for_one_application(self, user_id: int):
        return self._session.query(self._model).filter(
            self._model.user_type.in_([
                UserType.administrator,
                UserType.technical_support,
                UserType.super_user
            ]), self._model.user_id == user_id
        ).first()

    def check_permission(self, user_id: int, status):
        return self._session.query(self._model).filter(
            or_(
                self._model.user_type == UserType.super_user,
                self._model.user_type == status
            ), self._model.user_id == user_id
        ).first()
