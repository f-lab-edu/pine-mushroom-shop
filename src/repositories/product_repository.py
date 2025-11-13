from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logging_config import logger
from src.errors.exceptions import (
    DatabaseError,
    ProductAlreadyExists,
    DatabaseConnectionError,
)
from src.db import Product
from src.models.product_schema import ProductCreate


class ProductRepository:
    def __init__(self, db: AsyncSession):
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
