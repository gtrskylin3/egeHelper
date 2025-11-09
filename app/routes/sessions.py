from datetime import date
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.validation import (
    get_current_active_user
)
from app.schemas.sessions import StudySessionCreate, StudySessionRead
from app.schemas.users import UserScheme
from app.services.sessions import session_service
from app.database.db import get_db
from typing import Annotated

sessionDep = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter(prefix="/api/sessions")

@router.post('/', response_model=StudySessionRead)
async def create_session(
    db: sessionDep, 
    session_in: StudySessionCreate,
    user: UserScheme = Depends(get_current_active_user)
):
    return await session_service.create_session(db, session_in=session_in, user_id=user.id)

@router.get('/', response_model=list[StudySessionRead])
async def get_user_sessions(
    db: sessionDep,
    date: date = date.today(),
    user: UserScheme = Depends(get_current_active_user),
):
    return await session_service.get_sessions_for_user_by_date(db, user_id=user.id, date=date)

@router.delete('/{session_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: int,
    db: sessionDep,
    user: UserScheme = Depends(get_current_active_user)
):
    await session_service.delete_session(db, session_id=session_id, user_id=user.id)