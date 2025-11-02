from datetime import datetime

from sqlalchemy import BigInteger, String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


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
