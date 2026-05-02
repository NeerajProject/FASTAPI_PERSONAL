from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.diet_repository import DietRepository
from schemas.diet import DietCreate, DietUpdate, DietResponse

router = APIRouter(prefix="/diets", tags=["diets"])


@router.post("/", response_model=DietResponse)
def create_diet(diet: DietCreate, db: Session = Depends(get_db)):
    repo = DietRepository(db)
    return repo.create(diet)


@router.get("/", response_model=list[DietResponse])
def get_all_diets(db: Session = Depends(get_db)):
    repo = DietRepository(db)
    return repo.get_all()


@router.get("/{diet_id}", response_model=DietResponse)
def get_diet(diet_id: int, db: Session = Depends(get_db)):
    repo = DietRepository(db)
    diet = repo.get(diet_id)
    if not diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    return diet


@router.put("/{diet_id}", response_model=DietResponse)
def update_diet(diet_id: int, diet: DietUpdate, db: Session = Depends(get_db)):
    repo = DietRepository(db)
    updated_diet = repo.update(diet_id, diet)
    if not updated_diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    return updated_diet


@router.delete("/{diet_id}")
def delete_diet(diet_id: int, db: Session = Depends(get_db)):
    repo = DietRepository(db)
    if not repo.delete(diet_id):
        raise HTTPException(status_code=404, detail="Diet not found")
    return {"message": "Diet deleted successfully"}
