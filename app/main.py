from fastapi import FastAPI, Depends, HTTPException, status, Request
from app.routes.users import router as users_router

app = FastAPI(
    title="Digital Wallet",
    description="A digital wallet for users to store and manage their money",
    version="0.0.1",
)

app.include_router(users_router)

#Health API
@app.get("/health", tags=["Health"])
async def health():
    return {"status": "OK"}