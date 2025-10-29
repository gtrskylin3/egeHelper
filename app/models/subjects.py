from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from app.models.users import User


class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    color: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    owner: Mapped[Optional["User"]] = relationship(back_populates="subjects")
