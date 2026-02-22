from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.models.user import User, UserRole
from app.schemas.user import (
    UserCreate,
    UserListResponse,
    UserPasswordUpdate,
    UserResponse,
    UserUpdateMe,
)

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create new user. (Admin only)
    """
    user = (
        db.query(User)
        .filter((User.email == user_in.email) | (User.username == user_in.username))
        .first()
    )
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this user name or email already exists in the system.",
        )

    # Avoid creating superadmins if not superadmin
    if (
        user_in.roles == UserRole.SUPERADMIN
        and current_user.roles != UserRole.SUPERADMIN
    ):
        raise HTTPException(
            status_code=403, detail="Not enough privileges to create Superadmin"
        )

    hashed_password = security.get_password_hash(user_in.password)
    db_obj = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        roles=user_in.roles,
        is_active=user_in.is_active,
        added_by=current_user.username,
        time_added=datetime.now(timezone.utc),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdateMe,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user profile.
    """
    if user_in.email:
        existing_email = (
            db.query(User)
            .filter(User.email == user_in.email, User.id != current_user.id)
            .first()
        )
        if existing_email:
            raise HTTPException(status_code=409, detail="Email already taken")
        current_user.email = user_in.email
    if user_in.username:
        existing_username = (
            db.query(User)
            .filter(User.username == user_in.username, User.id != current_user.id)
            .first()
        )
        if existing_username:
            raise HTTPException(status_code=409, detail="Username already taken")
        current_user.username = user_in.username

    current_user.last_updated_by = current_user.username
    current_user.last_update_time = datetime.now(timezone.utc)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.patch("/me/password")
def update_password_me(
    *,
    db: Session = Depends(deps.get_db),
    body: UserPasswordUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own password.
    """
    if not security.verify_password(
        body.current_password, current_user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect password")

    hashed_password = security.get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    current_user.last_updated_by = current_user.username
    current_user.last_update_time = datetime.now(timezone.utc)
    db.add(current_user)
    db.commit()
    return {"msg": "Password updated successfully"}


@router.get("/", response_model=UserListResponse)
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Retrieve users. (Admin only)
    """
    query = db.query(User).filter(User.is_deleted == False)
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    return {"items": users, "total": total}


@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Get a specific user by id. (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}/disable", response_model=UserResponse)
def disable_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Disable a user. (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Users cannot disable themselves")

    # Avoid admins disabling superadmins
    if user.roles == UserRole.SUPERADMIN and current_user.roles != UserRole.SUPERADMIN:
        raise HTTPException(status_code=403, detail="Not enough privileges")

    user.is_active = False
    user.last_updated_by = current_user.username
    user.last_update_time = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=UserResponse)
def soft_delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Soft delete a user. (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Users cannot delete themselves")

    # Avoid admins deleting superadmins
    if user.roles == UserRole.SUPERADMIN and current_user.roles != UserRole.SUPERADMIN:
        raise HTTPException(status_code=403, detail="Not enough privileges")

    user.is_deleted = True
    user.is_active = False
    user.last_updated_by = current_user.username
    user.last_update_time = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
