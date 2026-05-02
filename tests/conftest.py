import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient

from database import Base, get_async_db
from main import app
from models.user import User
from repositories.user_repository import UserRepository
from routers.users import hash_password, create_access_token


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def async_db():
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with TestingSessionLocal() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def test_user(async_db: AsyncSession):
    user_repo = UserRepository(async_db)
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": hash_password("testpass123"),
        "role": "user",
    }
    user = await user_repo.create(user_data)
    return user


@pytest.fixture
async def admin_user(async_db: AsyncSession):
    user_repo = UserRepository(async_db)
    admin_data = {
        "username": "admin",
        "email": "admin@example.com",
        "password": hash_password("adminpass123"),
        "role": "admin",
    }
    admin = await user_repo.create(admin_data)
    return admin


@pytest.fixture
async def user_token(test_user: User):
    return create_access_token({"sub": test_user.username})


@pytest.fixture
async def admin_token(admin_user: User):
    return create_access_token({"sub": admin_user.username})


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
