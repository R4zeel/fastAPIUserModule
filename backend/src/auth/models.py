from sqlalchemy import Column, Integer, String, DateTime, Time

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, autoincrement=True)
    project_id = Column(Integer)
    env = Column(String)
    domain = Column(String)
    timestamp = Column(Time)
