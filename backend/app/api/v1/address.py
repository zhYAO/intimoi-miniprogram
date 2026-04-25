"""Address API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.member_address import MemberAddress
from app.middleware.auth import get_current_member_id
from app.utils.response import success, error, ERR_BAD_REQUEST, ERR_NOT_FOUND, ERR_INTERNAL
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class AddressRequest(BaseModel):
    receiver_name: str
    receiver_mobile: str
    receiver_province: str
    receiver_city: str
    receiver_district: str
    receiver_address: str
    is_default: bool = False


class UpdateAddressRequest(BaseModel):
    receiver_name: Optional[str] = None
    receiver_mobile: Optional[str] = None
    receiver_province: Optional[str] = None
    receiver_city: Optional[str] = None
    receiver_district: Optional[str] = None
    receiver_address: Optional[str] = None
    is_default: Optional[bool] = None


@router.get("")
async def get_addresses(
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """获取收货地址列表"""
    addresses = (
        db.query(MemberAddress)
        .filter(MemberAddress.member_id == member_id)
        .order_by(MemberAddress.is_default.desc(), MemberAddress.created_at.desc())
        .all()
    )
    
    default_id = None
    for addr in addresses:
        if addr.is_default:
            default_id = addr.id
            break
    
    items = [
        {
            "id": addr.id,
            "receiver_name": addr.receiver_name,
            "receiver_mobile": addr.receiver_mobile,
            "receiver_province": addr.receiver_province,
            "receiver_city": addr.receiver_city,
            "receiver_district": addr.receiver_district,
            "receiver_address": addr.receiver_address,
            "is_default": bool(addr.is_default),
            "created_at": addr.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for addr in addresses
    ]
    
    return success({
        "items": items,
        "default_id": default_id,
    })


@router.post("")
async def create_address(
    body: AddressRequest,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """新增收货地址"""
    if body.is_default:
        # Remove existing default
        db.query(MemberAddress).filter(
            MemberAddress.member_id == member_id,
            MemberAddress.is_default == 1,
        ).update({"is_default": 0})
    
    addr = MemberAddress(
        member_id=member_id,
        receiver_name=body.receiver_name,
        receiver_mobile=body.receiver_mobile,
        receiver_province=body.receiver_province,
        receiver_city=body.receiver_city,
        receiver_district=body.receiver_district,
        receiver_address=body.receiver_address,
        is_default=1 if body.is_default else 0,
    )
    db.add(addr)
    db.commit()
    db.refresh(addr)
    
    return success({"id": addr.id}, "地址已添加")


@router.put("/{address_id}")
async def update_address(
    address_id: int,
    body: UpdateAddressRequest,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """更新收货地址"""
    addr = (
        db.query(MemberAddress)
        .filter(MemberAddress.id == address_id, MemberAddress.member_id == member_id)
        .first()
    )
    
    if not addr:
        return error(ERR_NOT_FOUND, "地址不存在")
    
    if body.is_default:
        # Remove existing default
        db.query(MemberAddress).filter(
            MemberAddress.member_id == member_id,
            MemberAddress.is_default == 1,
        ).update({"is_default": 0})
    
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "is_default":
            value = 1 if value else 0
        setattr(addr, field, value)
    
    db.commit()
    return success(message="地址已更新")


@router.delete("/{address_id}")
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """删除收货地址"""
    addr = (
        db.query(MemberAddress)
        .filter(MemberAddress.id == address_id, MemberAddress.member_id == member_id)
        .first()
    )
    
    if not addr:
        return error(ERR_NOT_FOUND, "地址不存在")
    
    db.delete(addr)
    db.commit()
    return success(message="地址已删除")


@router.put("/{address_id}/default")
async def set_default_address(
    address_id: int,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """设置默认收货地址"""
    addr = (
        db.query(MemberAddress)
        .filter(MemberAddress.id == address_id, MemberAddress.member_id == member_id)
        .first()
    )
    
    if not addr:
        return error(ERR_NOT_FOUND, "地址不存在")
    
    # Remove existing default
    db.query(MemberAddress).filter(
        MemberAddress.member_id == member_id,
        MemberAddress.is_default == 1,
    ).update({"is_default": 0})
    
    addr.is_default = 1
    db.commit()
    
    return success(message="已设为默认地址")
