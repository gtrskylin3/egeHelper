from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task
from app.schemas.tasks import TaskCreate


class TaskRepository:
    async def get(self, db: AsyncSession, task_id: int) -> Task | None:
        statement = select(Task).where(Task.id == task_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        statement = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, task_in: TaskCreate, user_id: int) -> Task:
        task_data = task_in.model_dump()
        db_task = Task(**task_data, user_id=user_id)
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task


task_repository = TaskRepository()
