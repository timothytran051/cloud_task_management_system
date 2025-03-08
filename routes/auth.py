from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from database import get_db
from utils.auth import hash_password
from pydantic import BaseModel, EmailStr
from schemas.schemas import UserCreate

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(User.username == user.username) | (User.email == user.email))
    # existing_email = await db.execute(select(User).where(User.email == user.email)) # SELECT * FROM users WHERE email = {user.email}
    if existing_user.scalars().first() or existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    return {"message": "User Registered"}
