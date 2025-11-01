from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.member import Member


class Orders(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    member_id: Mapped[int] = mapped_column(
        ForeignKey("member.member_id"), nullable=False
    )
    member: Mapped["Member"] = relationship("Member", back_populates="orders")
    order_status: Mapped[str] = mapped_column(String(50), nullable=False)
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
