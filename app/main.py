from fastapi import FastAPI

from app.api.v1.routers import router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


def create_app() -> FastAPI:
    # Use Alembic migrations to manage schema changes.
    # Base.metadata.create_all(bind=engine)
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    app.include_router(router, prefix="/api/v1")
    return app


app = create_app()
