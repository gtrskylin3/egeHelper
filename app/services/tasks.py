from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.tasks import Task
from app.repositories.tasks import task_repository
from app.repositories.subjects import subject_repository # Нужен для валидации
from app.schemas.tasks import TaskCreate


class TaskService:
    async def create_task(
        self, db: AsyncSession, *, task_in: TaskCreate, user_id: int
    ) -> Task:
        """
        Создает задачу. 
        Если указан subject_id, проверяет, что он существует и принадлежит пользователю.
        """
        if task_in.subject_id:
            subject = await subject_repository.get(db, subject_id=task_in.subject_id)
            if not subject or subject.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid subject_id: {task_in.subject_id}",
                )
        
        return await task_repository.create(db, task_in=task_in, user_id=user_id)

    async def get_task(self, db: AsyncSession, *, task_id: int, user_id: int) -> Task:
        """Получает задачу по ID и проверяет владение."""
        task = await task_repository.get(db, task_id=task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        if task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this task",
            )
        return task


task_service = TaskService()
