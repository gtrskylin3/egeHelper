from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from app.models.subjects import Subject


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password_hash: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(server_default='true', default=True)
    is_admin: Mapped[bool] = mapped_column(server_default='false', default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc)
    )
    subjects: Mapped[list["Subject"]] = relationship(back_populates="owner")
