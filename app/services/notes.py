from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import date
from app.models.notes import Note
from app.repositories.notes import note_repository
from app.repositories.subjects import subject_repository
from app.schemas.notes import NoteCreate, NoteUpdate


class NoteService:
    async def create_note(
        self, db: AsyncSession, *, note_in: NoteCreate, user_id: int
    ) -> Note:
        """
        Создает заметку.
        Если указан subject_id, проверяет, что он существует и принадлежит пользователю.
        """
        if note_in.subject_id:
            subject = await subject_repository.get(db, subject_id=note_in.subject_id, user_id=user_id)
            if not subject:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid subject_id: {note_in.subject_id}",
                )

        return await note_repository.create(db, note_in=note_in, user_id=user_id)

    async def get_note(self, db: AsyncSession, *, note_id: int, user_id: int) -> Note:
        """Получает заметку по ID и проверяет владение."""
        note = await note_repository.get(db, note_id=note_id, user_id=user_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Note not with id {note_id} not found for user with id {user_id}"
            )
        return note
    
    async def update_note(
        self, db: AsyncSession, note_id: int, user_id: int, note_to_update: NoteUpdate
    ) -> Note:
        """Обновляет  предмет для пользователя."""
        note = await note_repository.get(db, note_id, user_id)
        if not note:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You can't update this")
        updated = await note_repository.update(
            db, note_to_update=note_to_update, note=note
        )
        if not updated: 
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Note not found")
        return updated
        

    async def delete_note(
        self, db: AsyncSession, *, note_id: int, user_id: int
    ) -> bool:
        """Удаляет предмет для пользователя."""
        note = await note_repository.get(db, note_id, user_id)
        if not note:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"No have user note with id {note_id}")
        await note_repository.delete(db, note=note)
        return True
    
    async def get_notes_for_user_by_date(self, db: AsyncSession, user_id: int, date: date):
        return await note_repository.get_by_user_and_date(db, user_id=user_id, date=date)

note_service = NoteService()
