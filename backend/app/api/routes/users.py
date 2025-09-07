from fastapi import APIRouter
from app.services import user_service

router = APIRouter()


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):