# FastAPI Repository Pattern Example

This repository demonstrates a minimal FastAPI project structure using a repository/service pattern.

## Structure

- `app/main.py` - FastAPI application factory and router registration
- `app/api/v1/routers.py` - REST endpoints
- `app/core/config.py` - settings and configuration
- `app/db/session.py` - database session management
- `app/db/base.py` - SQLAlchemy base model
- `app/models/user.py` - SQLAlchemy `User` model
- `app/schemas/user.py` - Pydantic request/response schemas
- `app/repositories/user_repository.py` - repository for user persistence
- `app/services/user_service.py` - business logic service layer
- `app/core/security.py` - password hashing and JWT token generation
- `app/schemas/token.py` - token response schema

## Available endpoints

- `POST /api/v1/users` — create user with `username`, `full_name`, and `password`
- `POST /api/v1/login` — login with `username` and `password`
- `GET /api/v1/users` — list users
- `GET /api/v1/users/{user_id}` — get user by ID
- `GET /api/v1/expenses` — list expense items
- `POST /api/v1/expenses` — create a new expense item
  - body: `{ "id": 3, "description": "Stationery", "amount": 15.75 }`
- `GET /api/v1/food-master` — list food master items
- `POST /api/v1/food-master` — add a food item
  - body: `{ "name": "Apple", "category": "Fruit", "qty_gram": 150.0, "calories": 95.0 }`

## Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure PostgreSQL in a `.env` file or shell environment:

```bash
SQLALCHEMY_DATABASE_URI=postgresql+psycopg://postgres:password@localhost:5432/fastapi_db
```

3. Run Alembic migrations:

```bash
alembic upgrade head
```

If the `users` table already exists, stamp the current schema instead of running the migration:

```bash
alembic stamp head
```

4. Start the server:

```bash
uvicorn main:app --reload
```

4. Open documentation at:

- http://127.0.0.1:8000/docs
