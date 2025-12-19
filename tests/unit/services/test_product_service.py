from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi_pagination.cursor import CursorParams, CursorPage

from src.db import Product
from src.models.product_schema import ProductCreate
from src.repositories.product_repository import ProductRepository
from src.services.product_service import ProductService


@pytest.mark.asyncio
async def test_create_product(sample_product: ProductCreate, saved_product: Product):
    # given
    mock_repository = AsyncMock(spec=ProductRepository)
    mock_repository.create_product = AsyncMock(return_value=saved_product)
    product_service = ProductService(product_repository=mock_repository)

    # when
    result = await product_service.create_product(sample_product)

    # then
    mock_repository.create_product.assert_called_once_with(sample_product)
    assert result == saved_product


@pytest.mark.asyncio
async def test_get_products(
    sample_cursor_params: CursorParams, sample_read_product: CursorPage[Product]
):
    # given
    mock_repository = AsyncMock(spec=ProductRepository)
    mock_repository.get_products = AsyncMock(return_value=sample_read_product)
    product_service = ProductService(product_repository=mock_repository)

    # when
    result = await product_service.get_products(sample_cursor_params)

    # then
    mock_repository.get_products.assert_called_once_with(sample_cursor_params)
    assert result == sample_read_product


@pytest.mark.asyncio
async def test_get_product_by_id_success(saved_product: Product):
    # given
    product_id = 1
    mock_repository = AsyncMock(spec=ProductRepository)
    mock_repository.get_product_by_id.return_value = saved_product
    product_service = ProductService(product_repository=mock_repository)

    # when
    product = await product_service.get_product_by_id(product_id)

    # then
    mock_repository.get_product_by_id.assert_called_once_with(product_id)
    assert product == saved_product


@pytest.mark.asyncio
async def test_update_product_by_id_success(sample_product: ProductCreate):
    # given
    product_id = 1
    saved_product = sample_product.model_dump()
    saved_product["product_id"] = product_id
    temp = saved_product.copy()
    update_data = {
        "product_id": product_id,
        "product_price": 9999,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    temp.update(update_data)

    mock_repository = AsyncMock(spec=ProductRepository)
    mock_repository.update_product.return_value = temp

    product_service = ProductService(mock_repository)

    # when
    result = await product_service.update_product_by_id(
        saved_product["product_id"], update_data
    )

    # then
    assert result.product_id == saved_product["product_id"]
    assert result.product_price == 9999
    assert result.product_price != saved_product["product_price"]
