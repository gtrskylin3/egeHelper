from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.validation import get_current_active_user
from app.database.db import get_db
from app.schemas.tasks import TaskCreate, TaskRead, TaskUpdate, TaskFilter
from app.schemas.users import UserScheme
from app.services.tasks import task_service

sessionDep = Annotated[AsyncSession, Depends(get_db)]
userDep = Annotated[UserScheme, Depends(get_current_active_user)]
router = APIRouter(prefix="/api/tasks")

@router.post("/", response_model=TaskRead)
async def task_create(
    db: sessionDep,
    data: TaskCreate,
    user: userDep,
):
    return await task_service.create_task(db, task_in=data, user_id=user.id)

@router.get("/", response_model=list[TaskRead])
async def get_tasks(
    db: sessionDep,
    filters: TaskFilter,
    user: userDep,
):
    return await task_service.get_tasks_for_user_filtered(db, filters=filters, user_id=user.id)

@router.put('/{task_id}', response_model=TaskRead)
async def update_task(db: sessionDep, task_id: int, data: TaskUpdate,user: userDep):
    return await task_service.update_task(db, task_id, data, user_id=user.id)

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(db: sessionDep, task_id: int, user: userDep):
    await task_service.delete_task(db, task_id, user_id=user.id)
