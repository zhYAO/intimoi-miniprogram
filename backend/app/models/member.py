"""Member model."""
from datetime import datetime
from sqlalchemy import String, BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Member(Base):
    """Member table - stores WeChat login members."""

    __tablename__ = "member"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    open_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, comment="微信OpenID")
    session_key: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="微信SessionKey")
    nickname: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="昵称")
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True, comment="头像URL")
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True, comment="手机号")
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="会员等级：1=普通，2=银卡，3=金卡")
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="最后登录时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="注册时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # Relationships
    addresses = relationship("MemberAddress", back_populates="member", cascade="all, delete-orphan")
    cart_items = relationship("Cart", back_populates="member", cascade="all, delete-orphan")
    favorites = relationship("Favorites", back_populates="member", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="member", cascade="all, delete-orphan")
