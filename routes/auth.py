from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, Task
from database import get_db
from utils.auth import hash_password, verify_password, generate_token, verify_token
from pydantic import BaseModel, EmailStr
from schemas.schemas import UserCreate, UserLogin
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from typing import List

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
    login = await db.execute(select(User).where((User.username == user.username) | (User.email == user.email)))
    user_data = login.scalars().first()
    if not user_data:
        raise HTTPException(status_code = 400, detail = "Username or Email not found")
    verify = verify_password(user.password, user_data.hashed_password)
    
    if verify == False:
        raise HTTPException(status_code = 400, detail = "Incorrect Password")
    
    token = generate_token({"sub": user_data.id}, key)
    return {"access_token": token, "token_type": "bearer"}

oauth2 = OAuth2PasswordBearer(tokenurl="login")

def token_verification(token: str = Depends(oauth2)):
    load_dotenv()
    key = os.getenv("SECRET_KEY")
    verify = verify_token(token, key)
    if not verify:
        raise HTTPException(status_code=401, detail="Token verification failed")
    return verify
    
@router.get("/tasks/", response_model=List[Task])
async def get_tasks(user: dict = Depends(token_verification), db: AsyncSession = Depends(get_db)):
    query = select(Task).where(Task.user_id == user["sub"])
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks
    # db.execute("SELECT * FROM tasks WHERE user_id = {user.id}")
    
@router.post("/tasks/")
async def create_task(task: Task, user: dict = Depends(token_verification), db: AsyncSession = Depends(get_db)):
    temp = Task(
        title = task.title,
        description = task.description,
        completed = task.completed,
        user_id = user["sub"]
    )
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp
# def create_task(task: Task):
#     if not task.title.strip():
#         raise HTTPException(status_code=400, detail="Title cannot be blank")
#     tasks[task.id] = task
#     return list(task.values())