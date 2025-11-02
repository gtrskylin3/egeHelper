from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from starlette.status import HTTP_403_FORBIDDEN

from app.models.subjects import Subject
from app.repositories.subjects import subject_repository
from app.schemas.subjects import SubjectCreate, SubjectUpdate


class SubjectService:
    async def get_subject(
        self, db: AsyncSession, *, subject_id: int, user_id: int
    ) -> Subject:
        """Получает предмет по ID и проверяет, что он принадлежит пользователю."""
        subject = await subject_repository.get(db, subject_id=subject_id, user_id=user_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"is not subject for user with id {user_id}",
            )
        return subject

    async def get_user_subjects(
        self, db: AsyncSession, *, user_id: int, skip: int | None, limit: int | None
    ) -> list[Subject]:
        """Получает список предметов для конкретного пользователя."""
        return await subject_repository.get_by_user(
            db, user_id=user_id, skip=skip, limit=limit
        )

    async def create_subject(
        self, db: AsyncSession, *, subject_in: SubjectCreate, user_id: int
    ) -> Subject:
        """Создает новый предмет для пользователя."""
        # Здесь можно добавить логику, например, проверку на дубликат имени
        return await subject_repository.create(
            db, subject_in=subject_in, user_id=user_id
        )
    async def update_subject(
        self, db: AsyncSession, subject_id: int, user_id: int, subject_in: SubjectUpdate
    ) -> Subject:
        """Обновляет  предмет для пользователя."""
        subject = await subject_repository.get(db, subject_id, user_id)
        if not subject:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You can't update this")
        updated = await subject_repository.update(
            db, subject_in=subject_in, subject=subject
        )
        if not updated: 
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Subject not found")
        return updated
        

    async def delete_subject(
        self, db: AsyncSession, *, subject_id: int, user_id: int
    ) -> bool:
        """Удаляет предмет для пользователя."""
        subject = await subject_repository.get(db, subject_id, user_id)
        if not subject:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"No have user subject with id {subject_id}")
        await subject_repository.delete(db, subject)
        return True


subject_service = SubjectService()
