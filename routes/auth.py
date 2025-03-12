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

router = APIRouter()
load_dotenv()
key = os.getenv("SECRET_KEY")

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
    
# @router.get("/tasks")
# async def get_tasks(user: dict = Depends(token_verification), db: AsyncSession = Depends(get_db)):
#     print("get tasks")
#     query = select(Task).where(Task.user_id == user["sub"])
#     result = await db.execute(query)
#     tasks = result.scalars().all()
#     return tasks
    
# @router.post("/tasks/")
# async def create_task(task: Task, user: dict = Depends(token_verification), db: AsyncSession = Depends(get_db)):
#     temp = Task(
#         title = task.title,
#         description = task.description,
#         completed = task.completed,
#         user_id = user["sub"]
#     )
#     db.add(temp)
#     await db.commit()
#     await db.refresh(temp)
#     return temp
# def create_task(task: Task):
#     if not task.title.strip():
#         raise HTTPException(status_code=400, detail="Title cannot be blank")
#     tasks[task.id] = task
#     return list(task.values())


