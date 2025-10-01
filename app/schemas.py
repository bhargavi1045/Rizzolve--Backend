
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ComplaintCreate(BaseModel):
    category: Optional[str] = None
    description: str


class ComplaintOut(BaseModel):
    id: int
    user_id: int
    category: Optional[str]
    priority: str
    status: str
    description: str
    assigned_to: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class KBIngestIn(BaseModel):
    title: str
    content: str
    tags: Optional[str] = None


class AskIn(BaseModel):
    query: str


class AskOut(BaseModel):
    answer: str
    citations: List[str]
