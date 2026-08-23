# simple 1 connection to postgres
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import settings

def test(url):
    return url

print(test(settings.DATABASE_URL))

#^ here i define the parameters for the connection pool
engine = create_async_engine(
    settings.DATABASE_URL,
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
    async with AsyncSessionLocal as session:
        yield session