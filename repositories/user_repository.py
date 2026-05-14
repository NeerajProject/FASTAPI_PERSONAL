from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(self.model).where(self.model.username == username)
        )
        return result.scalar_one_or_none()

