from app.models.telegram_user import UserType
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
        obj_in['sender_user_id'] = user.id
        obj_in['sender_user'] = user
        logger.info(obj_in)
        return self._repository_application.create(
            obj_in=obj_in,
            commit=True
        )

    async def get(self, application_id: int):
        return self._repository_application.get(id=application_id)

    async def get_last(self):
        return self._repository_application.get()

    async def applications_for(self, roles: UserType):
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
            commit=True
        )

    async def get_application_for_user(self, user_id: int, application_id: int):
        user = self._repository_telegram_user.get(user_id=user_id)
        application = self._repository_application.get(id=application_id)
        if (application is None) or (user.user_type != application.request_answered):
            return None
        return application

    async def delete(self, application_id: int):
        db_obj = self._repository_application.get(id=application_id)
        return self._repository_application.delete(db_obj=db_obj,
                                                   commit=True)

    async def application_for_user(self, user_id: int):
        user = self._repository_telegram_user.get(user_id=user_id)
        return self._repository_application.list(sender_user_id=user.id)


    # async def check_application(self) -> bool:
    #     app = self._repository_application.check_not_success()
    #     if app is None:
    #         return False
    #     return True
