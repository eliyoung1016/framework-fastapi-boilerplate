import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Prefer DATABASE_URL for Postgres/SQLModel compatibility
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
