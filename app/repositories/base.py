from typing import Type, TypeVar, Generic
from sqlalchemy import select
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base

ModelType = TypeVar('ModelType', bound=Base)
Create = TypeVar('Create', bound=BaseModel)
Update = TypeVar('Update', bound=BaseModel)

class BaseRepository(Generic[ModelType, Create, Update]):
    def __init__(self, model: Type[ModelType]):
       """
       Базовый репозиторий с CRUD операциями.
       :param model: SQLAlchemy модель
       """
       self.model = model
       
    async def get(self, db: AsyncSession, id: int) -> ModelType | None:
        statement = select(self.model).where(self.model.id == id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id_and_user_id(self, db: AsyncSession, id: int, user_id: int) -> ModelType | None:
        statement = select(self.model).where(self.model.id == id, self.model.user_id == user_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()
   
    async def create(
        self, db: AsyncSession, *, obj_in: Create, user_id: int
    ) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        obj_in: Update,
        db_obj: ModelType,
    ) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
        
    async def delete(
        self,
        db: AsyncSession,
        db_obj: ModelType,
    ) -> bool:
        await db.delete(db_obj)
        await db.commit()
        return True