from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Association / link tables (composite primary keys)
class UserDepartment(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    department_id: Optional[int] = Field(default=None, foreign_key="departments.id", primary_key=True)


class TagDocument(SQLModel, table=True):
    document_id: Optional[int] = Field(default=None, foreign_key="documents.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)


class RolePermission(SQLModel, table=True):
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id", primary_key=True)
    permission_id: Optional[int] = Field(default=None, foreign_key="permissions.permission_id", primary_key=True)


class DepartmentDocumentAccess(SQLModel, table=True):
    department_id: Optional[int] = Field(default=None, foreign_key="departments.id", primary_key=True)
    document_id: Optional[int] = Field(default=None, foreign_key="documents.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id", primary_key=True)


class UserDocumentAccess(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    document_id: Optional[int] = Field(default=None, foreign_key="documents.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id", primary_key=True)


# Core models
class UserBase(SQLModel):
    name: str
    email: EmailStr
    password: str


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    departments: List[Department] | list = Relationship(back_populates="users", link_model=UserDepartment)
    documents: List[Document] | list = Relationship(back_populates="owner")
    document_access: List[Document] | list = Relationship(back_populates="users_with_access", link_model=UserDocumentAccess)


class UserCreate(SQLModel):
    name: str
    email: EmailStr
    password: str


class UserRead(SQLModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


class DepartmentBase(SQLModel):
    name: str


class Department(DepartmentBase, table=True):
    __tablename__ = "departments"

    id: int | None = Field(default=None, primary_key=True)
    users: List[User] | list = Relationship(back_populates="departments", link_model=UserDepartment)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase):
    id: int


class DocumentBase(SQLModel):
    title: str
    description: Optional[str] = None


class Document(DocumentBase, table=True):
    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id")
    owner: Optional[User] = Relationship(back_populates="documents")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    tags: List[Tag] | list = Relationship(back_populates="documents", link_model=TagDocument)
    users_with_access: List[User] | list = Relationship(back_populates="document_access", link_model=UserDocumentAccess)


class DocumentCreate(DocumentBase):
    pass


class DocumentRead(DocumentBase):
    id: int
    owner_id: int
    created_at: datetime


class DocumentVersion(SQLModel, table=True):
    __tablename__ = "document_versions"

    id: int | None = Field(default=None, primary_key=True)
    document_id: int = Field(foreign_key="documents.id")
    version_number: int = Field(default=1)
    path_url: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TagBase(SQLModel):
    name: str


class Tag(TagBase, table=True):
    __tablename__ = "tags"

    id: int | None = Field(default=None, primary_key=True)
    documents: List[Document] | list = Relationship(back_populates="tags", link_model=TagDocument)


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int


class RoleBase(SQLModel):
    name: str


class Role(RoleBase, table=True):
    __tablename__ = "roles"

    id: int | None = Field(default=None, primary_key=True)
    users: List[User] | list = Relationship(back_populates="roles", link_model=UserDepartment)
    permissions: List["Permission"] | list = Relationship(back_populates="roles", link_model=RolePermission)


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int


class PermissionBase(SQLModel):
    permission_name: str
    description: Optional[str] = None


class Permission(PermissionBase, table=True):
    __tablename__ = "permissions"

    permission_id: int | None = Field(default=None, primary_key=True)
    roles: List[Role] | list = Relationship(back_populates="permissions", link_model=RolePermission)


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    permission_id: int


# Auth pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    exp: Optional[int] = None
