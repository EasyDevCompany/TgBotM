from dependency_injector import containers, providers
from app.core.config import Settings
from app.db.session import SyncSession

from app.models.telegram_user import TelegramUser

from app.repository.telegarm_user import RepositoryTelegramUser

from app.services.tg_user_service import TelegramUserService


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)
    db = providers.Singleton(SyncSession, db_url=config.provided.SYNC_SQLALCHEMY_DATABASE_URI)

    repository_telegram_user = providers.Singleton(RepositoryTelegramUser, model=TelegramUser, session=db)

    telegram_user_service = providers.Singleton(
        TelegramUserService,
        repository_telegram_user=repository_telegram_user
    )