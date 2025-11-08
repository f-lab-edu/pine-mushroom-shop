from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import DatabaseConnectionError, ProductAlreadyExists
from src.models import Product
from src.repositories.product_repository import ProductRepository
from src.schemas.product_schema import ProductCreate, ProductResponse

import logging

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_repository = ProductRepository(db)

    async def create_product(self, product_data: ProductCreate):
        product = Product(**product_data.model_dump())
        try:
            created_product = await self.product_repository.create_product(product)
            return ProductResponse(
                product_id=created_product.product_id,
                created_at=created_product.created_at,
            )

        except DatabaseConnectionError:
            logger.warning(
                "데이터 베이스 연결 오류가 발생했습니다. 상품 등록을 재시도합니다."
            )
            try:
                created_product = await self.product_repository.create_product(product)
                logger.info(
                    f"재시도 처리 결과 상품 등록 완료: 상품ID={created_product.product_id}"
                )
                return ProductResponse(
                    product_id=created_product.product_id,
                    created_at=created_product.created_at,
                )
            except DatabaseConnectionError as e:
                logger.error(f"데이터 베이스 연결 오류 발생: {str(e)}")
                raise e
            except Exception as e:
                logger.error(f"상품 등록 중 알 수 없는 오류 발생: {str(e)}")

        except ProductAlreadyExists as e:
            raise e

        except Exception as e:
            logger.error(f"상품 등록 중 알 수 없는 오류 발생: {str(e)}")
            raise e
