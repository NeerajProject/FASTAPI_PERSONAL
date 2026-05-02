# FastAPI Repository Pattern Implementation

This project implements the **Repository Pattern** with async/await support for clean, testable FastAPI applications. It includes dummy models (Product, Post) and a CLI tool for rapid scaffolding of new models.

## Architecture Overview

### Repository Pattern
The repository pattern provides an abstraction layer between your routes and the database:

```
Routes (FastAPI) 
    ↓
Repositories (Data Access Layer)
    ↓
Database (SQLAlchemy Models)
```

**Benefits:**
- ✅ Easy to test (repositories can be mocked)
- ✅ Decoupled business logic from database queries
- ✅ Reusable data access methods
- ✅ Simplified route handlers
- ✅ Type-safe with async support

### Project Structure

```
├── models/                      # SQLAlchemy ORM models
│   ├── user.py                 # User model with posts relationship
│   ├── product.py              # Dummy product model
│   └── post.py                 # Dummy post model with author FK
├── schemas/                     # Pydantic validation schemas
│   ├── user.py                 # User request/response schemas
│   ├── product.py              # Product schemas
│   └── post.py                 # Post schemas
├── repositories/                # Data access layer
│   ├── base.py                 # BaseRepository with async CRUD
│   ├── user_repository.py       # UserRepository
│   ├── product_repository.py    # ProductRepository
│   └── post_repository.py       # PostRepository
├── routers/                      # API route handlers
│   ├── users.py                # User routes (auth, CRUD)
│   ├── products.py             # Product routes (admin protected)
│   └── posts.py                # Post routes (author protected)
├── tests/                        # Pytest test suite
│   ├── conftest.py             # Fixtures for async testing
│   ├── test_*_repository.py     # Repository tests
│   └── test_*_routes.py         # Route endpoint tests
├── database.py                  # Database config (sync & async)
├── main.py                      # FastAPI app initialization
├── cli.py                       # CLI tool for scaffolding
└── requirement.txt              # Python dependencies
```

## Repository Pattern Usage

### Base Repository
All repositories extend `BaseRepository[T]` which provides async CRUD operations:

```python
class BaseRepository(Generic[T]):
    async def create(self, obj_in: dict) -> T
    async def get_by_id(self, obj_id: int) -> Optional[T]
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]
    async def update(self, obj_id: int, obj_in: dict) -> Optional[T]
    async def delete(self, obj_id: int) -> bool
    async def count(self) -> int
```

### Example: Using ProductRepository

**In Routes:**
```python
async def get_product_repository(db: AsyncSession = Depends(get_async_db)):
    return ProductRepository(db)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    repo: ProductRepository = Depends(get_product_repository),
):
    product = await repo.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Not found")
    return product
```

**In Tests:**
```python
@pytest.mark.asyncio
async def test_get_product(async_db: AsyncSession):
    repo = ProductRepository(async_db)
    product = await repo.create({"name": "Test", "price": 10.0})
    retrieved = await repo.get_by_id(product.id)
    assert retrieved.name == "Test"
```

### Custom Repositories
Extend `BaseRepository` to add custom methods:

```python
class PostRepository(BaseRepository[Post]):
    async def get_by_author(self, author_id: int):
        result = await self.db.execute(
            select(self.model).where(self.model.author_id == author_id)
        )
        return result.scalars().all()
```

## CLI Tool

The project includes a CLI tool for rapid development.

### Installation
```bash
pip install -r requirement.txt
```

### Available Commands

#### 1. Generate New Model
Creates model, schema, repository, routes, and tests:

```bash
python cli.py generate model <ModelName>
```

Example:
```bash
python cli.py generate model Article
```

This creates:
- `models/article.py` - SQLAlchemy model
- `schemas/article.py` - Pydantic schemas
- `repositories/article_repository.py` - Async repository
- `routers/articles.py` - REST endpoints
- `tests/test_article_repository.py` - Repository tests
- `tests/test_articles_routes.py` - Route tests

#### 2. Run Development Server
```bash
python cli.py dev
```

