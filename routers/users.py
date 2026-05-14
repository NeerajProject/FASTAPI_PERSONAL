from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse
from database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository
from jose import jwt
from jose.exceptions import JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)











SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    repo = UserRepository(db)
    user = await repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user




@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    repo = UserRepository(db)
    db_user = await repo.get_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    new_user_data = {"username": user.username, "password": hashed_password}
    
    # We can't use repo.create(new_user_data) directly because the BaseRepository 
    # might expect a different format or the model might have relationships.
    # But UserRepository extends BaseRepository[User].
    
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": f"User {new_user.username} created successfully."}


@router.post("/login")
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_async_db),
):
    repo = UserRepository(db)
    user = await repo.get_by_username(login_data.username)
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you have access!"}


@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, this is your profile!"}


@router.get("/dashboard")
def user_dashboard(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome to the dashboard, {current_user.username}!"}

@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    repo = UserRepository(db)
    return await repo.get_all()
