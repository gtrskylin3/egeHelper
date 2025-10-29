from typing import Optional
from datetime import datetime, date, timezone
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subject_id: Mapped[Optional[int]] = mapped_column(ForeignKey("subject.id"))
    title: Mapped[str]
    description: Mapped[Optional[str]]
    due_date: Mapped[Optional[date]]
    status: Mapped[str] = mapped_column(default="todo")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
