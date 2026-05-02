import click
import os
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent


# Templates for scaffolding

MODEL_TEMPLATE = '''from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class {ModelName}(Base):
    __tablename__ = "{table_name}"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
'''

SCHEMA_CREATE_TEMPLATE = '''from pydantic import BaseModel
from datetime import datetime


class {ModelName}Create(BaseModel):
    name: str
    description: str


class {ModelName}Update(BaseModel):
    name: str | None = None
    description: str | None = None


class {ModelName}Response(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
'''

REPOSITORY_TEMPLATE = '''from sqlalchemy.ext.asyncio import AsyncSession
from models.{model_lower} import {ModelName}
from repositories.base import BaseRepository


class {ModelName}Repository(BaseRepository[{ModelName}]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, {ModelName})
'''

ROUTES_TEMPLATE = '''from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db
from repositories.{model_lower}_repository import {ModelName}Repository
from schemas.{model_lower} import {ModelName}Create, {ModelName}Update, {ModelName}Response
from routers.users import get_current_user
from models.user import User

router = APIRouter(
    prefix="/{model_lower}s",
    tags=["{model_lower}s"],
)


async def get_{model_lower}_repository(db: AsyncSession = Depends(get_async_db)):
    return {ModelName}Repository(db)


@router.get("", response_model=list[{ModelName}Response])
async def list_{model_lower}s(
    skip: int = 0,
    limit: int = 100,
    repo: {ModelName}Repository = Depends(get_{model_lower}_repository),
):
    return await repo.get_all(skip=skip, limit=limit)


@router.get("/{{id}}", response_model={ModelName}Response)
async def get_{model_lower}(
    id: int,
    repo: {ModelName}Repository = Depends(get_{model_lower}_repository),
):
    obj = await repo.get_by_id(id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{ModelName} not found",
        )
    return obj


@router.post("", response_model={ModelName}Response, status_code=status.HTTP_201_CREATED)
async def create_{model_lower}(
    obj: {ModelName}Create,
    current_user: User = Depends(get_current_user),
    repo: {ModelName}Repository = Depends(get_{model_lower}_repository),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create {model_lower}s",
        )
    return await repo.create(obj.dict())


@router.put("/{{id}}", response_model={ModelName}Response)
async def update_{model_lower}(
    id: int,
    obj_update: {ModelName}Update,
    current_user: User = Depends(get_current_user),
    repo: {ModelName}Repository = Depends(get_{model_lower}_repository),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update {model_lower}s",
        )
    update_data = {{k: v for k, v in obj_update.dict().items() if v is not None}}
    updated_obj = await repo.update(id, update_data)
    if not updated_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{ModelName} not found",
        )
    return updated_obj


@router.delete("/{{id}}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{model_lower}(
    id: int,
    current_user: User = Depends(get_current_user),
    repo: {ModelName}Repository = Depends(get_{model_lower}_repository),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete {model_lower}s",
        )
    deleted = await repo.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{ModelName} not found",
        )
'''

TEST_REPOSITORY_TEMPLATE = '''import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.{model_lower}_repository import {ModelName}Repository
from models.{model_lower} import {ModelName}


@pytest.mark.asyncio
async def test_create_{model_lower}(async_db: AsyncSession):
    repo = {ModelName}Repository(async_db)
    obj_data = {{"name": "Test {ModelName}", "description": "Test Description"}}
    obj = await repo.create(obj_data)
    assert obj.id is not None
    assert obj.name == "Test {ModelName}"


@pytest.mark.asyncio
async def test_get_{model_lower}_by_id(async_db: AsyncSession):
    repo = {ModelName}Repository(async_db)
    obj_data = {{"name": "Test {ModelName}", "description": "Test"}}
    created = await repo.create(obj_data)
    retrieved = await repo.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id


@pytest.mark.asyncio
async def test_get_all_{model_lower}s(async_db: AsyncSession):
    repo = {ModelName}Repository(async_db)
    objects = await repo.get_all()
    assert isinstance(objects, list)


@pytest.mark.asyncio
async def test_update_{model_lower}(async_db: AsyncSession):
    repo = {ModelName}Repository(async_db)
    obj_data = {{"name": "Original", "description": "Original Description"}}
    obj = await repo.create(obj_data)
    update_data = {{"name": "Updated"}}
    updated = await repo.update(obj.id, update_data)
    assert updated.name == "Updated"


@pytest.mark.asyncio
async def test_delete_{model_lower}(async_db: AsyncSession):
    repo = {ModelName}Repository(async_db)
    obj_data = {{"name": "To Delete", "description": "Will be deleted"}}
    obj = await repo.create(obj_data)
    deleted = await repo.delete(obj.id)
    assert deleted is True
'''

