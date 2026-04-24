"""订单 Pydantic 模型。"""
from typing import List, Optional
from pydantic import BaseModel


class Receiver(BaseModel):
    name: str
    mobile: str
    province: str
    city: str
    district: str
    address: str


class Logistics(BaseModel):
    company: str = ""
    tracking_no: str = ""


class OrderGoods(BaseModel):
    oid: str
    goods_name: str
    spec_name: str
    price: float
    num: int
    image: str = ""


class Order(BaseModel):
    order_id: str
    trade_status: int = 10
    pay_status: int = 0
    paid: float = 0
    post_amount: float = 0
    trade_time: str = ""
    pay_time: str = ""
    receiver: Optional[Receiver] = None
    logistics: Optional[Logistics] = None
    goods: List[OrderGoods] = []
    remark: str = ""


class OrderListItem(BaseModel):
    order_id: str
    trade_status: int
    pay_status: int
    paid: float
    trade_time: str
    goods_thumbnails: List[str] = []
    goods_count: int = 0
