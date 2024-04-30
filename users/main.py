from fastapi import FastAPI

from api.base import api_router

app = FastAPI()
app.include_router(api_router)
