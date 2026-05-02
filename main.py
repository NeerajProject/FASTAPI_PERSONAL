from fastapi import FastAPI
from typing import Optional as Op
from pydantic import BaseModel
app = FastAPI()

@app.get("/")
async def root():    
    return {"message": "Hello "}

@app.get("/hello/{name}")
async def say_hello(name:str,age: Op[int] = None):    
    if age < 18:
        return {"message": f"Sorry {name}, you are not old enough to access this resource."}
    return {"message": f"Hello {name}!"}    

class Student(BaseModel):
    name: str   
    age: int
    roll: int

@app.post("/students/")
async def create_student(student: Student):
    
    return {"message": f"Student {student.name} created successfully with age {student.age} and roll number {student.roll}."}