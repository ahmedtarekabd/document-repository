from fastapi import Depends, FastAPI

from app.dependencies import get_query_token, get_token_header
from app.routers import users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
