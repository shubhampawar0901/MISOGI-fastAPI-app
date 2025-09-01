"""
This is model file for Transactions table 
-- Transactions Table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    transaction_type VARCHAR(20) NOT NULL, -- 'CREDIT', 'DEBIT', 'TRANSFER_IN', 'TRANSFER_OUT'
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    reference_transaction_id INTEGER REFERENCES transactions(id), -- For linking transfer transactions
    recipient_user_id INTEGER REFERENCES users(id), -- For transfers
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database.base import Base

class Transactions(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_type = Column(String(20))
    amount = Column(DECIMAL(10, 2))
    description = Column(Text)
    # reference_transaction_id = Column(Integer, ForeignKey("transactions.id"))
    # recipient_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    #Relationships
    user = relationship("Users", back_populates="transactions")
    # reference_transaction = relationship("Transactions", foreign_keys=[reference_transaction_id], back_populates="transactions")