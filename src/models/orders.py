from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String, DateTime, func, Boolean, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.member import Member
    from src.models.product import Product
    from src.models.payment import Payment
    from src.models.shipping import Shipping


class Orders(Base):
    __tablename__ = "orders"
    # Columns
    order_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    member_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("member.member_id"), nullable=False
    )
    order_status_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("order_status.order_status_id"), nullable=False
    )
    ordered_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
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
    # Relationship
    order_product: Mapped[list["OrderProduct"]] = relationship(
        "OrderProduct", back_populates="orders"
    )
    order_status: Mapped["OrderStatus"] = relationship(
        "OrderStatus", back_populates="orders"
    )
    member: Mapped["Member"] = relationship("Member", back_populates="orders")
    payment: Mapped["Payment"] = relationship("Payment", back_populates="orders")
    shipping: Mapped["Shipping"] = relationship("Shipping", back_populates="orders")


class OrderProduct(Base):
    __tablename__ = "order_product"
    # Columns
    order_product_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.order_id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("product.product_id"), nullable=False
    )
    order_product_price: Mapped[int] = mapped_column(Integer, nullable=False)
    order_product_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
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
    # Relationship
    order: Mapped["Orders"] = relationship("Orders", back_populates="order_product")
    product: Mapped["Product"] = relationship("Product", back_populates="order_product")


class OrderStatus(Base):
    __tablename__ = "order_status"
    # Columns
    order_status_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    order_status_category: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    # Relationship
    order: Mapped[list["Orders"]] = relationship(
        "Orders", back_populates="order_status"
    )
