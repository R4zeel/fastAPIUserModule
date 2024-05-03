import enum

from sqlalchemy import Column, Integer, String, DateTime, Time, types, Enum
from sqlalchemy.sql import func

from src.database import Base


class EnvType(enum.Enum):
    prod = "prod"
    preprod = "preprod"
    stage = "stage"


class DomainType(enum.Enum):
    canary = "canary"
    regular = "regular"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    project_id = Column(Integer)
    env = Column(Enum(EnvType))
    domain = Column(Enum(DomainType))
    timestamp = Column(Time, nullable=True)
