from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from enum import StrEnum


class ProductCategory(StrEnum):
    GIFT = "선물용"
    HOME = "가정용"
    FROZEN = "냉동"
    FRUIT = "과일"


class ProductStatus(StrEnum):
    ON_SALE = "판매중"
    SOLD_OUT = "품절"


class ProductCreate(BaseModel):
    product_name: str = Field(
        ..., min_length=0, max_length=100, description="상품 이름"
    )
    seller: str = Field(..., min_length=0, max_length=50, description="상품 판매처")
    origin: str = Field(..., min_length=0, max_length=50, description="상품 원산지")
    category: ProductCategory = Field(
        ...,
        description="상품 카테고리 (GIFT:선물용, HOME:가정용, FROZEN:냉동, FRUIT:과일",
    )
    product_status: ProductStatus = Field(
        ..., description="상품의 판매 상태 정보 (판매중, 품절)"
    )
    product_price: int = Field(..., ge=0, description="상품의 판매 가격")
    stock_quantity: int = Field(..., ge=0, description="상품의 남은 재고수량")
    description: str | None = Field(None, description="상품에 대한 상세 설명")


class ProductCreateResponse(BaseModel):
    product_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    product_id: int
    created_at: datetime
