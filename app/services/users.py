from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import Users
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserDelete
from sqlalchemy import select

async def get_user_by_id(user_id: int, db: AsyncSession):
    stmt = select(Users).where(Users.id == user_id)
    result = await db.execute(stmt)
    user = result.fetchone()
    print(user)
    if not user:
        return None
    return user

async def update_user(user_id: int, user: UserUpdate, db: AsyncSession):
    user_data = await get_user_by_id(user_id, db)
    print(user_data)
    if user_data.username != user.username:
        user_data.username = user.username
    if user_data.phone_number != user.phone_number:
        user_data.phone_number = user.phone_number
    db.commit()
    db.refresh(user_data)
    return user_data
    
