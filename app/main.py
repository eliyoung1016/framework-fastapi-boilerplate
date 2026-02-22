import logging
import time
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from sqlalchemy import create_engine

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.db import DATABASE_URL
from app.initial_data import main as init_data_main

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Wait for DB readiness
    retries = 5
    while retries > 0:
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect():
                pass
            break
        except Exception:
            logger.warning(
                f"Waiting for database to be ready... {retries} retries left"
            )
            time.sleep(1)
            retries -= 1

    if retries == 0:
        logger.error("Database connection failed. Exiting.")
        raise Exception("Database connection failed.")

    # Run Alembic migrations
    logger.info("Running database migrations...")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Migrations completed.")

    # Initialize data
    logger.info("Initializing database data...")
    init_data_main()
    logger.info("Database initialization completed.")

    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def main():
    return {"message": "Hello World"}
