import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

# Models
class UserBase(SQLModel):
    full_name: str
    email: EmailStr

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Data Transfer Objects (DTOs)
# Some DTOs are inspired by Fullstack Fastapi Template: https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/models.py
class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    created_at: str

class UserUpdate(UserBase):
    full_name: str | None = None
    email: EmailStr | None = None

class UpdatePassword(SQLModel):
    current_password: str
    new_password: str
