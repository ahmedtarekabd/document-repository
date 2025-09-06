from fastapi import APIRouter

router = APIRouter()


fake_users_db = {
    "rick": {"name": "Rick Sanchez", "email": "rick@example.com"},
    "morty": {"name": "Morty Smith", "email": "morty@example.com"},
}


@router.get("/users/", tags=["users"])
async def read_users():
    return fake_users_db


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
