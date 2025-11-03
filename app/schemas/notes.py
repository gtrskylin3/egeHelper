from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    date: date
    content: str


class NoteCreate(NoteBase):
    subject_id: Optional[int] = None

class NoteUpdate(BaseModel):
    date: date | None
    content: str | None = None

class NoteRead(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    subject_id: Optional[int] = None
