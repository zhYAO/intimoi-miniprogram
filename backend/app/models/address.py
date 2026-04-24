"""收货地址 Pydantic 模型。"""
from typing import List
from pydantic import BaseModel


class Address(BaseModel):
    id: str
    name: str
    mobile: str
    province: str
    city: str
    district: str
    address: str
    is_default: bool = False


class AddressCreate(BaseModel):
    name: str
    mobile: str
    province: str
    city: str
    district: str
    address: str
    is_default: bool = False


class AddressUpdate(BaseModel):
    name: str = ""
    mobile: str = ""
    province: str = ""
    city: str = ""
    district: str = ""
    address: str = ""
    is_default: bool = False
