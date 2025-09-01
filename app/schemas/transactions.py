from datetime import datetime
from pydantic import BaseModel, Field

"""
Transactions Model (SQLAlchemy)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_type = Column(String(20))
    amount = Column(DECIMAL(10, 2))
    description = Column(Text)
    reference_transaction_id = Column(Integer, ForeignKey("transactions.id"))
    recipient_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

APIs for which we may need to validate with pydantic schemas or conversion between pydantic->sqlalchemy and vice versa:
GET /users/{user_id}
Response: 200 OK
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "balance": 150.50,
  "created_at": "2024-01-01T00:00:00Z"
}

PUT /users/{user_id}
Request Body:
{
  "username": "string",
  "phone_number": "string"
}
Response: 200 OK

Wallet Endpoints
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

Transaction Endpoints
GET /transactions/{user_id}?page=1&limit=10
Response: 200 OK
{
  "transactions": [
    {
      "transaction_id": 123,
      "transaction_type": "CREDIT",
      "amount": 100.00,
      "description": "Added money",
      "created_at": "2024-01-01T12:30:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 10
}

GET /transactions/detail/{transaction_id}
Response: 200 OK
{
  "transaction_id": 123,
  "user_id": 1,
  "transaction_type": "TRANSFER_OUT",
  "amount": 25.00,
  "description": "Transfer to jane_doe",
  "recipient_user_id": 2,
  "reference_transaction_id": 124,
  "created_at": "2024-01-01T12:30:00Z"
}

POST /transactions
Request Body:
{
  "user_id": 1,
  "transaction_type": "CREDIT|DEBIT",
  "amount": 100.00,
  "description": "Manual transaction"
}
Response: 201 Created

"""

class TransactionBase(BaseModel):
    transaction_type: str = Field(..., min_length=1, max_length=20)
    amount: float = Field(..., gt=0, lt=1000000)
    description: str | None = None

class TransactionCreate(TransactionBase):
    user_id: int
    reference_transaction_id: int | None = None
    recipient_user_id: int | None = None

class TransactionRead(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TransactionUpdate(TransactionBase):
    pass

class TransactionDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True

