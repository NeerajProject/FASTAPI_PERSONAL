from typing import Generic, TypeVar, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: type[T]):
        self.db = db
        self.model = model

    async def create(self, obj_in: dict) -> T:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        result = await self.db.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, obj_id: int, obj_in: dict) -> Optional[T]:
        db_obj = await self.get_by_id(obj_id)
        if db_obj:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            await self.db.commit()
            await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, obj_id: int) -> bool:
        db_obj = await self.get_by_id(obj_id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True
        return False

    async def count(self) -> int:
        result = await self.db.execute(select(self.model))
        return len(result.scalars().all())
