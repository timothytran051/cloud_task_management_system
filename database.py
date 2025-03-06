from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import session, declarative_base, sessionmaker
from fastapi import Depends
import os
from dotenv import load_dotenv

URL = os.getenv("DATABASE_URL")

engine = create_async_engine(URL, echo=True)

async_session = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

