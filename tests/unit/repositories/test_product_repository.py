from unittest.mock import AsyncMock, ANY, MagicMock, patch

import pytest
from fastapi_pagination.cursor import CursorParams, CursorPage

from src.db import Product
from src.models.product_schema import ProductCreate
from src.repositories.product_repository import ProductRepository


@pytest.mark.asyncio
async def test_create_product_success(sample_product: ProductCreate):
    # given
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_repository = ProductRepository(mock_db)

    # when
    created_product = await mock_repository.create_product(sample_product)

    # then
    mock_db.add.assert_called_once_with(ANY)
    product = mock_db.add.call_args.args[0]
    assert isinstance(product, Product)

    assert isinstance(created_product, Product)

    mock_db.commit.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_products_success(
    sample_cursor_params: CursorParams, sample_read_product: CursorPage[Product] | None
):
    # given
    mock_db = AsyncMock()
    mock_repository = ProductRepository(mock_db)

    with patch(
        "src.repositories.product_repository.paginate", new_callable=AsyncMock
    ) as mock_paginate:
        mock_paginate.return_value = sample_read_product

        # when
        products = await mock_repository.get_products(sample_cursor_params)

        # then
        mock_paginate.assert_called_once()
        call_args = mock_paginate.call_args
        assert call_args.args[0] == mock_db
        assert call_args.kwargs["params"] == sample_cursor_params

        assert products == sample_read_product


@pytest.mark.asyncio
async def test_get_product_by_id_success(saved_product: Product):
    # given
    product_id = 1
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = saved_product
    mock_db.execute.return_value = mock_result
    mock_repository = ProductRepository(mock_db)

    # when
    product = await mock_repository.get_product_by_id(product_id)

    # then
    mock_db.execute.assert_called_once()
    args, kwargs = mock_db.execute.call_args
    stmt = args[0]
    assert stmt is not None

    mock_result.scalar_one_or_none.assert_called_once_with()
    assert product == saved_product
