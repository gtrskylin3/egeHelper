from app.models.tasks import Task
from app.schemas.tasks import TaskCreate, TaskUpdate
from .base import BaseRepository


class TaskRepository(BaseRepository[Task, TaskCreate, TaskUpdate]):
    pass

task_repository = TaskRepository(Task)

