from sqlalchemy.orm import Session
from models.diet import Diet
from schemas.diet import DietCreate, DietUpdate


class DietRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, diet: DietCreate) -> Diet:
        db_diet = Diet(name=diet.name)
        self.db.add(db_diet)
        self.db.commit()
        self.db.refresh(db_diet)
        return db_diet

    def get(self, diet_id: int) -> Diet | None:
        return self.db.query(Diet).filter(Diet.id == diet_id).first()

    def get_all(self) -> list[Diet]:
        return self.db.query(Diet).all()

    def update(self, diet_id: int, diet: DietUpdate) -> Diet | None:
        db_diet = self.get(diet_id)
        if db_diet:
            if diet.name is not None:
                db_diet.name = diet.name
            self.db.commit()
            self.db.refresh(db_diet)
        return db_diet

    def delete(self, diet_id: int) -> bool:
        db_diet = self.get(diet_id)
        if db_diet:
            self.db.delete(db_diet)
            self.db.commit()
            return True
        return False
