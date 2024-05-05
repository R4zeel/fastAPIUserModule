from sqlalchemy.orm import Session

from . import models
from . import schemas
from . import utils


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(
        login=user.login,
        env=user.env,
        domain=user.domain,
        project_id=user.project_id,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
