"""
POST /transfer
Request Body:
{
  "sender_user_id": 1,
  "recipient_user_id": 2,
  "amount": 25.00,
  "description": "Payment for dinner"
}
Response: 201 Created
{
  "transfer_id": "unique_transfer_id",
  "sender_transaction_id": 123,
  "recipient_transaction_id": 124,
  "amount": 25.00,
  "sender_new_balance": 125.50,
  "recipient_new_balance": 75.00,
  "status": "completed"
}

Response: 400 Bad Request
{
  "error": "Insufficient balance",
  "current_balance": 10.00,
  "required_amount": 25.00
}


"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transactions import Transactions
from app.models.users import Users
from app.services.users import get_user_by_id, update_user
from app.services.transactions import create_transaction
from app.schemas.transactions import TransactionBase, TransactionRead, TransactionUpdate, TransactionDelete, TransactionCreate
from sqlalchemy import select

async def transfer_money(sender_user_id: int, recipient_user_id: int, amount: float, description: str, db: AsyncSession):
    sender = await get_user_by_id(sender_user_id, db)
    if not sender:
        return None
    if sender.balance < amount:
        return None
    recipient = await get_user_by_id(recipient_user_id, db)
    if not recipient:
        return None
    sender.balance -= amount
    recipient.balance += amount
    await update_user(sender_user_id, sender, db)
    await update_user(recipient_user_id, recipient, db)
    sender_transaction = TransactionCreate(user_id=sender_user_id, transaction_type="TRANSFER_OUT", amount=amount, description=description, recipient_user_id=recipient_user_id)
    recipient_transaction = TransactionCreate(user_id=recipient_user_id, transaction_type="TRANSFER_IN", amount=amount, description=description, recipient_user_id=sender_user_id)
    sender_transaction = await create_transaction(sender_transaction, db)
    recipient_transaction = await create_transaction(recipient_transaction, db)
    return {
        "transfer_id": "unique_transfer_id",
        "sender_transaction_id": sender_transaction.id,
        "recipient_transaction_id": recipient_transaction.id,
        "amount": amount,
        "sender_new_balance": sender.balance,
        "recipient_new_balance": recipient.balance,
        "status": "completed"
    }

async def get_transfer_by_id(transfer_id: int, db: AsyncSession):
    stmt = select(Transactions).where(Transactions.id == transfer_id)
    result = await db.execute(stmt)
    transaction = result.fetchone()
    if not transaction:
        return None
    return transaction

async def get_transfer_by_sender_id(sender_user_id: int, db: AsyncSession):
    stmt = select(Transactions).where(Transactions.user_id == sender_user_id)
    result = await db.execute(stmt)
    transactions = result.fetchall()
    if not transactions:
        return None
    return transactions