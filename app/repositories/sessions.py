from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sessions import StudySession
from app.schemas.sessions import StudySessionCreate, StudySessionUpdate
from .base import BaseRepository


class StudySessionRepository(BaseRepository[StudySession, StudySessionCreate, StudySessionUpdate]):
    async def get_by_user_and_date(
        self, db: AsyncSession, *, user_id: int, date: date
    ) -> list[StudySession]:
        statement = (
            select(self.model).where(self.model.user_id == user_id, self.model.date == date)
        )
        result = await db.execute(statement)
        return list(result.scalars().all())


session_repository = StudySessionRepository(StudySession)
