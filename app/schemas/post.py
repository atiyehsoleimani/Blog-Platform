from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):

    title: str =Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=10000)

class PostUpdate(BaseModel):

    title: str | None =Field(default=None, min_length=1, max_length=200)
    body: str | None = Field(default=None, min_length=1, max_length=10000)

class PostRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str=Field(min_length=1, max_length=200)
    author_id: int
    body: str
    created_at: datetime
