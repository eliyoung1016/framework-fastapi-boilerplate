import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def init_db(db: Session) -> None:
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        logger.info(f"Creating initial superuser: {settings.FIRST_SUPERUSER}")
        user = User(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER_USERNAME,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            roles=UserRole.SUPERADMIN,
            is_active=True,
            time_added=datetime.now(timezone.utc),
            added_by="system",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("Initial superuser created successfully.")
    else:
        logger.info("Initial superuser already exists.")


def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
