from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from .base import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.subjects import Subject


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subjects: Mapped[list["Subject"]] = relationship(back_populates="owner")
