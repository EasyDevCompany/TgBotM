import enum

from app.db.base_class import Base
from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Enum,
    DateTime
)
from sqlalchemy.sql import func


class UserType(str, enum.Enum):
    employee = "employee"
    technical_support = "technical_support"
    administrator = "administrator"
    super_user = "super_user"


class TelegramUser(Base):
    __tablename__ = "telegramuser"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    last_action = Column(DateTime, nullable=True, onupdate=func.now())
    user_type = Column(Enum(UserType))

    def __repr__(self) -> str:
        return f"{self.username} {self.first_name}"
