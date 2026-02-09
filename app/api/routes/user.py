from fastapi import APIRouter

from app.models import AppUserModel

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("/", response_model=AppUserModel):
    pass