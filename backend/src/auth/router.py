from datetime import datetime

from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.exceptions import ValidationException
from sqlalchemy.orm import Session

from .dependencies import get_db
from . import crud
from . import models
from . import schemas

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.User).filter(models.User.login == user.login).first()
    )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/users/{user_id}/lock/", response_model=schemas.User)
def acquire_lock(user_id: int, db: Session = Depends(get_db)):
    """
    Присваивание пользователю временной метки, сигнализирующей о том,
    что пользователь заблокирован для использования.
    """
    db_user = crud.get_user(db, user_id)
    lock_time = datetime.now().time()
    if db_user.timestamp:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"User is locked, lock time {lock_time}",
        )
    db_user.timestamp = lock_time
    db.commit()
    return Response(
        f"Lock created, lock time {lock_time}",
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/users/{user_id}/release_lock/", response_model=schemas.User)
def release_lock(user_id: int, db: Session = Depends(get_db)):
    """
    Снятие блокировки с пользователя и установка
    значения временной метки на None.
    """
    db_user = crud.get_user(db, user_id)
    if not db_user.timestamp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not locked",
        )
    db_user.timestamp = None
    db.commit()
    return Response(
        "User lock released",
        status_code=status.HTTP_200_OK,
    )
