from sqlalchemy.orm import mapped_column,Mapped
from src.database import Base
from sqlalchemy import (
    String,Boolean
)
from sqlalchemy.orm import  Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)