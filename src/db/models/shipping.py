from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, String, DateTime, func, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db import Orders
from src.db.models.base import Base


class Shipping(Base):
    __tablename__ = "shipping"
    # Columns
    shipping_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.order_id"), nullable=False
    )
    shipping_status_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shipping_status.shipping_status_id"), nullable=False
    )
    shipping_address: Mapped[str] = mapped_column(String(100), nullable=False)
    tracking_number: Mapped[str] = mapped_column(String(50), nullable=False)
    shipped_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Relationship
    orders: Mapped["Orders"] = relationship("Orders", back_populates="shipping")
    shipping_status: Mapped["ShippingStatus"] = relationship(
        "ShippingStatus", back_populates="shipping"
    )


class ShippingStatus(Base):
    __tablename__ = "shipping_status"
    # Columns
    shipping_status_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    shipping_status_category: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    # Relationship
    shipping: Mapped["Shipping"] = relationship(
        "Shipping", back_populates="shipping_status"
    )
