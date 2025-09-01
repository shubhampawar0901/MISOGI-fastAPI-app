from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserRead(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] | None = None
    balance: float | None = 0.00
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=255)
    phone_number: str | None = None
    #balance is default 0
    balance: float | None = 0.00
    
class UserResponse(BaseModel):
    id: Optional[int] = None
    username: Optional[str]
    email: Optional[str] = None
    phone_number: Optional[str] | None = None
    balance: float | None = 0.00
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str | None = None
    phone_number: str | None = None

    class Config:
        from_attributes = True

class UserDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True