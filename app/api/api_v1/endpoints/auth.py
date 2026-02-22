from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.schemas.token import Token, TokenPayload
from app.utils.email import send_reset_password_email

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not user.is_active or user.is_deleted:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/login/refresh-token", response_model=Token)
def refresh_token(token: str, db: Session = Depends(deps.get_db)):
    """
    Refresh tokens.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if not token_data.refresh:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        if not token_data.sub:
            raise HTTPException(
                status_code=403, detail="Could not validate credentials"
            )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    user = db.query(User).filter(User.id == int(token_data.sub)).first()
    if not user or not user.is_active or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found or inactive")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/password-recovery/{email}")
def recover_password(email: str, db: Session = Depends(deps.get_db)):
    """
    Password Recovery.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found in system")

    password_reset_token = security.create_access_token(
        subject=email, expires_delta=timedelta(hours=1)
    )
    send_reset_password_email(
        email_to=user.email, email=user.email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


class ResetPasswordInput(BaseModel):
    token: str
    new_password: str


@router.post("/reset-password")
def reset_password(body: ResetPasswordInput, db: Session = Depends(deps.get_db)):
    """
    Reset password based on token.
    """
    try:
        payload = jwt.decode(
            body.token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not user.is_active or user.is_deleted:
        raise HTTPException(status_code=400, detail="Inactive user")

    hashed_password = security.get_password_hash(body.new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
