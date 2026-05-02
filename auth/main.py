from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session  
import models,Schema,utils
from auth_database import get_db,engine
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import  OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose.exceptions import JWTError
SECRET_KEY = "NJ69"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#HELPER FUNCTION THAT CREATES THE DATABASE TABLES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

app = FastAPI()

@app.post("/register/")
async def register(user: Schema.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = utils.hash_password(user.password)
    new_user = models.User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": f"User {new_user.username} created successfully."}


@app.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"} 

def get_current_user(
    token: str = Depends(oauth2_scheme),   # ✅ FIXED
    db: Session = Depends(get_db)
):
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

    user = db.query(models.User).filter(models.User.username == username).first()

    if user is None:
        raise credentials_exception

    return user
@app.get("/protected/")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you have access to this protected route!"}


def require_role(role: list[str]):
    def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role not in role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")
        return current_user
    return role_checker

@app.get("/profile/")
def profile(current_user: models.User = Depends(require_role(["user","admin"]))):
    return {"message": f"Hello {current_user.username}, this is your profile!"}

@app.get("/user/dashboard/")
def user_dashboard(current_user: models.User = Depends(require_role(["user"]))):
    return {"message": f"Welcome to the user dashboard, {current_user.username}!"}