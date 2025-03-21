from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.sql.expression import and_, update
from models import Task
from database import get_db
from utils.auth import hash_password, verify_password, generate_token, verify_token
from pydantic import BaseModel, EmailStr
from schemas.schemas import TaskSchema, TaskCreate, TaskUpdate
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
    new_task = Task(
        title = task.title,
        description = task.description,
        completed = task.completed,
        user_id = int(user["sub"])
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return(new_task)

@router.delete("/{task_id}")
async def delete_task(task_id: int, user: dict = Depends(token_verification), db: AsyncSession = Depends(get_db)):
    query = select(Task).where(and_(Task.id == task_id, Task.user_id == int(user["sub"])))
    result = await db.execute(query)
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task does not exist")
    if task.user_id != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Forbidden")
    await db.delete(task)
    await db.commit()
    return{"message": "Task Deleted Successfully"}

@router.patch("/{task_id}")
async def update_task(task_id: int, new_task: TaskUpdate, user: dict = Depends(token_verification), db: AsyncSession = Depends(get_db)):
    query = select(Task).where(and_(Task.id == task_id, Task.user_id == int(user["sub"])))
    result = await db.execute(query)
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task does not exist")
    if task.user_id != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Forbidden")
    if new_task.title is not None and not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be blank")
    
    if new_task.title:
        task.title = new_task.title
    if new_task.description:
        task.description = new_task.description
    if new_task.completed is not None:
        task.completed = new_task.completed
    
    await db.commit()
    await db.refresh(task)
    return{"message": "Task Updated Successfully", "updated_task": task}

#RESUME