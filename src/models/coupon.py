from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.member import Member


class Coupon(Base):
    __tablename__ = "coupon"
    # Columns
    coupon_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    coupon_name: Mapped[str] = mapped_column(String(50), unique=True)
    discount_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    # Relationship
    member_coupon: Mapped[list["MemberCoupon"]] = relationship(
        "MemberCoupon", back_populates="coupon"
    )


class MemberCoupon(Base):
    __tablename__ = "member_coupon"
    # Columns
    member_coupon_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    member_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("member.member_id"), nullable=False
    )
    coupon_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("coupon.coupon_id"), nullable=False
    )
    member_coupon_status_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("member_coupon_status.member_coupon_status_id"),
        nullable=False,
    )
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    # Relationship
    member: Mapped["Member"] = relationship("Member", back_populates="member_coupon")
    coupon: Mapped["Coupon"] = relationship("Coupon", back_populates="member")
    member_coupon_status: Mapped["MemberCouponStatus"] = relationship(
        "MemberCouponStatus", back_populates="member_coupon"
    )


class MemberCouponStatus(Base):
    __tablename__ = "member_coupon_status"
    # columns
    member_coupon_status_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    # Relationship
    member_coupon: Mapped["MemberCoupon"] = relationship(
        "MemberCoupon", back_populates="member_coupon_status"
    )


class MemberCouponHistory(Base):
    __tablename__ = "member_coupon_history"
    # Columns
    member_coupon_history_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    member_coupon_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("member_coupon.member_coupon_id"), nullable=False
    )
    previous_coupon_status: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    current_coupon_status: Mapped[str] = mapped_column(String(50), nullable=False)
    applied_discount_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_reason: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    # Relationship
    member_coupon: Mapped["MemberCoupon"] = relationship(
        "MemberCoupon", back_populates="member_coupon_history"
    )