#### 3. Run Tests
```bash
python cli.py test
```

#### 4. Seed Database
```bash
python cli.py seed
```

## API Endpoints

### Users (Auth)
- `POST /users/register` - Create user account
- `POST /users/login` - Login and get JWT token
- `GET /users/protected` - Protected route (auth required)
- `GET /users/profile` - User profile (user/admin)
- `GET /users/dashboard` - Dashboard (user only)

### Products (Admin Protected)
- `GET /products` - List all products
- `GET /products/{id}` - Get product by ID
- `POST /products` - Create product (admin only)
- `PUT /products/{id}` - Update product (admin only)
- `DELETE /products/{id}` - Delete product (admin only)

### Posts (Author Protected)
- `GET /posts` - List all posts
- `GET /posts/{id}` - Get post by ID
- `POST /posts` - Create post (authenticated)
- `PUT /posts/{id}` - Update post (author or admin)
- `DELETE /posts/{id}` - Delete post (author or admin)

## Environment Configuration

Create a `.env` file based on `.env.example`:

```bash
# PostgreSQL
POSTGRES_USER=fastapi_db
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_db

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Testing

### Run All Tests
```bash
python cli.py test
```

### Run Specific Test
```bash
pytest tests/test_product_repository.py -v
```

### Run with Coverage
```bash
pytest --cov=. tests/
```

### Test Structure

Tests use:
- **conftest.py** - Fixtures for async DB, client, users, tokens
- **Async support** - `@pytest.mark.asyncio` decorator
- **In-memory DB** - SQLite for fast tests
- **Mock auth** - Pre-created test users and tokens

Example test:
```python
@pytest.mark.asyncio
async def test_create_product(async_db: AsyncSession):
    repo = ProductRepository(async_db)
    product = await repo.create({
        "name": "Test",
        "price": 29.99
    })
    assert product.id is not None
```

## Adding New Models

### Option 1: Use CLI (Recommended)
```bash
python cli.py generate model YourModel
```

Then update `main.py` to include the new router:
```python
from routers import users, products, posts, yourmodels

app.include_router(yourmodels.router)
```

### Option 2: Manual Steps
1. Create model in `models/yourmodel.py`
2. Create schema in `schemas/yourmodel.py`
3. Create repository in `repositories/yourmodel_repository.py`
4. Create routes in `routers/yourmodels.py`
5. Create tests in `tests/test_yourmodel_*.py`
6. Update `main.py` to include router

## Key Features

✅ **Async/Await** - Full async support with AsyncSession  
✅ **Type Safety** - Generic BaseRepository with type hints  
✅ **JWT Auth** - Secure token-based authentication  
✅ **Role-Based Access** - Admin/user role differentiation  
✅ **Repository Pattern** - Clean data access abstraction  
✅ **Pytest Integration** - Comprehensive async test suite  
✅ **CLI Scaffolding** - Generate models, repos, routes, tests  
✅ **Pydantic Validation** - Request/response validation  
✅ **FastAPI Docs** - Auto-generated Swagger UI at /docs  

## Performance Tips

1. **Use async database operations** - Always use `AsyncSession`
2. **Pagination** - Use skip/limit in list endpoints
3. **Connection pooling** - Configured in `database.py`
4. **Lazy loading** - SQLAlchemy relationships are lazy by default
5. **Caching** - Add caching layer for frequently accessed data

## Common Issues

### Import Errors
Ensure all modules are in Python path. Run from project root:
```bash
python cli.py dev
```

### Database Connection
Check `.env` file matches your PostgreSQL credentials:
```bash
psql -U fastapi_db -h localhost -d fastapi_db
```

### Test Failures
Use in-memory SQLite for tests (conftest.py handles this):
```bash
pytest -v --tb=short
```

## Next Steps

1. ✅ Review the repository pattern structure
2. ✅ Run tests: `python cli.py test`
3. ✅ Start dev server: `python cli.py dev`
4. ✅ Generate new model: `python cli.py generate model Article`
5. ✅ Visit http://localhost:8000/docs for API documentation

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
