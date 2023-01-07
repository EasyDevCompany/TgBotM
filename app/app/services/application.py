from app.repository.telegarm_user import RepositoryTelegramUser
from app.repository.application import ApplicationRepository
from app.models.application import Application
from loguru import logger


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

    async def applications_for(self, roles: Application.RequestAnswered):
        return self._repository_application.list(
            request_answered=roles
        )

    async def update(self, application_id: int, obj_in: dict):
        return self._repository_application.update(
            db_obj=self._repository_application.get(id=application_id),
            obj_in=obj_in
        )
