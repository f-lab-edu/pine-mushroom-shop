import pytest
from fastapi_pagination.cursor import CursorParams, CursorPage

from src.db import Product


@pytest.fixture(scope="function")
def sample_cursor_params() -> CursorParams:
    return CursorParams()


@pytest.fixture(scope="function")
def sample_read_product() -> CursorPage[Product] | None:
    return {
        "items": [
            Product(
                product_id=11,
                product_name="강원도 자연산 뽕나무 상황 1kg",
                seller="강원송이총판",
                origin="국내",
                category="선물용",
                product_price=1200000,
                stock_quantity=10,
                description="string",
                created_at="2025-11-15T06=12:32.513800",
            )
        ],
        "total": 7,
        "current_page": "Pg%3D%3D",
        "current_page_backwards": "PA%3D%3D",
        "previous_page": "null",
        "next_page": "null",
    }
