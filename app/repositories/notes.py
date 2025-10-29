from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notes import Note
from app.schemas.notes import NoteCreate


class NoteRepository:
    async def get(self, db: AsyncSession, note_id: int) -> Note | None:
        statement = select(Note).where(Note.id == note_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Note]:
        statement = select(Note).where(Note.user_id == user_id).offset(skip).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, note_in: NoteCreate, user_id: int) -> Note:
        note_data = note_in.model_dump()
        db_note = Note(**note_data, user_id=user_id)
        db.add(db_note)
        await db.commit()
        await db.refresh(db_note)
        return db_note


note_repository = NoteRepository()
