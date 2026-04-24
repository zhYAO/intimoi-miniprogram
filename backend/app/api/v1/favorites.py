"""Favorites API endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models.favorites import Favorites
from app.models.goods import Goods
from app.middleware.auth import get_current_member_id
from app.utils.response import success, error, ERR_BAD_REQUEST, ERR_NOT_FOUND, ERR_INTERNAL
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter()


class AddFavoriteRequest(BaseModel):
    goods_id: str


@router.get("")
async def get_favorites(
    page: int = Query(default=0, ge=0),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """获取收藏列表"""
    query = (
        db.query(Favorites)
        .filter(Favorites.member_id == member_id)
        .order_by(Favorites.created_at.desc())
    )
    
    total = query.count()
    items_raw = query.offset(page * page_size).limit(page_size).all()
    
    result = []
    for fav in items_raw:
        goods = db.query(Goods).filter(Goods.goods_id == fav.goods_id).first()
        if not goods:
            continue
        
        thumbnail = ""
        if goods.images:
            try:
                images = json.loads(goods.images)
                thumbnail = images[0] if images else ""
            except:
                pass
        
        result.append({
            "id": fav.id,
            "goods_id": fav.goods_id,
            "goods_name": goods.goods_name,
            "price": float(goods.price),
            "thumbnail": thumbnail,
            "created_at": fav.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })
    
    return success({
        "items": result,
    })


@router.post("")
async def add_favorite(
    body: AddFavoriteRequest,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """添加收藏"""
    # Check if goods exists
    goods = db.query(Goods).filter(Goods.goods_id == body.goods_id).first()
    if not goods:
        return error(ERR_NOT_FOUND, "商品不存在")
    
    # Check if already favorited
    existing = (
        db.query(Favorites)
        .filter(Favorites.member_id == member_id, Favorites.goods_id == body.goods_id)
        .first()
    )
    if existing:
        return success(message="已收藏")
    
    fav = Favorites(member_id=member_id, goods_id=body.goods_id)
    db.add(fav)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return error(ERR_BAD_REQUEST, "收藏失败")
    
    return success(message="已收藏")


@router.delete("/{goods_id}")
async def delete_favorite(
    goods_id: str,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """取消收藏"""
    fav = (
        db.query(Favorites)
        .filter(Favorites.member_id == member_id, Favorites.goods_id == goods_id)
        .first()
    )
    
    if not fav:
        return error(ERR_NOT_FOUND, "收藏不存在")
    
    db.delete(fav)
    db.commit()
    return success(message="已取消收藏")
