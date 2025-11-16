from fastapi import Depends
from fastapi_pagination.cursor import CursorParams, CursorPage

from src.errors.exceptions import DatabaseConnectionError
from src.db.models.product import Product
from src.repositories.product_repository import ProductRepository
from src.models.product_schema import ProductCreate

from src.core.logging_config import logger


class ProductService:
    def __init__(
        self, product_repository: ProductRepository = Depends(ProductRepository)
    ):
        self.product_repository = product_repository

    async def create_product(self, product_data: ProductCreate) -> Product | None:
        try:
            created_product = await self.product_repository.create_product(product_data)
        except DatabaseConnectionError:
            logger.warning(
                "데이터 베이스 연결 오류가 발생했습니다. 상품 등록을 재시도합니다."
            )
            created_product = await self.product_repository.create_product(product_data)

        return created_product

    async def get_products(self, params: CursorParams) -> CursorPage[Product] | None:
        try:
            products = await self.product_repository.get_products(params)
        except DatabaseConnectionError:
            logger.warning(
                "데이터 베이스 연결 오류가 발생했습니다. 상품 조회를 재시도합니다."
            )
            products = await self.product_repository.get_products(params)

        return products

    async def get_product_by_id(self, product_id: int) -> Product | None:
        try:
            product = await self.product_repository.get_product_by_id(product_id)
        except DatabaseConnectionError:
            logger.warning(
                "데이터 베이스 연결 오류가 발생했습니다. 상품 조회를 재시도합니다."
            )
            product = await self.product_repository.get_product_by_id(product_id)

        return product
