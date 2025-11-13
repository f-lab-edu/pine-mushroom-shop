import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product_schema import ProductCreate
from src.repositories.product_repository import ProductRepository


@pytest.mark.asyncio
async def test_create_product_success(sample_product: ProductCreate, db: AsyncSession):
    # given
    product_repository = ProductRepository(db)

    # when
    created_product = await product_repository.create_product(sample_product)

    # then
    assert created_product.product_id == 1
    assert created_product.product_name == sample_product.product_name
    assert created_product.stock_quantity == sample_product.stock_quantity
    # product_repository.assert_called_once_with()
