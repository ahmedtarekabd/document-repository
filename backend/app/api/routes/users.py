from typing import Annotated, Any
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_user, authenticate_user, create_access_token, current_user_dep
from app.models.users import User, UserCreate, UserRead
from app.core.config import settings
from app.models.auth import Token
from app.core.db import SessionDep
from app.core.security import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/signup")
def register_user(user_data: UserCreate, session: SessionDep):
    # Check if user already exists
    db_user = get_user(session, user_data.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    try:
        print('user_data', user_data)
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hashed_password
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating user: {str(e)}"
        )
    
    return db_user

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: current_user_dep,
):
    return current_user
