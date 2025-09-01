from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database.base import SessionLocal
from app.database.session import get_db
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserDelete
from app.services.users import get_user_by_id, update_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK, response_description="Get user details by user_id")
async def get_user_by_id(user_id: int, db: SessionLocal = Depends(get_db)):
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Update user with PUT /users/{user_id}
@router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK, response_description="Update user details")
async def update_user(user_id: int, user: UserUpdate, db: SessionLocal = Depends(get_db)):
    user = await update_user(user_id, user, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user