from typing import List, Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: Optional[str] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    liked: int
    disliked: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserAuthenticate(UserBase):
    password: str


class User(UserBase):
    id: int
    items: List[Post] = []

    class Config:
        orm_mode = True


class AuthToken(BaseModel):
    access_token: str
