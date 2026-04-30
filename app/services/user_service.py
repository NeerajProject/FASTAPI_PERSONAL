from datetime import timedelta
from typing import List, Optional

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_users(self) -> List[User]:
        return self.repository.get_all()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.repository.get_by_username(username)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.repository.get(user_id)

    def create_user(self, user_in: UserCreate) -> User:
        password_hash = get_password_hash(user_in.password)
        return self.repository.create(user_in, password_hash)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.repository.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    def create_token(self, user: User) -> str:
        expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(data={"sub": user.username}, expires_delta=expires)
