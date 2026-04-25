"""Favorites model."""
from datetime import datetime
from sqlalchemy import String, BigInteger, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Favorites(Base):
    """Favorites table - member's favorite goods."""

    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("member.id"), nullable=False, index=True, comment="会员ID")
    goods_id: Mapped[str] = mapped_column(String(32), ForeignKey("goods.goods_id"), nullable=False, comment="WDT商品ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="收藏时间")

    # Relationships
    member = relationship("Member", back_populates="favorites")
    goods = relationship("Goods", back_populates="favorites")
