"""FastAPI application entrypoint.

Migration commands:
- Create a new migration:
  alembic revision --autogenerate -m "add new table"
- Apply migrations to the database:
  alembic upgrade head
- Revert the last migration:
  alembic downgrade -1
- Show current revision:
  alembic current

If the schema already exists and you just need to mark it as migrated:
  alembic stamp head
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


def create_app() -> FastAPI:
    # Use Alembic migrations to manage schema changes.
    # Base.metadata.create_all(bind=engine)
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix="/api/v1")
    return app


app = create_app()
