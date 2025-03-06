from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from database import get_db
from utils.auth import hash_password
from pydantic import BaseModel, EmailStr

