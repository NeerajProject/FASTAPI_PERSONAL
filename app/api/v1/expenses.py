from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

class Expense(BaseModel):
    id: int
    description: str
    amount: float

fake_expenses: List[Expense] = [
    Expense(id=1, description="Office supplies", amount=42.50),
    Expense(id=2, description="Travel reimbursement", amount=120.00),
]


@router.get("/expenses", response_model=List[Expense])
def get_expenses() -> List[Expense]:
    """Return the current list of expense items."""
    return fake_expenses


@router.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(expense: Expense) -> Expense:
    """Create a new expense item.

    Request body:
    {
      "id": 3,
      "description": "Stationery",
      "amount": 15.75
    }
    """
    if any(item.id == expense.id for item in fake_expenses):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expense ID already exists")
    fake_expenses.append(expense)
    return expense
