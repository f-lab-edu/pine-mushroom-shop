from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    String,
    Integer,
    Text,
    DateTime,
    func,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.orders import OrderProduct


class Product(Base):
    __tablename__ = "product"

    __table_args__ = (
        UniqueConstraint(
            "product_name", "seller", "origin", name="uq_product_seller_origin"
        ),
    )

    product_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    product_name: Mapped[str] = mapped_column(String(100))
    seller: Mapped[str] = mapped_column(String(50))
    origin: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    product_status: Mapped[str] = mapped_column(String(50), nullable=False)
    product_price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None
    )
    order_product: Mapped[list["OrderProduct"]] = relationship(
        "OrderProduct", back_populates="product"
    )
