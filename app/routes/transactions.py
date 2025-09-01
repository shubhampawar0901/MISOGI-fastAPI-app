from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database.session import get_db
from app.schemas.transactions import TransactionCreate, TransactionRead, TransactionUpdate, TransactionDelete
from app.services.transactions import create_transaction, get_user_transactions, get_transaction_by_id
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED, response_description="Create transaction")
async def create_transaction_route(transaction: TransactionCreate, db: AsyncSession = Depends(get_db)):
    transaction = await create_transaction(transaction, db)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    return transaction

@router.get("/{user_id}", response_model=list[TransactionRead], status_code=status.HTTP_200_OK, response_description="Get user transactions")
async def get_user_transactions_route(user_id: int, page: int = 1, limit: int = 10, db: AsyncSession = Depends(get_db)):
    transactions = await get_user_transactions(user_id, page, limit, db)
    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    return transactions

@router.get("/detail/{transaction_id}", response_model=TransactionRead, status_code=status.HTTP_200_OK, response_description="Get transaction details")
async def get_transaction_details_route(transaction_id: int, db: AsyncSession = Depends(get_db)):
    transaction = await get_transaction_by_id(transaction_id, db)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction
