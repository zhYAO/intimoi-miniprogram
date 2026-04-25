"""Cart API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models.cart import Cart
from app.models.goods import Goods
from app.models.goods_spec import GoodsSpec
from app.middleware.auth import get_current_member_id
from app.utils.response import success, error, ERR_BAD_REQUEST, ERR_NOT_FOUND, ERR_UNAUTHORIZED, ERR_INTERNAL
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class AddCartRequest(BaseModel):
    goods_id: str
    spec_id: str
    num: int = 1


class UpdateCartRequest(BaseModel):
    num: int


class SelectAllRequest(BaseModel):
    selected: bool


@router.get("")
async def get_cart(
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """获取购物车列表"""
    items = (
        db.query(Cart)
        .filter(Cart.member_id == member_id)
        .all()
    )
    
    result = []
    total_amount = 0
    
    for item in items:
        # Join with goods_spec to get real-time stock and price
        spec = db.query(GoodsSpec).filter(GoodsSpec.spec_id == item.spec_id).first()
        goods = db.query(Goods).filter(Goods.goods_id == item.goods_id).first()
        
        price = float(spec.price) if spec else 0
        stock = spec.stock if spec else 0
        goods_name = goods.goods_name if goods else ""
        spec_name = spec.spec_name if spec else ""
        thumbnail = ""
        if goods and goods.images:
            import json
            try:
                images = json.loads(goods.images)
                thumbnail = images[0] if images else ""
            except:
                pass
        
        subtotal = price * item.num
        if item.selected:
            total_amount += subtotal
        
        result.append({
            "id": item.id,
            "goods_id": item.goods_id,
            "spec_id": item.spec_id,
            "goods_name": goods_name,
            "spec_name": spec_name,
            "price": price,
            "num": item.num,
            "stock": stock,
            "thumbnail": thumbnail,
            "selected": bool(item.selected),
        })
    
    return success({
        "items": result,
        "total_amount": round(total_amount, 2),
    })


@router.post("")
async def add_to_cart(
    body: AddCartRequest,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """添加商品至购物车"""
    # Check if already in cart
    existing = (
        db.query(Cart)
        .filter(
            Cart.member_id == member_id,
            Cart.goods_id == body.goods_id,
            Cart.spec_id == body.spec_id,
        )
        .first()
    )
    
    if existing:
        existing.num += body.num
        cart_item_id = existing.id
    else:
        cart_item = Cart(
            member_id=member_id,
            goods_id=body.goods_id,
            spec_id=body.spec_id,
            num=body.num,
            selected=1,
        )
        db.add(cart_item)
        db.flush()
        cart_item_id = cart_item.id
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return error(ERR_BAD_REQUEST, "添加购物车失败")
    
    # Count total items
    total_count = db.query(Cart).filter(Cart.member_id == member_id).count()
    
    return success({
        "cart_item_id": cart_item_id,
        "cart_count": total_count,
    }, "已加入购物车")


@router.put("/{item_id}")
async def update_cart_item(
    item_id: int,
    body: UpdateCartRequest,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """更新购物车商品数量（传0删除）"""
    item = (
        db.query(Cart)
        .filter(Cart.id == item_id, Cart.member_id == member_id)
        .first()
    )
    
    if not item:
        return error(ERR_NOT_FOUND, "购物车项不存在")
    
    if body.num <= 0:
        db.delete(item)
        db.commit()
        return success(message="已删除")
    
    item.num = body.num
    db.commit()
    return success(message="更新成功")


@router.delete("/{item_id}")
async def delete_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """删除购物车商品"""
    item = (
        db.query(Cart)
        .filter(Cart.id == item_id, Cart.member_id == member_id)
        .first()
    )
    
    if not item:
        return error(ERR_NOT_FOUND, "购物车项不存在")
    
    db.delete(item)
    db.commit()
    return success(message="已删除")


@router.put("/select-all")
async def select_all_cart(
    body: SelectAllRequest,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """全选/取消全选购物车"""
    selected = 1 if body.selected else 0
    db.query(Cart).filter(Cart.member_id == member_id).update({"selected": selected})
    db.commit()
    return success(message="操作成功")
