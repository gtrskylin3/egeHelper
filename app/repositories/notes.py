from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.models.notes import Note
from app.schemas.notes import NoteCreate, NoteUpdate
from .base import BaseRepository


class NoteRepository(BaseRepository[Note, NoteCreate, NoteUpdate]):
    async def get_by_user_and_date(
        self, db: AsyncSession, *, user_id: int, date: date,  skip: int | None = 0, limit: int | None= 100
    ) -> list[Note]:
        statement = select(Note).where(Note.user_id == user_id, Note.date == date).offset(skip).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())


note_repository = NoteRepository(Note)
