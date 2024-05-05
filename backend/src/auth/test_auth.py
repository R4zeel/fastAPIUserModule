import pytest
from fastapi import status
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .crud import create_user
from src.database import Base, engine
from src.main import app
from .dependencies import get_db
from . import models

TEST_PAYLOAD = {
    "login": "test",
    "project_id": 1,
    "env": "stage",
    "domain": "canary",
    "password": "testp@ss",
}
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_user_create(test_db):
    response = client.post("/users/", json=TEST_PAYLOAD)
    assert response.status_code == status.HTTP_200_OK


def test_create_user_with_invalid_data(test_db):
    test_payload = {
        "login": "test",
        "password": "testp@ss",
        "project_id": "1",
        "domain": "canare",
        "env": "test",
    }
    response = client.post("/users/", json=test_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_users_list(test_db):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK


def test_user_lock(test_db):
    test_user = client.post("/users/", json=TEST_PAYLOAD)
    response = client.post("/users/1/lock/")
    assert response.status_code == status.HTTP_201_CREATED


def test_locked_user(test_db):
    test_uesr = client.post("/users/", json=TEST_PAYLOAD)
    lock = client.post("/users/1/lock/")
    response = client.post("/users/1/lock/")
    assert response.status_code == status.HTTP_423_LOCKED


def test_user_release_lock(test_db):
    test_uesr = client.post("/users/", json=TEST_PAYLOAD)
    lock = client.post("/users/1/lock/")
    response = client.post("/users/1/release_lock/")
    assert response.status_code == status.HTTP_200_OK


def test_unlocked_user(test_db):
    test_user = client.post("/users/", json=TEST_PAYLOAD)
    response = client.post("/users/1/release_lock/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
