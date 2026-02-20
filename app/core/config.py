import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "framework-python Boilerplate"
    API_V1_STR: str = "/api/v1"
    
    # JWT Settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # Refresh Token
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30 * 6 # 6 months

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
