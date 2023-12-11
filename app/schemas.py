from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class Post(BaseModel):
    id: int
    title: str
    description: str
    published: bool = False


class PostPatch(BaseModel):
    id: int = None
    title: str = None
    description: str = None
    published: bool = False


class User(BaseModel):
    email: EmailStr
    password: str


