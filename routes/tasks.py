from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from models import Task
from database import get_db
from utils.auth import hash_password, verify_password, generate_token, verify_token
from pydantic import BaseModel, EmailStr
from schemas.schemas import TaskSchema, TaskCreate
import os
from dotenv import load_dotenv
from typing import List
from routes.auth import token_verification

router = APIRouter()
load_dotenv()
key = os.getenv("SECRET_KEY")

@router.get("/", response_model = List[TaskSchema])
async def get_tasks(user: dict = Depends(token_verification), db: AsyncSession = Depends(get_db)):
    # print("get tasks")
    query = select(Task).where(Task.user_id == int(user["sub"]))
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks
    
@router.post("/", response_model=TaskSchema)
async def create_task(task: TaskCreate, user: dict = Depends(token_verification), db: AsyncSession = Depends(get_db)):
    temp = Task(
        title = task.title,
        description = task.description,
        completed = task.completed,
        user_id = int(user["sub"])
    )
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp