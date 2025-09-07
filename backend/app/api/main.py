from fastapi import APIRouter

from app.api.routes import users
from app.core.db import init_db, get_session

api_router = APIRouter()
api_router.include_router(users.router)

init_db(session=get_session())
