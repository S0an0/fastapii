from pydantic import BaseModel , Field , EmailStr
from typing import Optional


class Task(BaseModel):
    description: Optional[str] = None


class CreateTask(Task):
    pass
    #description: str = Field(..., min_length=1, description="Описание задачи")
    

class UpdateTask(BaseModel):
    description: Optional[str] = None
    pass

