from pydantic import BaseModel , Field , EmailStr
from typing import Optional


class Task(BaseModel):
    id: int
    description: Optional[str] = None


class CreateTask(BaseModel):
    description: str = Field(..., min_length=1, description="Описание задачи")
    pass

class UpdateTask(BaseModel):
    description: Optional[str] = None
    pass

