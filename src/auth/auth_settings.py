from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_COOKIE_NAME: str = "my_access_tokeen"
    JWT_TOKEN_LOCATION: str = "cookies"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = str(BASE_DIR / ".env"),

settings = Settings()