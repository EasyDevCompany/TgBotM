from app.repository.telegarm_user import RepositoryTelegramUser
from app.models.telegram_user import TelegramUser
from typing import Any


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

    async def users_list(self, user_type):
        if user_type == 'admin':
            user_list = self._repository_telegram_user.list(user_type=TelegramUser.UserType.administrator)
        elif user_type == 'moder':
            user_list = self._repository_telegram_user.list(user_type=TelegramUser.UserType.technical_support)
        ids = []
        for user in user_list:
            ids.append(user.user_id)
        return ids