from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transactions import Transactions
from app.models.users import Users
from app.services.users import get_user_by_id, update_user
from app.schemas.transactions import TransactionCreate, TransactionRead, TransactionUpdate, TransactionDelete
from sqlalchemy import select

async def create_transaction(transaction: TransactionCreate, db: AsyncSession):
    """
    if amount is credited or debited to wallet balance will be updated in users table as well
    """
    db_transaction = Transactions(**transaction.model_dump())

    if transaction.transaction_type == "CREDIT":
        user = await get_user_by_id(transaction.user_id, db)
        user.balance += transaction.amount
        await update_user(transaction.user_id, user, db)
    elif transaction.transaction_type == "DEBIT":
        user = await get_user_by_id(transaction.user_id, db)
        user.balance -= transaction.amount
        await update_user(transaction.user_id, user, db)

    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_user_transactions(user_id: int, page: int, limit: int, db: AsyncSession):
    stmt = select(Transactions).where(Transactions.user_id == user_id).offset((page - 1) * limit).limit(limit)
    result = await db.execute(stmt)
    transactions = result.fetchall()
    if not transactions:
        return None
    return transactions

async def get_transaction_by_id(transaction_id: int, db: AsyncSession):
    stmt = select(Transactions).where(Transactions.id == transaction_id)
    result = await db.execute(stmt)
    transaction = result.fetchone()
    if not transaction:
        return None
    return transaction

