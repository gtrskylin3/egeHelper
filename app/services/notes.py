from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.notes import Note
from app.repositories.notes import note_repository
from app.repositories.subjects import subject_repository
from app.schemas.notes import NoteCreate


class NoteService:
    async def create_note(
        self, db: AsyncSession, *, note_in: NoteCreate, user_id: int
    ) -> Note:
        """
        Создает заметку.
        Если указан subject_id, проверяет, что он существует и принадлежит пользователю.
        """
        if note_in.subject_id:
            subject = await subject_repository.get(db, subject_id=note_in.subject_id)
            if not subject or subject.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid subject_id: {note_in.subject_id}",
                )

        return await note_repository.create(db, note_in=note_in, user_id=user_id)

    async def get_note(self, db: AsyncSession, *, note_id: int, user_id: int) -> Note:
        """Получает заметку по ID и проверяет владение."""
        note = await note_repository.get(db, note_id=note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )
        if note.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this note",
            )
        return note


note_service = NoteService()
