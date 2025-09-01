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
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transactions import Transactions
from app.models.users import Users
from app.services.users import get_user_by_id, update_user
from app.services.transactions import create_transaction
from app.schemas.transactions import TransactionBase, TransactionRead, TransactionUpdate, TransactionDelete, TransactionCreate
from sqlalchemy import select

async def get_user_balance(user_id: int, db: AsyncSession):
    stmt = select(Users).where(Users.id == user_id)
    result = await db.execute(stmt)
    user = result.fetchone()
    if not user:
        return None
    return user.balance

async def add_money_to_wallet(user_id: int, amount: float, description: str, db: AsyncSession):
    user = await get_user_by_id(user_id, db)
    if not user:
        return None
    user.balance += amount
    await update_user(user_id, user, db)
    transaction = TransactionCreate(user_id=user_id, transaction_type="CREDIT", amount=amount, description=description)
    await create_transaction(transaction, db)
    return user.balance

async def withdraw_money_from_wallet(user_id: int, amount: float, description: str, db: AsyncSession):
    user = await get_user_by_id(user_id, db)
    if not user:
        return None
    if user.balance < amount:
        return None
    user.balance -= amount
    await update_user(user_id, user, db)
    transaction = TransactionCreate(user_id=user_id, transaction_type="DEBIT", amount=amount, description=description)
    await create_transaction(transaction, db)
    return user.balance