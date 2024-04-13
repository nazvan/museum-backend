from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text, create_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

DATABASE_URI = "postgresql+asyncpg://postgres:postgres@localhost/museum_data"

engine = create_async_engine(DATABASE_URI, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
    

