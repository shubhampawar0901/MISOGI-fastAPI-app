from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database.session import get_db
from app.schemas.transactions import TransactionCreate, TransactionRead, TransactionUpdate, TransactionDelete, TransactionBase, TransactionCreateTransfer, TransactionReadTransfer, TransactionUpdateTransfer, TransactionDeleteTransfer
from app.services.transfer import transfer_money, get_transfer_by_id, get_transfer_by_sender_id
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/transfer", tags=["Transfer"])

@router.post("/", response_model=TransactionReadTransfer, status_code=status.HTTP_201_CREATED, response_description="Transfer money")
async def transfer_money_route(transfer: TransactionCreateTransfer, db: AsyncSession = Depends(get_db)):
    transfer = await transfer_money(transfer.sender_user_id, transfer.recipient_user_id, transfer.amount, transfer.description, db)
    if not transfer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")
    return transfer

@router.get("/{transfer_id}", response_model=TransactionReadTransfer, status_code=status.HTTP_200_OK, response_description="Get transfer details")
async def get_transfer_details_route(transfer_id: int, db: AsyncSession = Depends(get_db)):
    transfer = await get_transfer_by_id(transfer_id, db)
    if not transfer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transfer not found")
    return transfer

@router.get("/{transfer_id}/details", response_model=TransactionReadTransfer, status_code=status.HTTP_200_OK, response_description="Get transfer details")
async def get_transfer_details_route(transfer_id: int, db: AsyncSession = Depends(get_db)):
    transfer = await get_transfer_by_id(transfer_id, db)
    if not transfer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transfer not found")
    return transfer

@router.get("/{sender_user_id}/transfers", response_model=list[TransactionReadTransfer], status_code=status.HTTP_200_OK, response_description="Get all transfers by sender")
async def get_all_transfers_by_sender_route(sender_user_id: int, db: AsyncSession = Depends(get_db)):
    transfers = await get_transfer_by_sender_id(sender_user_id, db)
    if not transfers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transfers found")
    return transfers
