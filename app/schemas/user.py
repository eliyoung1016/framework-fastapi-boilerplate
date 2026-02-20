from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: Optional[bool] = True

# Properties to run when creating user
class UserCreate(UserBase):
    password: str
    roles: Optional[UserRole] = UserRole.USER

# Admin/Superadmin properties when updating user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    roles: Optional[UserRole] = None

# Current user properties when updating own profile
class UserUpdateMe(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str

# Properties to return via API
class UserResponse(UserBase):
    id: int
    roles: UserRole
    time_added: Optional[datetime] = None

    class Config:
        from_attributes = True

# Properties to return for pagination
class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
