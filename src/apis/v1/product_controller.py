from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_pagination.cursor import CursorParams, CursorPage

from src.core.logging_config import logger
from src.db import Product
from src.errors.exceptions import ProductAlreadyExists
from src.models.product_schema import (
    ProductCreate,
    ProductCreateResponse,
    ProductResponse,
)
from src.services.product_service import ProductService

router = APIRouter(prefix="/product", tags=["product"])


@router.post(
    "/", response_model=ProductCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_product(
    product: ProductCreate,
    product_service: ProductService = Depends(ProductService),
) -> ProductCreateResponse:
    try:
        created_product = await product_service.create_product(product)
    except ProductAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 상품입니다."
        )
    logger.info(f"상품 등록에 성공하였습니다. 상품ID: {created_product.product_id}")
    return ProductCreateResponse.model_validate(created_product)


@router.get(
    "/", response_model=CursorPage[ProductResponse], status_code=status.HTTP_200_OK
)
async def get_products(
    param: CursorParams = Depends(),
    product_service: ProductService = Depends(ProductService),
) -> CursorPage[Product]:
    products = await product_service.get_products(param)
    if products is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="죄송합니다. 현재 등록된 상품이 없습니다.",
        )

    return products


@router.get(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
async def get_product_by_id(
    product_id: int, product_service: ProductService = Depends(ProductService)
) -> ProductResponse:
    product = await product_service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="죄송합니다. 해당 상품을 찾을 수 없습니다.",
        )
    return ProductResponse.model_validate(product)
