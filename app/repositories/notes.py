from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.models.notes import Note
from app.schemas.notes import NoteCreate, NoteUpdate


class NoteRepository:
    async def get(self, db: AsyncSession, note_id: int, user_id: int) -> Note | None:
        statement = select(Note).where(Note.id == note_id, Note.user_id == user_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Note]:
        statement = select(Note).where(Note.user_id == user_id).offset(skip).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())
    
    async def get_by_user_and_date(
        self, db: AsyncSession, *, user_id: int, date: date,  skip: int | None = 0, limit: int | None= 100
    ) -> list[Note]:
        statement = select(Note).where(Note.user_id == user_id, Note.date == date).offset(skip).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, note_in: NoteCreate, user_id: int) -> Note:
        note_data = note_in.model_dump()
        db_note = Note(**note_data, user_id=user_id)
        db.add(db_note)
        await db.commit()
        await db.refresh(db_note)
        return db_note
    
    async def update(self, db: AsyncSession, *, note_to_update: NoteUpdate, note: Note) -> Note:
        if note_to_update.date:
            note.date = note_to_update.date
        if note_to_update.content:
            note.content = note_to_update.content
        await db.commit()
        await db.refresh(note)
        return note
    
    async def delete(self, db: AsyncSession, *, note: Note) -> bool:
        await db.delete(note)
        await db.commit()
        return True


note_repository = NoteRepository()
