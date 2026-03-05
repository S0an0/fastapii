from pydantic import BaseModel , Field , EmailStr
from typing import Optional


class TaskUserBase(BaseModel):
    task_id: int
    user_id: int

class TaskUserCreate(TaskUserBase):
    pass

class TaskUserResponse(TaskUserBase):
    pass

class TaskUserUpdate(BaseModel):
    task_id: Optional[int] = None
    user_id: Optional[int] = None

class SetTask(BaseModel): 
    task_id: Optional[int] = None

class SetUser(BaseModel):
    user_id: Optional[int] = None