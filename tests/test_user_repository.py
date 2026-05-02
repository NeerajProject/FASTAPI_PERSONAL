import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository
from routers.users import hash_password


@pytest.mark.asyncio
async def test_create_user(async_db: AsyncSession):
    repo = UserRepository(async_db)
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": hash_password("password123"),
        "role": "user",
    }
    user = await repo.create(user_data)
    assert user.id is not None
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"


@pytest.mark.asyncio
async def test_get_user_by_username(async_db: AsyncSession):
    repo = UserRepository(async_db)
    user_data = {
        "username": "findme",
        "email": "findme@example.com",
        "password": hash_password("password123"),
    }
    created = await repo.create(user_data)
    retrieved = await repo.get_by_username("findme")
    assert retrieved is not None
    assert retrieved.id == created.id


@pytest.mark.asyncio
async def test_get_user_by_email(async_db: AsyncSession):
    repo = UserRepository(async_db)
    user_data = {
        "username": "emailuser",
        "email": "email@example.com",
        "password": hash_password("password123"),
    }
    created = await repo.create(user_data)
    retrieved = await repo.get_by_email("email@example.com")
    assert retrieved is not None
    assert retrieved.id == created.id


@pytest.mark.asyncio
async def test_update_user(async_db: AsyncSession):
    repo = UserRepository(async_db)
    user_data = {
        "username": "updateme",
        "email": "updateme@example.com",
        "password": hash_password("password123"),
    }
    user = await repo.create(user_data)
    update_data = {"role": "admin"}
    updated = await repo.update(user.id, update_data)
    assert updated.role == "admin"


@pytest.mark.asyncio
async def test_delete_user(async_db: AsyncSession):
    repo = UserRepository(async_db)
    user_data = {
        "username": "deleteme",
        "email": "deleteme@example.com",
        "password": hash_password("password123"),
    }
    user = await repo.create(user_data)
    deleted = await repo.delete(user.id)
    assert deleted is True
    retrieved = await repo.get_by_id(user.id)
    assert retrieved is None
