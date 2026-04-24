"""Goods spec model."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, BigInteger, DateTime, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class GoodsSpec(Base):
    """Goods spec cache table - synced from WDT."""

    __tablename__ = "goods_spec"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    spec_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, comment="WDT规格ID")
    goods_id: Mapped[str] = mapped_column(String(32), ForeignKey("goods.goods_id"), nullable=False, index=True, comment="WDT商品ID")
    spec_no: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="规格编码")
    spec_name: Mapped[str] = mapped_column(String(128), nullable=False, comment="规格名称")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="规格单价")
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="库存")
    is_on_sale: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否上架")
    wdt_synced_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="最近一次从WDT同步的时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="首次同步时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # Relationships
    goods = relationship("Goods", back_populates="specs")
