from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Repository Pattern"
    VERSION: str = "0.1.0"
    SQLALCHEMY_DATABASE_URI: str = "postgresql+psycopg://fastapi_db:password@localhost:5432/fastapi_db"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = {
        "env_file": ".env",
    }


settings = Settings()
