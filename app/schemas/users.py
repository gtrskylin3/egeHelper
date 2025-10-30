from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from .subjects import SubjectRead


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserScheme(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    is_admin: bool
    

class UserCreate(UserBase):
    password: str


class UserRead(UserScheme):
    created_at: datetime
    subjects: list[SubjectRead] = []
