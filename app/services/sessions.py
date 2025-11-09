from collections import defaultdict
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import date 
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
        """
        if session_in.subject_id:
            subject = await subject_repository.get_by_id_and_user_id(db, id=session_in.subject_id, user_id=user_id)
            if not subject:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Subject with id {session_in.subject_id} not found for this user",
                )
        return await session_repository.create(
            db, obj_in=session_in, user_id=user_id
        )

    async def get_user_stats(self, db: AsyncSession, *, user_id: int, from_date: date | None, to_date: date | None, date: date | None) -> dict:
        """Собирает статистику по времени обучения для пользователя."""
        if from_date and to_date:
            sessions = await session_repository.get_by_user_from_date_to_date(db, user_id=user_id, from_date=from_date, to_date=to_date)
        elif date:
            sessions = await session_repository.get_by_user_and_date(db, user_id=user_id, date=date)
        else: 
            sessions = await session_repository.get_by_user(db, user_id=user_id)
            
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
            "by_subject": dict(by_subject),
        }
    
    async def get_user_subject_stats(self, db: AsyncSession, *, user_id: int, subject_id: int, date: date | None) -> dict:
        """Собирает статистику по времени обучения для пользователя по предмету."""
        if date:
            sessions = await session_repository.get_by_user_and_date(db, user_id=user_id, date=date)
        else:
            sessions = await session_repository.get_by_user(db, user_id=user_id)
        subject = await subject_repository.get_by_id_and_user_id(db, subject_id, user_id)
        if not subject:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Subject with this id not found for this user')
        total_minutes = 0
        for session in sessions:
            if session.subject_id == subject_id:
                total_minutes += session.duration_minutes
        return {
            'subject_id': subject_id, 
            'subject': subject.name,
            'total_minutes': total_minutes
            }

    async def get_sessions_for_user_by_date(self, db: AsyncSession, user_id: int, date: datetime.date):
        return await session_repository.get_by_user_and_date(db, user_id=user_id, date=date)

    async def delete_session(self, db: AsyncSession, *, user_id: int, session_id: int):
        db_obj = await session_repository.get_by_id_and_user_id(db, id=session_id, user_id=user_id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session with id {session_id} not found")
        await session_repository.delete(db, db_obj=db_obj)


session_service = StudySessionService()
