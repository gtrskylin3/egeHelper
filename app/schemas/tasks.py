from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: str = "todo"

class TaskFilter(BaseModel):
    due_date_from: Optional[date]
    due_date_to: Optional[date]
    status: Optional[str]
    subject_id: Optional[int]

class TaskCreate(TaskBase):
    subject_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    subject_id: Optional[int] = None
    created_at: datetime
