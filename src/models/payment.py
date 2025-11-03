from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Integer,
    String,
    DateTime,
    func,
    Boolean,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.orders import Orders
    from src.models.member import Member


class Payment(Base):
    __tablename__ = "payment"
    # Columns
    payment_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.order_id"), nullable=False
    )
    member_coupon_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("member_coupon.member_coupon_id"), nullable=False
    )
    used_points: Mapped[int] = mapped_column(Integer, nullable=True)
    payment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(50), nullable=False)
    order_product_price: Mapped[int] = mapped_column(Integer, nullable=False)
    paid_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Relationship
    orders: Mapped["Orders"] = relationship("Orders", back_populates="payment")
    member: Mapped["Member"] = relationship("Member", back_populates="payment")
    payment_cancel: Mapped["PaymentCancel"] = relationship(
        "PaymentCancel", back_populates="payment"
    )


class PaymentCancel(Base):
    __tablename__ = "payment_cancel"
    # Columns
    payment_cancel_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    payment_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("payment.payment_id"), nullable=False
    )
    member_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("member.member_id"), nullable=False
    )
    requested_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_canceled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    cancel_reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Relationship
    payment: Mapped[list["Payment"]] = relationship(
        "Payment", back_populates="payment_cancel"
    )
    member: Mapped["Member"] = relationship("Member", back_populates="payment_cancel")


class PaymentStatus(Base):
    __tablename__ = "payment_status"
    # Columns
    payment_status_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    payment_status_category: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
