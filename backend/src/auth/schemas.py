from typing import Optional
from datetime import datetime, time

from pydantic import BaseModel

from .models import DomainType, EnvType


class UserBase(BaseModel):
    """Базовая схема для модели пользователя."""

    login: str
    project_id: int
    env: Optional[EnvType]
    domain: Optional[DomainType]


class UserCreate(UserBase):
    """Схема модели пользователя для создания записи в БД."""

    password: str


class User(UserBase):
    """Схема модели пользователя для чтения."""

    id: int
    created_at: datetime
    timestamp: time | None

    class Config:
        orm_mode = True
