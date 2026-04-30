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

- `GET /api/v1/users` — list users
  - command: `curl -X GET http://127.0.0.1:8000/api/v1/users`
- `POST /api/v1/users` — create a new user
  - body: `{ "username": "admin", "full_name": "Admin User", "password": "securepassword" }`
  - command: `curl -X POST http://127.0.0.1:8000/api/v1/users -H 'Content-Type: application/json' -d '{"username":"admin","full_name":"Admin User","password":"securepassword"}'`
- `POST /api/v1/login` — login with `username` and `password`
  - body: `{ "username": "admin", "password": "securepassword" }`
  - command: `curl -X POST http://127.0.0.1:8000/api/v1/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"securepassword"}'`
- `GET /api/v1/users/{user_id}` — get user by ID
  - command: `curl -X GET http://127.0.0.1:8000/api/v1/users/1`
- `GET /api/v1/food-master` — list food master items
  - command: `curl -X GET http://127.0.0.1:8000/api/v1/food-master`
- `POST /api/v1/food-master` — add a food item
  - body: `{ "name": "Apple", "category": "Fruit", "qty_gram": 150.0, "calories": 95.0 }`
  - command: `curl -X POST http://127.0.0.1:8000/api/v1/food-master -H 'Content-Type: application/json' -d '{"name":"Apple","category":"Fruit","qty_gram":150.0,"calories":95.0}'`

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

If the `users` or `food_items` tables already exist, stamp the current schema instead of running the migration:

```bash
alembic stamp head
```

For a single migration covering all current DB models:

```bash
alembic revision --autogenerate -m "initial schemas"
alembic upgrade head
```

4. Start the server:

```bash
uvicorn main:app --reload
```

4. Open documentation at:

- http://127.0.0.1:8000/docs
