"""购物车 Pydantic 模型。"""
from typing import List, Optional
from pydantic import BaseModel


class CartItem(BaseModel):
    cart_item_id: str
    spec_id: str
    goods_name: str = ""
    spec_name: str = ""
    price: float = 0
    num: int = 1
    image: str = ""
    stock_status: str = "sufficient"
    checked: bool = True


class Cart(BaseModel):
    items: List[CartItem] = []
    total_amount: float = 0
