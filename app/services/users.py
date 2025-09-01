from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import Users
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserDelete
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import hashlib

def hash_password(password: str) -> str:
    """Hash a password using simple SHA256 (temporary solution)"""
    return hashlib.sha256(password.encode()).hexdigest()

async def get_user_by_id(user_id: int, db: AsyncSession) -> Optional[Users]:
    """Get user by ID, returns the user object directly"""
    stmt = select(Users).where(Users.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()  # This returns the actual user object or None
    return user

async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Users]:
    """Get all users with pagination"""
    stmt = select(Users).offset(skip).limit(limit)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return list(users)

async def get_user_by_email(email: str, db: AsyncSession) -> Optional[Users]:
    """Get user by email"""
    stmt = select(Users).where(Users.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return user

async def get_user_by_username(username: str, db: AsyncSession) -> Optional[Users]:
    """Get user by username"""
    stmt = select(Users).where(Users.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return user

async def create_user(user: UserCreate, db: AsyncSession) -> Optional[Users]:
    """Create a new user"""
    try:
        # Check if user with email or username already exists
        existing_user_email = await get_user_by_email(user.email, db)
        if existing_user_email:
            return None  # User with this email already exists

        existing_user_username = await get_user_by_username(user.username, db)
        if existing_user_username:
            return None  # User with this username already exists

        # Hash the password
        hashed_password = hash_password(user.password)

        # Create new user instance
        db_user = Users(
            username=user.username,
            email=user.email,
            password=hashed_password,
            phone_number=user.phone_number,
            balance=user.balance or 0.00
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    except IntegrityError:
        await db.rollback()
        return None

async def update_user(user_id: int, user: UserUpdate, db: AsyncSession) -> Optional[Users]:
    """Update user details"""
    user_data = await get_user_by_id(user_id, db)
    if not user_data:
        return None

    # Update only provided fields
    if user.username is not None:
        # Check if username is already taken by another user
        existing_user = await get_user_by_username(user.username, db)
        if existing_user and existing_user.id != user_id:
            return None  # Username already taken
        user_data.username = user.username

    if user.phone_number is not None:
        user_data.phone_number = user.phone_number

    try:
        await db.commit()
        await db.refresh(user_data)
        return user_data
    except IntegrityError:
        await db.rollback()
        return None

async def delete_user(user_id: int, db: AsyncSession) -> bool:
    """Delete a user by ID"""
    user = await get_user_by_id(user_id, db)
    if not user:
        return False

    try:
        await db.delete(user)
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        return False
