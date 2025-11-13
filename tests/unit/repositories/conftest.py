# conftest.py
from typing import AsyncGenerator
from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy import (
    String,
    Integer,
    Text,
    DateTime,
    func,
    Boolean,
    UniqueConstraint,
)

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from src.models.product_schema import ProductCreate, ProductStatus, ProductCategory


class TestBase(DeclarativeBase):
    pass


class Product(TestBase):
    __tablename__ = "product"

    __table_args__ = (
        UniqueConstraint(
            "product_name", "seller", "origin", name="uq_product_seller_origin"
        ),
    )

    product_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    product_name: Mapped[str] = mapped_column(String(100))
    seller: Mapped[str] = mapped_column(String(50))
    origin: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    product_status: Mapped[str] = mapped_column(String(50), nullable=False)
    product_price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None
    )


@pytest_asyncio.fixture(scope="function")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


@pytest.fixture
def sample_product() -> ProductCreate:
    return ProductCreate(
        product_name="테스트 송이",
        seller="강원송이총판",
        origin="국내",
        category=ProductCategory.GIFT,
        product_status=ProductStatus.SOLD_OUT,
        product_price=1000,
        stock_quantity=10,
        description="test",
    )
