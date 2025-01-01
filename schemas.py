from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PostBase(BaseModel):
    content: str
    picture: Optional[str] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    views: int = 0

    class Config:
        orm_mode = True
