from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.tasks import Task
from app.repositories.tasks import task_repository
from app.repositories.subjects import subject_repository # Нужен для валидации
from app.schemas.tasks import TaskCreate, TaskFilter, TaskUpdate


class TaskService:
    async def create_task(
        self, db: AsyncSession, *, task_in: TaskCreate, user_id: int
    ) -> Task:
        """
        Создает задачу. 
        Если указан subject_id, проверяет, что он существует и принадлежит пользователю.
        """
        if task_in.subject_id:
            subject = await subject_repository.get_by_id_and_user_id(db, id=task_in.subject_id, user_id = user_id)
            if not subject:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail = f"Subject with id {task_in.subject_id} not found for this user",
                )
        
        return await task_repository.create(db, obj_in=task_in, user_id=user_id)

    async def get_task(self, db: AsyncSession, *, task_id: int, user_id: int) -> Task:
        """Получает задачу по ID и проверяет владение."""
        task = await task_repository.get_by_id_and_user_id(db, id=task_id, user_id=user_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found for this user"
            )
        return task
    
    async def update_task(self, db: AsyncSession, task_id: int, task_to_update: TaskUpdate, user_id: int) -> Task:
        task = await task_repository.get_by_id_and_user_id(db, id=task_id, user_id=user_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found for this user"
            )
        return await task_repository.update(db, obj_in=task_to_update, db_obj=task)
    
    async def delete_task(self, db: AsyncSession, task_id: int, user_id: int):
        task = await task_repository.get_by_id_and_user_id(db, id=task_id, user_id=user_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found for this user"
            )
        await task_repository.delete(db, db_obj=task)
    
    async def get_tasks_for_user_filtered(self, db:AsyncSession, user_id: int, filters:TaskFilter) -> list[Task]:
        filtered_tasks = await task_repository.get_by_user_filtered(db, user_id, filters)
        return filtered_tasks

task_service = TaskService()