TEST_ROUTES_TEMPLATE = '''import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_list_{model_lower}s(async_client: AsyncClient):
    response = await async_client.get("/{model_lower}s")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_{model_lower}(async_client: AsyncClient, auth_token: str):
    response = await async_client.post(
        "/{model_lower}s",
        json={{"name": "Test", "description": "Test Description"}},
        headers={{"Authorization": f"Bearer {{auth_token}}"}}
    )
    assert response.status_code in [201, 403]  # 403 if not admin
'''


@click.group()
def cli():
    """FastAPI Scaffolding CLI Tool"""
    pass


@cli.group()
def generate():
    """Generate new models, repositories, routes, and tests"""
    pass


@generate.command()
@click.argument("model_name")
def model(model_name):
    """Generate model, repository, schema, and routes"""
    model_lower = model_name.lower()
    model_name = model_name.capitalize()

    click.echo(f"📦 Generating {model_name}...")

    files_created = []

    # Create model
    model_file = BASE_DIR / "models" / f"{model_lower}.py"
    model_content = MODEL_TEMPLATE.format(ModelName=model_name, table_name=f"{model_lower}s")
    model_file.write_text(model_content)
    files_created.append(str(model_file))
    click.echo(f"✅ Created {model_file}")

    # Create schema
    schema_file = BASE_DIR / "schemas" / f"{model_lower}.py"
    schema_content = SCHEMA_CREATE_TEMPLATE.format(ModelName=model_name)
    schema_file.write_text(schema_content)
    files_created.append(str(schema_file))
    click.echo(f"✅ Created {schema_file}")

    # Create repository
    repo_file = BASE_DIR / "repositories" / f"{model_lower}_repository.py"
    repo_content = REPOSITORY_TEMPLATE.format(
        ModelName=model_name,
        model_lower=model_lower
    )
    repo_file.write_text(repo_content)
    files_created.append(str(repo_file))
    click.echo(f"✅ Created {repo_file}")

    # Create routes
    routes_file = BASE_DIR / "routers" / f"{model_lower}s.py"
    routes_content = ROUTES_TEMPLATE.format(
        ModelName=model_name,
        model_lower=model_lower
    )
    routes_file.write_text(routes_content)
    files_created.append(str(routes_file))
    click.echo(f"✅ Created {routes_file}")

    # Create tests
    test_repo_file = BASE_DIR / "tests" / f"test_{model_lower}_repository.py"
    test_repo_content = TEST_REPOSITORY_TEMPLATE.format(
        ModelName=model_name,
        model_lower=model_lower
    )
    test_repo_file.write_text(test_repo_content)
    files_created.append(str(test_repo_file))
    click.echo(f"✅ Created {test_repo_file}")

    test_routes_file = BASE_DIR / "tests" / f"test_{model_lower}s_routes.py"
    test_routes_content = TEST_ROUTES_TEMPLATE.format(
        ModelName=model_name,
        model_lower=model_lower
    )
    test_routes_file.write_text(test_routes_content)
    files_created.append(str(test_routes_file))
    click.echo(f"✅ Created {test_routes_file}")

    click.echo(f"\n✨ Successfully generated {model_name} scaffold!")
    click.echo(f"📝 Files created: {len(files_created)}")
    click.echo("\n📋 Next steps:")
    click.echo("1. Update main.py to include the new router")
    click.echo(f"2. Add the model to models/__init__.py")
    click.echo("3. Run migrations or recreate database")
    click.echo("4. Run pytest to test the new routes")


@cli.command()
def seed():
    """Seed database with dummy data"""
    click.echo("🌱 Seeding database with dummy data...")
    click.echo("✅ Seed completed! (Implement actual seeding logic)")


@cli.command()
def test():
    """Run pytest"""
    click.echo("🧪 Running tests...")
    os.system("pytest -v")


@cli.command()
def dev():
    """Run development server"""
    click.echo("🚀 Starting development server...")
    os.system("uvicorn main:app --reload")


if __name__ == "__main__":
    cli()
