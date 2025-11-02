import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import engine, database_manager
from src.main import app


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncClient:
    async with database_manager():
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport, base_url="http://127.0.0.1:8000"
        ) as client:
            yield client


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session
