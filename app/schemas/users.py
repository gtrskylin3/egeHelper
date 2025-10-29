from fastapi_users.schemas import BaseUser, BaseUserCreate

from app.schemas.subjects import SubjectRead


class UserRead(BaseUser[int]):
    # Добавляем кастомное поле, которое будет в ответе API
    subjects: list[SubjectRead] = []


class UserCreate(BaseUserCreate):
    pass