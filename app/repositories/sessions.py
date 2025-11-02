from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sessions import StudySession
from app.schemas.sessions import StudySessionCreate


class StudySessionRepository:
    async def get(self, db: AsyncSession, session_id: int, user_id: int) -> StudySession | None:
        statement = select(StudySession).where(StudySession.id == session_id, StudySession.user_id == user_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[StudySession]:
        statement = (
            select(StudySession).where(StudySession.user_id == user_id).offset(skip).limit(limit)
        )
        result = await db.execute(statement)
        return list(result.scalars().all())
    
    async def get_by_user_and_date(
        self, db: AsyncSession, *, user_id: int, date: date
    ) -> list[StudySession]:
        statement = (
            select(StudySession).where(StudySession.user_id == user_id, StudySession.date == date)
        )
        result = await db.execute(statement)
        # print(date, list(result.scalars().all()))
        return list(result.scalars().all())

    async def create(
        self, db: AsyncSession, *, session_in: StudySessionCreate, user_id: int
    ) -> StudySession:
        session_data = session_in.model_dump()
        session = StudySession(**session_data, user_id=user_id)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session
    
    async def delete(
        self, db: AsyncSession, *, session: StudySession
    ) -> bool:
        await db.delete(session)
        await db.commit()
        return True

session_repository = StudySessionRepository()
