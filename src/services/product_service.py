from sqlalchemy.ext.asyncio import AsyncSession

from src.errors.exceptions import DatabaseConnectionError
from src.db.models.product import Product
from src.repositories.product_repository import ProductRepository
from src.models.product_schema import ProductCreate

from src.core.logging_config import logger


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_repository = ProductRepository(db)

    async def create_product(self, product_data: ProductCreate) -> Product | None:
        try:
            created_product = await self.product_repository.create_product(product_data)
        except DatabaseConnectionError:
            logger.warning(
                "데이터 베이스 연결 오류가 발생했습니다. 상품 등록을 재시도합니다."
            )
            created_product = await self.product_repository.create_product(product_data)

        return created_product
