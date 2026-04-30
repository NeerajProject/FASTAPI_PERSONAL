from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter()


@router.get("/users", response_model=List[UserRead])
def read_users(db: Session = Depends(get_db)) -> List[UserRead]:
    """Return all users.

    Route path: GET /api/v1/users
    Example command:
      curl -X GET http://127.0.0.1:8000/api/v1/users
    """
    service = UserService(UserRepository(db))
    return service.get_users()


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    
    """Create a new user.

    Route path: POST /api/v1/users
    Request body:
    {
      "username": "admin",
      "full_name": "Admin User",
      "password": "securepassword"
    }
    Example command:
      curl -X POST http://127.0.0.1:8000/api/v1/users \
        -H 'Content-Type: application/json' \
        -d '{"username":"admin","full_name":"Admin User","password":"securepassword"}'
    """
    service = UserService(UserRepository(db))
    if service.get_user_by_username(user_in.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return service.create_user(user_in)


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)) -> Token:
    """Authenticate a user and return a JWT token.

    Route path: POST /api/v1/login
    Request body:
    {
      "username": "admin",
      "password": "securepassword"
    }
    Example command:
      curl -X POST http://127.0.0.1:8000/api/v1/login \
        -H 'Content-Type: application/json' \
        -d '{"username":"admin","password":"securepassword"}'
    """
    service = UserService(UserRepository(db))
    user = service.authenticate_user(user_in.username, user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = service.create_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    """Get a single user by ID.

    Route path: GET /api/v1/users/{user_id}
    Example command:
      curl -X GET http://127.0.0.1:8000/api/v1/users/1
    """
    service = UserService(UserRepository(db))
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
