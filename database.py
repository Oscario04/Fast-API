from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Async database URL for FastAPI
DATABASE_URL = os.getenv("DATABASE_URL")
# Sync database URL for Alembic migrations
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")

# Async engine for FastAPI
async_engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Sync engine for Alembic migrations
sync_engine = create_engine(SYNC_DATABASE_URL)

Base = declarative_base()

async def get_session():
    async with SessionLocal() as session:
        yield session
