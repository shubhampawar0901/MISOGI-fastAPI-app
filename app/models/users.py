from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, func
from sqlalchemy.orm import relationship
from app.database.base import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    phone_number = Column(String(15))
    balance = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    #Relationships
    transactions = relationship("Transactions", back_populates="user")