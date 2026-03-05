from sqlalchemy.orm import mapped_column,Mapped
from src.database import Base
from sqlalchemy import (
    String,Boolean
)
from sqlalchemy.orm import  Mapped, mapped_column

class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255))