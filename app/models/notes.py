from typing import Optional
from datetime import date
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Note(Base):
    __tablename__ = "note"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subject_id: Mapped[Optional[int]] = mapped_column(ForeignKey("subject.id"))
    date: Mapped[date]
    content: Mapped[str]