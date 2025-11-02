from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subjects import Subject
from app.schemas.subjects import SubjectCreate, SubjectUpdate


class SubjectRepository:
    async def get(self, db: AsyncSession, subject_id: int, user_id: int) -> Subject | None:
        statement = select(Subject).where(Subject.id == subject_id, Subject.user_id == user_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int | None = 0, limit: int | None = 100
    ) -> list[Subject]:
        statement = (
            select(Subject).where(Subject.user_id == user_id).offset(skip).limit(limit)
        )
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

    async def update(
        self,
        db: AsyncSession,
        subject_in: SubjectUpdate,
        subject: Subject,
    ) -> Subject:
        if subject_in.name:
            subject.name = subject_in.name
        if subject_in.color:
            subject.color = subject_in.color
        await db.commit()
        await db.refresh(subject)
        return subject

    async def delete(
        self,
        db: AsyncSession,
        subject: Subject,
    ) -> bool:
        await db.delete(subject)
        await db.commit()
        return True


subject_repository = SubjectRepository()
