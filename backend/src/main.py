from fastapi import FastAPI

from .database import engine
from .auth import models
from .auth.router import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
