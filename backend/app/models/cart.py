"""Cart model."""
from datetime import datetime
from sqlalchemy import String, BigInteger, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Cart(Base):
    """Cart table - shopping cart items."""

    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("member.id"), nullable=False, index=True, comment="会员ID")
    goods_id: Mapped[str] = mapped_column(String(32), nullable=False, comment="WDT商品ID")
    spec_id: Mapped[str] = mapped_column(String(32), nullable=False, comment="WDT规格ID")
    num: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="数量")
    selected: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否选中结算：0=未选，1=选中")
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="实时库存（查询时回填，不持久化）")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="加入时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # Relationships
    member = relationship("Member", back_populates="cart_items")
