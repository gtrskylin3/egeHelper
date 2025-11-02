from typing import Optional
from datetime import datetime
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date 

class StudySession(Base):
    __tablename__ = "studysession"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subject_id: Mapped[Optional[int]] = mapped_column(ForeignKey("subject.id"))
    started_at: Mapped[datetime]
    date: Mapped[date]
    duration_minutes: Mapped[int]
    note: Mapped[Optional[str]]

