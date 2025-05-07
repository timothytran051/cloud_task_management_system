from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from models import User, Task
from database import get_db
from utils.auth import hash_password, verify_password, generate_token, verify_token
from pydantic import BaseModel, EmailStr
from schemas.schemas import UserCreate, UserLogin
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from typing import List
import jwt
from fastapi.responses import JSONResponse, RedirectResponse
from urllib.parse import urlencode

router = APIRouter()
load_dotenv()
key = os.getenv("SECRET_KEY")
client_id = os.getenv("GOOGLE_CLIENT_ID")
redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    
@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where((User.username == user.username) | (User.email == user.email)))
    if existing_user.scalars().first():
        print("Duplicate user detected")
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
    secure = hash_password(user.password)
    new_user = User(username = user.username, email = user.email, hashed_password = secure)
    db.add(new_user)
    await db.commit()
    
    return {"message": "User Registered"}

@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    # print(f"username: {user.username}, email: {user.email}")
    login = await db.execute(select(User).where(or_(User.username == user.username, User.email == user.email)))
    user_data = login.scalars().first()
    # print(f"User: {user_data}")
    if not user_data:
        raise HTTPException(status_code = 400, detail = "Username or Email not found")
    verify = verify_password(user.password, user_data.hashed_password)
    
    if verify == False:
        raise HTTPException(status_code = 400, detail = "Incorrect Password")
    # print(f"user id: {user_data.id}")
    # print(f"SECRET_KEY: {key}")
    token = generate_token({"sub": user_data.id}, key)
    # print(f"Generated Token: {token}")
    return {"access_token": token, "token_type": "bearer"}

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

def token_verification(token: str = Depends(oauth2)):
    key = os.getenv("SECRET_KEY")
    # verify = verify_token(token, key)
    # print(f"first pass: {token}")
    # print(f"key: {key}")
    verify = None
    try:
        verify = verify_token(token, key)
    except Exception as e:
        print(f"Error decoding token: {e}")
    if not verify:
        raise HTTPException(status_code=401, detail="Token verification failed")
    return verify
    
# @router.get("/google-login")
# def google_login():
#     google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
#     params = {
#         "client_id" : client_id,
#         "response_type": "code",
#         "redirect_uri": redirect_uri,
#         "scope": "openid email profile",
#         "access_type": "offline",
#         "prompt": "conest"
#     }
#     url = f"{google_auth_url}?{urlencode(params)}"
#     return RedirectResponse(url)