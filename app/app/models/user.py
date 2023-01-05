import enum

from app.db.base_class import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum
)
from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = "users"

    class UsersRoles(enum.Enum):
        super_user = "super_user"
        moderator = "moderator"
        admin = "admin"

    id = Column(Integer(), primary_key=True)
    login = Column(String(255))
    password = Column(String(80))
    active = Column(Boolean())
    role = Column(Enum(UsersRoles))


