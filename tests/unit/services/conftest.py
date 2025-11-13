import pytest

from src.db import Product
from src.models.product_schema import ProductCreate, ProductCategory, ProductStatus


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
def saved_product() -> Product:
    return Product(
        product_id=1,
        product_name="테스트 송이",
        seller="강원송이총판",
        origin="국내",
        category="선물용",
        product_price=1000,
        stock_quantity=10,
        description="test",
    )
