from unittest.mock import AsyncMock, patch

import pytest

from src.db import Product
from src.models.product_schema import ProductCreate
from src.services.product_service import ProductService


@pytest.mark.asyncio
async def test_create_product(
    sample_product: ProductCreate, saved_product: Product, mock_db: AsyncMock
):
    # given
    product_service = ProductService(mock_db)

    # when
    with patch.object(
        product_service.product_repository,
        "create_product",
        new_callable=AsyncMock,
        return_value=saved_product,
    ) as mock_product_service_product_repository:
        result = await product_service.create_product(sample_product)

    # then
    assert result.product_id == saved_product.product_id
    mock_product_service_product_repository.assert_called_once_with(sample_product)
