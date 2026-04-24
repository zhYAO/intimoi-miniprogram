"""Category model."""
from datetime import datetime
from sqlalchemy import String, BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Category(Base):
    """Category table - product categories."""

    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="分类名称")
    parent_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="父分类ID，顶级为NULL")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="排序（越小越靠前）")
    is_active: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否启用")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
