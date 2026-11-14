from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str=Field(min_length=3, max_length=50)
    password: str=Field(min_length=8)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    username: str=Field(min_length=3, max_length=50)
    created_at: datetime


class UserInDB(UserRead):
    hashed_password: str
