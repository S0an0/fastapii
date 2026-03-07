from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List, Optional
import secrets
import json

class Settings(BaseSettings):
    # JWT Settings (AuthX)
    JWT_SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Секретный ключ для JWT"
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="Алгоритм шифрования JWT"
    )
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Время жизни access токена в минутах"
    )
    JWT_ACCESS_COOKIE_NAME: str = Field(
        default="access_token",
        description="Имя cookie для хранения токена"
    )
    JWT_TOKEN_LOCATION: List[str] = Field(
        default=["cookies"],
        description="Где искать токен (cookies, headers)"
    )
    
    # Дополнительные настройки
    BCRYPT_ROUNDS: int = Field(default=12, description="Количество раундов для bcrypt")
    
    model_config = SettingsConfigDict(
        env_file=".env",  # .env в корне проекта, не в src/
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        # Специальная обработка для JWT_TOKEN_LOCATION (из .env строки в список)
        json_encoders={
            List[str]: lambda v: json.dumps(v)
        }
    )
    
    @classmethod
    def parse_env_var(cls, field_name: str, raw_val: str):
        """Парсинг переменных окружения"""
        if field_name == "JWT_TOKEN_LOCATION":
            # Преобразуем строку вида '["cookies"]' в список
            return json.loads(raw_val)
        return raw_val

# Создаем глобальный экземпляр настроек
settings = Settings()