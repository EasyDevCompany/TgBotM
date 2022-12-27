import os
from dependency_injector import containers, providers
from core.config import Settings
from db.session import SyncSession

from app.models.telegram_user import TelegramUser
from app.models.application import Application

from app.repository.telegarm_user import RepositoryTelegramUser
from app.repository.application import ApplicationRepository

from app.services.tg_user_service import TelegramUserService
from app.services.application import ApplicationService


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings,
                                 POSTGRES_USER=os.getenv("POSTGRES_USER"),
                                 POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
                                 POSTGRES_SERVER=os.getenv("POSTGRES_SERVER"),
                                 POSTGRES_DB=os.getenv("POSTGRES_DB"),
                                 BOT_TOKEN=os.getenv('TOKEN'))
    db = providers.Singleton(SyncSession, db_url=config.provided.SYNC_SQLALCHEMY_DATABASE_URI)

    repository_telegram_user = providers.Singleton(RepositoryTelegramUser, model=TelegramUser, session=db)
    repository_application = providers.Singleton(ApplicationRepository, model=Application, session=db)

    telegram_user_service = providers.Singleton(
        TelegramUserService,
        repository_telegram_user=repository_telegram_user
    )
    application_service = providers.Singleton(
        ApplicationService,
        repository_telegram_user=repository_telegram_user,
        repository_application=repository_application

    )
