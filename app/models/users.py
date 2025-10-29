from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from app.models.subjects import Subject


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc)
    )
    subjects: Mapped[list["Subject"]] = relationship(back_populates="owner")
