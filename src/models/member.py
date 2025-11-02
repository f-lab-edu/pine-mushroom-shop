import enum
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    String,
    Boolean,
    Enum,
    Date,
    DateTime,
    Integer,
    func,
    ForeignKey,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.orders import Orders
    from src.models.coupon import MemberCoupon


class MemberGender(str, enum.Enum):
    MALE = "남"
    FEMALE = "여"


class Member(Base):
    __tablename__ = "member"
    # Columns
    member_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    login_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    password_check_question: Mapped[str] = mapped_column(String(100), nullable=False)
    password_check_answer: Mapped[str] = mapped_column(String(255), nullable=False)
    member_name: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_email_agreed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    gender: Mapped[str] = mapped_column(Enum(MemberGender), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    points_balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None
    )
    # Relationship
    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="member")
    member_coupon: Mapped[list["MemberCoupon"]] = relationship(
        "MemberCoupon", back_populates="member"
    )
    points_history: Mapped[list["PointsHistory"]] = relationship(
        "PointsHistory", back_populates="member"
    )


class PointsHistory(Base):
    __tablename__ = "points_history"
    # Columns
    points_history_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    member_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("member.member_id"), nullable=False
    )
    previous_points_balance: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    current_points_balance: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_reason: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    # Relationship
    member: Mapped["Member"] = relationship("Member", back_populates="points_history")
