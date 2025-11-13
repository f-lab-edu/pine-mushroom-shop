from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import pool

from src.core import config
from src.db import Base

async_engine = create_async_engine(
    url=config.db.url,
    echo=config.db.echo,
    poolclass=pool.StaticPool,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, autocommit=False, expire_on_commit=False
)


async def create_db_and_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def close_db() -> None:
    await async_engine.dispose()


@asynccontextmanager
async def database_manager() -> AsyncGenerator[None, None]:
    await create_db_and_tables()
    try:
        yield
    finally:
        await close_db()
