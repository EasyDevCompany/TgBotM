from app.repository.telegarm_user import RepositoryTelegramUser
from typing import Any
from app.models.telegram_user import TelegramUser
from loguru import logger


class TelegramUserService:

    def __init__(self, repository_telegram_user: RepositoryTelegramUser):
        self._repository_telegram_user = repository_telegram_user

    async def get_or_create(self, obj_in: Any):
        if isinstance(obj_in, dict):
            user = self._repository_telegram_user.get(user_id=int(obj_in.get("user_id")))
            if user is not None:
                return user
            return self._repository_telegram_user.create(obj_in=obj_in, commit=True)

        return self._repository_telegram_user.get(user_id=obj_in)

    async def user_permission(self, user_id: int) -> bool:
        user = self._repository_telegram_user.check_permission_for_one_application(user_id=user_id)
        logger.info(user)
        if user is None:
            return False
        return True

    async def check_permission_for_user(self, user_id: int, user_type) -> bool:
        user = self._repository_telegram_user.check_permission(user_id=user_id, status=user_type)
        if user is None:
            return False
        return True
