from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.subjects import Subject
from app.repositories.subjects import subject_repository
from app.schemas.subjects import SubjectCreate, SubjectUpdate


class SubjectService:
    async def get_subject(
        self, db: AsyncSession, *, subject_id: int, user_id: int
    ) -> Subject:
        """Получает предмет по ID и проверяет, что он принадлежит пользователю."""
        subject = await subject_repository.get_by_id_and_user_id(db, id=subject_id, user_id=user_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subject with id {subject_id} not found for this user",
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
        return await subject_repository.create(
            db, obj_in=subject_in, user_id=user_id
        )

    async def update_subject(
        self, db: AsyncSession, *, subject_id: int, user_id: int, subject_in: SubjectUpdate
    ) -> Subject:
        """Обновляет предмет для пользователя."""
        db_obj = await self.get_subject(db, subject_id=subject_id, user_id=user_id)
        return await subject_repository.update(
            db, db_obj=db_obj, obj_in=subject_in
        )

    async def delete_subject(
        self, db: AsyncSession, *, subject_id: int, user_id: int
    ):
        """Удаляет предмет для пользователя."""
        db_obj = await self.get_subject(db, subject_id=subject_id, user_id=user_id)
        await subject_repository.delete(db, db_obj=db_obj)


subject_service = SubjectService()
