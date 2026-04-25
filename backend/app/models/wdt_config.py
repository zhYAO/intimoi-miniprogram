"""WDT config model."""
from datetime import datetime
from sqlalchemy import String, BigInteger, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class WdtConfig(Base):
    """WDT config table - stores WDT account configuration."""

    __tablename__ = "wdt_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    env: Mapped[str] = mapped_column(Enum("test", "prod"), unique=True, nullable=False, comment="环境：test=测试，prod=正式")
    appkey: Mapped[str] = mapped_column(String(64), nullable=False, comment="WDT AppKey")
    appsecret: Mapped[str] = mapped_column(String(128), nullable=False, comment="WDT AppSecret（AES-256加密存储）")
    sid: Mapped[str] = mapped_column(String(32), nullable=False, comment="WDT SID")
    base_url: Mapped[str] = mapped_column(String(128), nullable=False, comment="API Base URL")
    is_active: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否启用")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
