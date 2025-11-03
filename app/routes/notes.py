from datetime import date
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.validation import (
    get_current_active_user
)
from app.schemas.notes import NoteCreate, NoteRead, NoteUpdate
from app.schemas.users import UserScheme
from app.services.notes import note_service
from app.database.db import get_db
from typing import Annotated

sessionDep = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter(prefix="/api/notes")

@router.post('/', response_model=NoteRead)
async def create_session(
    db: sessionDep, 
    note_in: NoteCreate,
    user: UserScheme = Depends(get_current_active_user)
):
    return await note_service.create_note(db, note_in=note_in, user_id=user.id)

@router.get('/', response_model=list[NoteRead])
async def get_user_notes(
    db: sessionDep,
    date: date,
    user: UserScheme = Depends(get_current_active_user),
):
    return await note_service.get_notes_for_user_by_date(db, user_id=user.id, date=date)


@router.delete('/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: sessionDep,
    user: UserScheme = Depends(get_current_active_user)
):
    await note_service.delete_note(db, note_id=note_id, user_id=user.id)

@router.delete('/{note_id}', response_model=NoteRead)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: sessionDep,
    user: UserScheme = Depends(get_current_active_user)
):
    await note_service.update_note(db, note_id=note_id, note_to_update=note_data, user_id=user.id)
    
