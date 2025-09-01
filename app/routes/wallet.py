from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database.session import get_db
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserDelete
from app.services.users import get_user_by_id, update_user
from app.services.wallet import get_user_balance, add_money_to_wallet, withdraw_money_from_wallet
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/wallet", tags=["Wallet"])

"""
GET /wallet/{user_id}/balance
Response: 200 OK
{
  "user_id": 1,
  "balance": 150.50,
  "last_updated": "2024-01-01T12:30:00Z"
}

POST /wallet/{user_id}/add-money
Request Body:
{
  "amount": 100.00,
  "description": "Added money to wallet"
}
Response: 201 Created
{
  "transaction_id": 123,
  "user_id": 1,
  "amount": 100.00,
  "new_balance": 250.50,
  "transaction_type": "CREDIT"
}

POST /wallet/{user_id}/withdraw
Request Body:
{
  "amount": 50.00,
  "description": "Withdrew money from wallet"
}
Response: 201 Created / 400 Bad Request (insufficient balance)

"""

@router.get("/{user_id}/balance", response_model=float, status_code=status.HTTP_200_OK, response_description="Get user balance by user_id")
async def get_user_balance(user_id: int, db: AsyncSession = Depends(get_db)):
    balance = await get_user_balance(user_id, db)
    if not balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return balance

@router.post("/{user_id}/add-money", response_model=float, status_code=status.HTTP_201_CREATED, response_description="Add money to wallet")
async def add_money_to_wallet(user_id: int, amount: float, description: str, db: AsyncSession = Depends(get_db)):
    balance = await add_money_to_wallet(user_id, amount, description, db)
    if not balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return balance

@router.post("/{user_id}/withdraw", response_model=float, status_code=status.HTTP_201_CREATED, response_description="Withdraw money from wallet")
async def withdraw_money_from_wallet(user_id: int, amount: float, description: str, db: AsyncSession = Depends(get_db)):
    balance = await withdraw_money_from_wallet(user_id, amount, description, db)
    if not balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return balance

