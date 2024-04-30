from fastapi import APIRouter

from .v1.routers import router

api_router = APIRouter()
api_router.include_router(router, prefix="", tags=["users"])
