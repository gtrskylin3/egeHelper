from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.validation import (
    get_current_active_user
)
from app.schemas.subjects import SubjectRead, SubjectCreate, SubjectUpdate
from app.schemas.users import UserScheme
from app.services.subjects import subject_service
from app.database.db import get_db
from typing import Annotated

sessionDep = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter(prefix="/api/subjects")

@router.post('/', response_model= SubjectRead)
async def create_subject(
    db: sessionDep, 
    subject_in: SubjectCreate,
    user: UserScheme = Depends(get_current_active_user)
):
    return await subject_service.create_subject(db, subject_in=subject_in, user_id=user.id)

@router.get('/', response_model=list[SubjectRead])
async def get_user_subjects(
    db: sessionDep,
    skip: int | None = None, 
    limit: int | None = None,
    user: UserScheme = Depends(get_current_active_user),
):
    return await subject_service.get_user_subjects(db, user_id=user.id, limit=limit, skip=skip)

@router.put('/{subject_id}', response_model=SubjectRead)
async def update_subject(
    subject_id: int,
    db: sessionDep,
    subject_update: SubjectUpdate,
    user: UserScheme = Depends(get_current_active_user)
):
    return await subject_service.update_subject(db, subject_id=subject_id, user_id=user.id, subject_in=subject_update)

@router.delete('/{subject_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(
    subject_id: int,
    db: sessionDep,
    user: UserScheme = Depends(get_current_active_user)
):
    await subject_service.delete_subject(db, subject_id=subject_id, user_id=user.id)