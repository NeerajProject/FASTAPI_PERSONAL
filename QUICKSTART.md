# Quick Start Guide

## 1. Install Dependencies
```bash
pip install -r requirement.txt
```

## 2. Configure Environment
Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:
```
POSTGRES_USER=fastapi_db
POSTGRES_PASSWORD=123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_db
SECRET_KEY=your-secret-key-here
```

## 3. Setup Database
Make sure PostgreSQL is running, then create the database:
```bash
createdb -U fastapi_db fastapi_db
```

## 4. Start Development Server
```bash
python cli.py dev
```

Server will run at: http://localhost:8000

## 5. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 6. Test the API

### Register a User
```bash
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "role": "user"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

You'll get a response with `access_token`. Use this token for authenticated requests.

### Create a Product (Admin Only)
```bash
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer {your_access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 1299.99
  }'
```

### List Products
```bash
curl "http://localhost:8000/products"
```

### Create a Post
```bash
curl -X POST "http://localhost:8000/posts" \
  -H "Authorization: Bearer {your_access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is my first post content"
  }'
```

## 7. Run Tests
```bash
python cli.py test
```

Or run specific tests:
```bash
pytest tests/test_product_repository.py -v
```

## 8. Generate New Model
```bash
python cli.py generate model Article
```

This creates all necessary files:
- Model, Schema, Repository, Routes, and Tests

Then add to `main.py`:
```python
from routers import users, products, posts, articles
app.include_router(articles.router)
```

## 9. Explore the API

**Dummy Models Included:**
- **Products** - Simple inventory (GET, POST, PUT, DELETE)
- **Posts** - Blog posts linked to users (GET, POST, PUT, DELETE)

**Key Features:**
- JWT authentication
- Role-based access control (admin/user)
- Repository pattern for clean data access
- Full async support
- Comprehensive test suite
- Auto-generated API documentation

## Troubleshooting

### Issue: "No module named 'asyncpg'"
**Solution:** Install dependencies with `pip install -r requirement.txt`

### Issue: "Connection refused" on database
**Solution:** Make sure PostgreSQL is running:
```bash
# On macOS
brew services start postgresql

# On Linux
sudo systemctl start postgresql

# Verify connection
psql -U fastapi_db -h localhost -d fastapi_db
```

### Issue: Tests fail with "database locked"
**Solution:** Tests use in-memory SQLite by default. If you see errors, try:
```bash
rm -rf .pytest_cache
pytest --tb=short
```

## Architecture Overview

```
FastAPI Routes
    ↓
Repositories (Data Access Layer)
    ↓
SQLAlchemy Models
    ↓
PostgreSQL Database
```

The repository pattern ensures:
- ✅ Easy testing (mock repositories)
- ✅ Clean separation of concerns
- ✅ Reusable data access logic
- ✅ Type-safe operations

## Documentation

For detailed documentation, see:
- [REPOSITORY_PATTERN.md](./REPOSITORY_PATTERN.md) - Complete architecture guide
- [FastAPI Docs](http://localhost:8000/docs) - Auto-generated API docs
- [Swagger UI](http://localhost:8000/redoc) - Alternative docs view

## Next Steps

1. ✅ Run `python cli.py dev` to start server
2. ✅ Visit http://localhost:8000/docs to explore API
3. ✅ Create test users and try endpoints
4. ✅ Run `python cli.py generate model <Name>` to add new features
5. ✅ Read [REPOSITORY_PATTERN.md](./REPOSITORY_PATTERN.md) for deep dive

Happy coding! 🚀
