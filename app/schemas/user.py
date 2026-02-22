from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: bool | None = True


# Properties to run when creating user
class UserCreate(UserBase):
    password: str
    roles: UserRole | None = UserRole.USER


# Admin/Superadmin properties when updating user
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    is_active: bool | None = None
    roles: UserRole | None = None


# Current user properties when updating own profile
class UserUpdateMe(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str


# Properties to return via API
class UserResponse(UserBase):
    id: int
    roles: UserRole
    time_added: datetime | None = None

    class Config:
        from_attributes = True


# Properties to return for pagination
class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
