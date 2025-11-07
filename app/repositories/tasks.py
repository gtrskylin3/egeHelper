from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task
from app.schemas.tasks import TaskCreate, TaskFilter, TaskUpdate

from .base import BaseRepository


class TaskRepository(BaseRepository[Task, TaskCreate, TaskUpdate]):
    async def get_by_user_filtered(
        self, db: AsyncSession, user_id: int, filter: TaskFilter
    ) -> list[Task]:
        stmt = select(Task).where(Task.user_id == user_id)
        if filter.due_date_to:
            stmt = stmt.where(Task.due_date <= filter.due_date_to)

        if filter.due_date_from:
            stmt = stmt.where(Task.due_date >= filter.due_date_from)

        if filter.status:
            stmt = stmt.where(Task.status == filter.status)
        
        if filter.subject_id:
            stmt = stmt.where(Task.subject_id == filter.subject_id)

        result = await db.scalars(stmt)
        return list(result.all())


task_repository = TaskRepository(Task)
