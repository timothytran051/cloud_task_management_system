from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import session, declarative_base
import os
from dotenv import load_dotenv

URL = os.getenv("DATABASE_URL")