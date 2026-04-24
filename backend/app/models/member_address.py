"""Member address model."""
from datetime import datetime
from sqlalchemy import String, BigInteger, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class MemberAddress(Base):
    """Member address table - stores shipping addresses."""

    __tablename__ = "member_address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("member.id"), nullable=False, index=True, comment="会员ID")
    receiver_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="收货人姓名")
    receiver_mobile: Mapped[str] = mapped_column(String(20), nullable=False, comment="联系电话")
    receiver_province: Mapped[str] = mapped_column(String(32), nullable=False, comment="省份")
    receiver_city: Mapped[str] = mapped_column(String(32), nullable=False, comment="城市")
    receiver_district: Mapped[str] = mapped_column(String(32), nullable=False, comment="区县")
    receiver_address: Mapped[str] = mapped_column(String(256), nullable=False, comment="详细地址")
    is_default: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="是否默认地址：0=否，1=是")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="添加时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # Relationships
    member = relationship("Member", back_populates="addresses")
