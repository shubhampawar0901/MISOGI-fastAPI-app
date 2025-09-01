from app.database.base import SessionLocal
from app.models.users import Users
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserDelete

async def get_user_by_id(user_id: int, db: SessionLocal):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        return None
    return user

async def update_user(user_id: int, user: UserUpdate, db: SessionLocal):
    user = await get_user_by_id(user_id, db)

    if user.username != user.username:
        user.username = user.username
    if user.phone_number != user.phone_number:
        user.phone_number = user.phone_number
    db.commit()
    db.refresh(user)
    return user
    
