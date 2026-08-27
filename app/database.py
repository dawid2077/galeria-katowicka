#database.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import settings
#! make sure to not use this function in prod
def test(url):
    return url

#print(test(settings.DATABASE_URL))

#* this so we have a connection pool and session we can pass to endpoints
engine = create_async_engine(
    settings.DATABASE_URL,
    #! set to True for raw sql info
    #echo=True,
    pool_size=2,
    max_overflow=3,
    pool_timeout=10,
    pool_pre_ping=True
)

AsyncSessionLocal =async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session