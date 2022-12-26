from repository.telegarm_user import RepositoryTelegramUser
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

