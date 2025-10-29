from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subjects import Subject
from app.schemas.subjects import SubjectCreate


class SubjectRepository:
    async def get(self, db: AsyncSession, subject_id: int) -> Subject | None:
        statement = select(Subject).where(Subject.id == subject_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Subject]:
        statement = select(Subject).where(Subject.user_id == user_id).offset(skip).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())

    async def create(
        self, db: AsyncSession, *, subject_in: SubjectCreate, user_id: int
    ) -> Subject:
        subject_data = subject_in.model_dump()
        db_subject = Subject(**subject_data, user_id=user_id)
        db.add(db_subject)
        await db.commit()
        await db.refresh(db_subject)
        return db_subject


subject_repository = SubjectRepository()