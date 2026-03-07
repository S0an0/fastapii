from sqlalchemy.orm import mapped_column,Mapped
from src.database import Base
from sqlalchemy import (
    String,Boolean
)
from sqlalchemy.orm import  Mapped, mapped_column
from src.core import pwd_context


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)


    def set_password(self, plain_password: str) -> None:
        """Хеширует и сохраняет пароль"""
        self.hashed_password = pwd_context.hash(plain_password)
    
    def verify_password(self, plain_password: str) -> bool:
        """Проверяет пароль"""
        return pwd_context.verify(plain_password, self.hashed_password)