from sqlalchemy import Integer, String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from src.database import Base


class TaskUserAssociation(Base):
    __tablename__ = 'tasks_users'
    id = Column(Integer, primary_key=True)
    task_id =  Column(Integer(), ForeignKey("task.id"))
    user_id =  Column(Integer(), ForeignKey("user.id"))
