from fastapi import Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.cursor import CursorParams, CursorPage
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from src.core.database import get_db
from src.core.logging_config import logger
from src.errors.exceptions import (
    DatabaseError,
    ProductAlreadyExists,
    DatabaseConnectionError,
)
from src.db import Product
from src.models.product_schema import ProductCreate, ProductStatus


class ProductRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.db.add(product)
        try:
            await self.db.commit()
            return product

        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"데이터베이스 제약 조건 위배: {str(e)}")
            raise ProductAlreadyExists(e) from e

        except DatabaseConnectionError as e:
            await self.db.rollback()
            logger.error(f"데이터베이스 연결 오류: {str(e)}")
            raise

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"SQLAlchemy 오류 발생: {str(e)}")
            raise DatabaseError(e) from e

    async def get_products(self, params: CursorParams) -> CursorPage[Product] | None:
        stmt = (
            select(Product)
            .where(Product.is_deleted.is_(False))
            .where(Product.product_status == ProductStatus.ON_SALE)
            .order_by(desc(Product.created_at), desc(Product.product_id))
        )
        try:
            products = await paginate(self.db, stmt, params=params)
        except DatabaseConnectionError as e:
            logger.error(f"데이터 베이스 연결 오류: {str(e)}")
            raise e

        return products

    async def get_product_by_id(self, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.product_id == product_id)
        try:
            product = await self.db.execute(stmt)
        except DatabaseConnectionError as e:
            logger.error(f"데이터 베이스 연결 오류: {str(e)}")
            raise e

        return product.scalar_one_or_none()
