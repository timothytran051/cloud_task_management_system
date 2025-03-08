from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import session, declarative_base, sessionmaker
from fastapi import Depends
import os
from dotenv import load_dotenv 
from typing import AsyncGenerator
# DATABASE_URL = "postgresql+asyncpg://postgres:new_secure_password@localhost:5432/task_management"
# URL = (DATABASE_URL)
URL = os.getenv("DATABASE_URL")

engine = create_async_engine(URL, echo=True)

async_session = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

