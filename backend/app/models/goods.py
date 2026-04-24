"""Goods model."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, BigInteger, DateTime, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Goods(Base):
    """Goods cache table - synced from WDT."""

    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    goods_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, comment="WDT商品ID")
    goods_no: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="商品货号")
    goods_name: Mapped[str] = mapped_column(String(256), nullable=False, comment="商品名称")
    category_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="分类ID")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0"), comment="售价")
    original_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="划线价")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="商品详情（富文本）")
    images: Mapped[str | None] = mapped_column(String(512), nullable=True, comment="商品图片列表（JSON数组）")
    sales: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="销量")
    is_on_sale: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否上架：0=下架，1=上架")
    wdt_synced_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="最近一次从WDT同步的时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="首次同步时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # Relationships
    specs = relationship("GoodsSpec", back_populates="goods", cascade="all, delete-orphan")
    favorites = relationship("Favorites", back_populates="goods")
