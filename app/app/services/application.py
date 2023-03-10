from app.repository.telegarm_user import RepositoryTelegramUser
from app.repository.application import ApplicationRepository
from app.models.application import Application
from loguru import logger
from app.models.telegram_user import UserType


class ApplicationService:

    def __init__(
            self,
            repository_telegram_user: RepositoryTelegramUser,
            repository_application: ApplicationRepository
    ):
        self._repository_application = repository_application
        self._repository_telegram_user = repository_telegram_user

    async def create(self, obj_in: dict, user_id: int):
        user = self._repository_telegram_user.get(user_id=user_id)
        obj_in["user_id"] = user.id
        obj_in["user"] = user
        logger.info(obj_in)
        return self._repository_application.create(
            obj_in=obj_in,
            commit=True
        )

    async def get(self, application_id: int):
        return self._repository_application.get(id=application_id)

    async def applications_for(self, roles):
        return self._repository_application.list(
            request_answered=roles
        )

    async def update(self, application_id: int, obj_in: dict, user_id: int = None):
        if user_id is not None:
            user = self._repository_telegram_user.get(user_id=user_id)
            obj_in['recipient_user_id'] = user.id
            obj_in['recipient_user'] = user
        return self._repository_application.update(
            db_obj=self._repository_application.get(id=application_id),
            obj_in=obj_in,
        )

    async def get_application_for_user(self, user_id: int, application_id: int):
        user = self._repository_telegram_user.get(user_id=user_id)
        application = self._repository_application.get(id=application_id)
        if (application is not None) and (user.user_type == application.request_answered or
                                          user.user_type == UserType.super_user):
            return application
        return None

    async def application_for_user(self, user_id: int):
        user = self._repository_telegram_user.get(user_id=user_id)
        return self._repository_application.list(sender_user_id=user.id)

