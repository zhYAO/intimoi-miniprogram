"""Order item model."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, BigInteger, DateTime, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class OrderItem(Base):
    """Order items table - line items for orders."""

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(String(64), ForeignKey("orders.order_id"), nullable=False, index=True, comment="主订单号")
    sub_order_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, comment="子订单号")
    goods_id: Mapped[str] = mapped_column(String(32), nullable=False, comment="WDT商品ID")
    spec_id: Mapped[str] = mapped_column(String(32), nullable=False, comment="WDT规格ID")
    goods_name: Mapped[str] = mapped_column(String(256), nullable=False, comment="商品名称")
    spec_name: Mapped[str] = mapped_column(String(128), nullable=False, comment="规格名称")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="单价")
    num: Mapped[int] = mapped_column(Integer, nullable=False, comment="数量")
    refund_status: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="退款状态：0=无退款，1=部分退款，2=全部退款")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="创建时间")

    # Relationships
    order = relationship("Order", back_populates="items")
