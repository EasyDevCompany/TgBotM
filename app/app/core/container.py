import os
from dependency_injector import containers, providers
from core.config import Settings
from db.session import SyncSession

from models.telegram_user import TelegramUser

from repository.telegarm_user import RepositoryTelegramUser

from services.tg_user_service import TelegramUserService
from dotenv import load_dotenv

load_dotenv


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings,
                                 POSTGRES_USER=os.getenv("POSTGRES_USER"),
                                 POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
                                 POSTGRES_SERVER=os.getenv("POSTGRES_SERVER"),
                                 POSTGRES_DB=os.getenv("POSTGRES_DB"),
                                 BOT_TOKEN=os.getenv('TOKEN'))
    db = providers.Singleton(SyncSession, db_url=config.provided.SYNC_SQLALCHEMY_DATABASE_URI)

    repository_telegram_user = providers.Singleton(RepositoryTelegramUser, model=TelegramUser, session=db)

    telegram_user_service = providers.Singleton(
        TelegramUserService,
        repository_telegram_user=repository_telegram_user
    )