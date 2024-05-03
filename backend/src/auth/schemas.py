from typing import Optional
from datetime import datetime, time

from pydantic import BaseModel

from .models import DomainType, EnvType


class UserBase(BaseModel):
    login: str
    project_id: int
    env: Optional[EnvType]
    domain: Optional[DomainType]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    timestamp: time

    class Config:
        orm_mode = True
