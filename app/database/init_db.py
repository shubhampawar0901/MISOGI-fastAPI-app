# Database initialisation file
"""
session file is present in app/session.py 
"""
from app.database.session import engine
from app.models.users import Users
from app.models.transactions import Transactions

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Users.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
