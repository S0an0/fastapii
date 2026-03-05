from pydantic import BaseModel , Field , EmailStr
from typing import Optional



class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr


class UserCreate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    pass
    #id: int