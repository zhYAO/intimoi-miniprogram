"""商品 Pydantic 模型。"""
from typing import List, Optional
from pydantic import BaseModel


class SpecInfo(BaseModel):
    spec_id: str
    spec_name: str
    price: float
    stock: int


class Product(BaseModel):
    id: str
    name: str
    subtitle: str = ""
    price: float
    original_price: float = 0
    image: str = ""
    images: List[str] = []
    stock: int = 0
    stock_status: str = "sufficient"  # sufficient / low
    specs: List[SpecInfo] = []
    detail_html: str = ""


class ProductListItem(BaseModel):
    id: str
    name: str
    subtitle: str = ""
    price: float
    original_price: float = 0
    image: str = ""
    stock: int = 0
    stock_status: str = "sufficient"
