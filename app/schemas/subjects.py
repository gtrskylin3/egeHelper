from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubjectBase(BaseModel):
    name: str
    color: Optional[str] = None


class SubjectCreate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
