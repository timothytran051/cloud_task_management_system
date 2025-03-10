from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from database import get_db
from utils.auth import hash_password, verify_password
from pydantic import BaseModel, EmailStr
from schemas.schemas import UserCreate, UserLogin

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where((User.username == user.username) | (User.email == user.email)))
    # existing_email = await db.execute(select(User).where(User.email == user.email)) # SELECT * FROM users WHERE email = {user.email}
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
    secure = hash_password(user.password)
    new_user = User(username = user.username, email = user.email, hashed_password = secure)
    db.add(new_user)
    await db.commit()
    
    return {"message": "User Registered"}

@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    login = await db.execute(select(User).where((User.username == user.username) | (User.email == user.email)))
    user_data = login.scalars().first()
    if not user_data:
        raise HTTPException(status_code = 400, detail = "Username or Email not found")
    verify = verify_password(user.password, user_data.hashed_password)
    
    if verify == False:
        raise HTTPException(status_code = 400, detail = "Incorrect Password")
    
    