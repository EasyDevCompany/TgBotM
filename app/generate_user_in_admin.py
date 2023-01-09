from string import (
    ascii_lowercase,
    ascii_uppercase,
    digits
)
from random import choice
from loguru import logger

from app.db.session import SyncSession
from app.models.user import User
from app.core.config import settings

PASSWORD_LENGTH = 10


def generate_password() -> str:
    chars = ascii_lowercase + ascii_uppercase + digits
    gen_password = ""
    for _ in range(PASSWORD_LENGTH):
        gen_password += choice(chars)
    return gen_password


if __name__ == "__main__":
    session = SyncSession(settings.SYNC_SQLALCHEMY_DATABASE_URI)
    login = input("Придумайте логин: ")
    password = generate_password()
    logger.info(f"""
    Generate user with login: {login} and password: {password}
    """)
    user = User(
        login=login,
        password=password,
        active=True,
        role=User.UsersRoles.super_user
    )
    session.session.add(user)
    session.session.commit()
