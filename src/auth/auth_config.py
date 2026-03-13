from authx import AuthX, AuthXConfig
from src.auth.auth_settings import settings

config = AuthXConfig(
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
    JWT_ALGORITHM=settings.JWT_ALGORITHM,
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_ACCESS_COOKIE_NAME=settings.JWT_ACCESS_COOKIE_NAME,
    JWT_ACCESS_TOKEN_EXPIRES=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    JWT_COOKIE_CSRF_PROTECT=False,   # True в продакшне (требует CSRF-заголовок)
    JWT_COOKIE_SECURE=False,         # True в продакшне (только HTTPS)
)

auth = AuthX(config=config)