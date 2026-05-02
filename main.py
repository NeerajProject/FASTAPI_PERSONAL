from fastapi import FastAPI
from database import init_db
from routers import users

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()  # create tables

app.include_router(users.router)