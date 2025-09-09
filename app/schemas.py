from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Annotated

from app.database import Base


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
    email: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, 0 <= 1]  # value can either be 0 or 1
