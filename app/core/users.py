import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from app.database.db import get_user_db
from app.models.users import User


from sqlalchemy import select
from sqlalchemy.orm import selectinload


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def get(self, id: int, *, request: Optional[Request] = None) -> Optional[User]:
        # Переопределяем метод get, чтобы всегда жадно загружать subjects
        statement = select(User).options(selectinload(User.subjects)).where(User.id == id)
        result = await self.user_db.session.execute(statement)
        return result.scalar_one_or_none()


async def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    yield UserManager(user_db)
