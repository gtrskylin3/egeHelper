from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudySessionBase(BaseModel):
    duration_minutes: int
    note: Optional[str] = None


class StudySessionCreate(StudySessionBase):
    subject_id: Optional[int] = None
    started_at: datetime
    date: date


class StudySessionRead(StudySessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    subject_id: Optional[int] = None
    started_at: datetime
    date: date
