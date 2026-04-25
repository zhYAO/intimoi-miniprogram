"""Order model."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, BigInteger, DateTime, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Order(Base):
    """Orders table - local cache of orders pushed to WDT."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, comment="小程序订单号")
    wdt_tid: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="WDT生成的订单号")
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("member.id"), nullable=False, index=True, comment="会员ID")
    trade_status: Mapped[int] = mapped_column(Integer, nullable=False, comment="订单状态")
    pay_status: Mapped[str] = mapped_column(String(8), nullable=False, comment="支付状态")
    logistics_type: Mapped[int] = mapped_column(Integer, nullable=False, comment="物流类型")
    receiver_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="收货人")
    receiver_mobile: Mapped[str] = mapped_column(String(20), nullable=False, comment="联系电话")
    receiver_province: Mapped[str] = mapped_column(String(32), nullable=False, comment="省份")
    receiver_city: Mapped[str] = mapped_column(String(32), nullable=False, comment="城市")
    receiver_district: Mapped[str] = mapped_column(String(32), nullable=False, comment="区县")
    receiver_address: Mapped[str] = mapped_column(String(256), nullable=False, comment="详细地址")
    post_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0"), comment="运费")
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="订单总金额")
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0"), comment="已支付金额")
    trade_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="下单时间")
    push_status: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="推送状态：0=待推送，1=已推送，2=推送失败")
    push_msg: Mapped[str | None] = mapped_column(String(256), nullable=True, comment="推送失败原因")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # Relationships
    member = relationship("Member", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
