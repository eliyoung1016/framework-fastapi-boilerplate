from sqlalchemy import Integer, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel.sql.sqltypes import AutoString
from datetime import datetime, timezone
import enum
from .base import Base


class UserRole(str, enum.Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        AutoString, unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        AutoString, unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(AutoString, nullable=False)
    is_active: Mapped[bool | None] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool | None] = mapped_column(Boolean, default=False)
    roles: Mapped[UserRole | None] = mapped_column(
        SAEnum(UserRole), default=UserRole.USER
    )
    added_by: Mapped[str | None] = mapped_column(AutoString, nullable=True)
    time_added: Mapped[datetime | None] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    last_updated_by: Mapped[str | None] = mapped_column(AutoString, nullable=True)
    last_update_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
