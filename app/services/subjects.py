from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.subjects import Subject
from app.repositories.subjects import subject_repository
from app.schemas.subjects import SubjectCreate


class SubjectService:
    async def get_subject(
        self, db: AsyncSession, *, subject_id: int, user_id: int
    ) -> Subject:
        """Получает предмет по ID и проверяет, что он принадлежит пользователю."""
        subject = await subject_repository.get(db, subject_id=subject_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )
        if subject.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this subject",
            )
        return subject

    async def get_user_subjects(
        self, db: AsyncSession, *, user_id: int, skip: int, limit: int
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


subject_service = SubjectService()
