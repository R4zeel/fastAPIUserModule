import enum

from sqlalchemy import Column, Integer, String, DateTime, Time, types, Enum
from sqlalchemy.sql import func
from sqlalchemy.sql.elements import Null

from src.database import Base

MAX_STR_LEN = 128


class EnvType(enum.Enum):
    """Доступные значения для поля Env модели пользователя."""

    prod = "prod"
    preprod = "preprod"
    stage = "stage"


class DomainType(enum.Enum):
    """Доступные значения для поля Domain модели пользователя."""

    canary = "canary"
    regular = "regular"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    project_id = Column(Integer, nullable=True, default=None)
    env = Column(Enum(EnvType))
    domain = Column(Enum(DomainType))
    timestamp = Column(Time, nullable=True, default=None)
