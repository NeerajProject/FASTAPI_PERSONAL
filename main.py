from fastapi import FastAPI
from database import engine, Base
from routers import users, diets

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI with Repository Pattern")

app.include_router(users.router)
app.include_router(diets.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
