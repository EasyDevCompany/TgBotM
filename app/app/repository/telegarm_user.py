from .base import RepositoryBase
from app.models.telegram_user import UserType, TelegramUser
from sqlalchemy import or_


class RepositoryTelegramUser(RepositoryBase[TelegramUser]):

    def check_permission(self, user_id: int):
        return self._session.query(self._model).filter(
            or_(
                self._model.user_type == UserType.administrator,
                self._model.user_type == UserType.technical_support
            ), self._model.user_id == user_id
        ).first()
