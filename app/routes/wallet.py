from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database.session import get_db
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserDelete
from app.services.users import get_user_by_id, update_user
from app.services.wallet import get_user_balance as get_balance_service, add_money_to_wallet as add_money_service, withdraw_money_from_wallet as withdraw_money_service
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

router = APIRouter(prefix="/wallet", tags=["Wallet"])

# Request schemas for wallet operations
class WalletOperationRequest(BaseModel):
    amount: float
    description: str

@router.get("/{user_id}/balance", response_model=float, status_code=status.HTTP_200_OK, response_description="Get user balance by user_id")
async def get_balance_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get user balance by user ID"""
    balance = await get_balance_service(user_id, db)
    if balance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return balance

@router.post("/{user_id}/add-money", response_model=float, status_code=status.HTTP_201_CREATED, response_description="Add money to wallet")
async def add_money_endpoint(user_id: int, request: WalletOperationRequest, db: AsyncSession = Depends(get_db)):
    """Add money to user's wallet"""
    balance = await add_money_service(user_id, request.amount, request.description, db)
    if balance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or operation failed")
    return balance

@router.post("/{user_id}/withdraw", response_model=float, status_code=status.HTTP_201_CREATED, response_description="Withdraw money from wallet")
async def withdraw_money_endpoint(user_id: int, request: WalletOperationRequest, db: AsyncSession = Depends(get_db)):
    """Withdraw money from user's wallet"""
    balance = await withdraw_money_service(user_id, request.amount, request.description, db)
    if balance is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found or insufficient balance")
    return balance

