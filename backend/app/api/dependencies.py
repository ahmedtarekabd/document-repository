from typing import Annotated
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError


from fastapi import Header, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.core.config import settings
from app.core.security import verify_password
from app.models import User, TokenData
from app.core.db import SessionDep


# User & Auth dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.API_V1_STR + "/users/login")

async def get_token_header(
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if authorization.split()[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    return authorization.split()[1]

def get_user(session: Session, email: str):
    user = session.exec(
        select(User).where(User.email == email)
    ).first()
    return user

def authenticate_user(fake_db, email: str, password: str) -> bool | User:
    user = get_user(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

current_user_dep = Annotated[User, Depends(get_current_user)]
