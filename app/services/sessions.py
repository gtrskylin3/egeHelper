from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.sessions import StudySession
from app.repositories.sessions import session_repository
from app.repositories.subjects import subject_repository
from app.schemas.sessions import StudySessionCreate


class StudySessionService:
    async def create_session(
        self, db: AsyncSession, *, session_in: StudySessionCreate, user_id: int
    ) -> StudySession:
        """
        Создает учебную сессию.
        Если указан subject_id, проверяет, что он существует и принадлежит пользователю.
        """
        if session_in.subject_id:
            subject = await subject_repository.get(db, subject_id=session_in.subject_id)
            if not subject or subject.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid subject_id: {session_in.subject_id}",
                )

        return await session_repository.create(
            db, session_in=session_in, user_id=user_id
        )

    async def get_user_stats(self, db: AsyncSession, *, user_id: int) -> dict:
        """Собирает статистику по времени обучения для пользователя."""
        # Получаем все сессии и все предметы пользователя
        sessions = await session_repository.get_by_user(db, user_id=user_id, limit=10000)
        subjects = await subject_repository.get_by_user(db, user_id=user_id, limit=1000)
        subject_map = {subject.id: subject.name for subject in subjects}

        total_minutes = 0
        by_subject = defaultdict(int)

        for session in sessions:
            total_minutes += session.duration_minutes
            if session.subject_id:
                subject_name = subject_map.get(session.subject_id, "Unknown Subject")
                by_subject[subject_name] += session.duration_minutes
            else:
                by_subject["Without subject"] += session.duration_minutes

        return {
            "total_minutes": total_minutes,
            "by_subject": dict(by_subject), # Преобразуем в обычный dict для JSON
        }


session_service = StudySessionService()
