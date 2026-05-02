from pydantic import BaseModel,EmailStr



# Define Pydantic models for user registration and login
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"  # Default role is "user"

# Define a Pydantic model for user login
class UserLogin(BaseModel): 
    username: str
    password: str