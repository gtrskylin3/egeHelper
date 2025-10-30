from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from .subjects import SubjectRead


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserScheme(UserBase):
    id: int

class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    subjects: list[SubjectRead] = []
