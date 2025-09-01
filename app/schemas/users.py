from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str | None = None
    balance: float = 0.00
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)
    phone_number: str | None = None
    #balance is default 0
    balance: float = 0.00
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str | None = None
    balance: float = 0.00
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str | None = None
    phone_number: str | None = None

    class Config:
        orm_mode = True

class UserDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True