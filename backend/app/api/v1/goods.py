"""Goods API endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.goods import Goods
from app.models.goods_spec import GoodsSpec
from app.utils.response import success, error, ERR_NOT_FOUND, ERR_INTERNAL
from typing import Optional
import json

router = APIRouter()


@router.get("")
async def get_goods_list(
    category_id: Optional[int] = None,
    page: int = Query(default=0, ge=0),
    page_size: int = Query(default=20, ge=1, le=100),
    sort: str = "default",
    db: Session = Depends(get_db),
):
    """获取商品列表"""
    query = db.query(Goods).filter(Goods.is_on_sale == 1)
    
    if category_id:
        query = query.filter(Goods.category_id == category_id)
    
    # Sorting
    if sort == "price_asc":
        query = query.order_by(Goods.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Goods.price.desc())
    elif sort == "sales":
        query = query.order_by(Goods.sales.desc())
    else:
        query = query.order_by(Goods.id.desc())
    
    # Total count
    total = query.count()
    
    # Pagination
    items = query.offset(page * page_size).limit(page_size).all()
    
    result = []
    for g in items:
        # Parse images
        thumbnail = ""
        if g.images:
            try:
                images = json.loads(g.images)
                thumbnail = images[0] if images else ""
            except:
                pass
        
        # Calculate total stock from specs
        total_stock = (
            db.query(func.sum(GoodsSpec.stock))
            .filter(GoodsSpec.goods_id == g.goods_id)
            .scalar()
        ) or 0
        
        result.append({
            "goods_id": g.goods_id,
            "goods_name": g.goods_name,
            "price": float(g.price),
            "original_price": float(g.original_price) if g.original_price else None,
            "thumbnail": thumbnail,
            "sales": g.sales,
            "is_on_sale": g.is_on_sale,
            "stock": total_stock,
        })
    
    return success({
        "items": result,
        "total": total,
    })


@router.get("/{goods_id}")
async def get_goods_detail(
    goods_id: str,
    db: Session = Depends(get_db),
):
    """获取商品详情"""
    goods = db.query(Goods).filter(Goods.goods_id == goods_id).first()
    if not goods:
        return error(ERR_NOT_FOUND, "商品不存在")
    
    # Parse images
    images = []
    if goods.images:
        try:
            images = json.loads(goods.images)
        except:
            pass
    
    # Get specs
    specs = db.query(GoodsSpec).filter(GoodsSpec.goods_id == goods_id).all()
    specs_data = []
    total_stock = 0
    for spec in specs:
        total_stock += spec.stock
        specs_data.append({
            "spec_id": spec.spec_id,
            "spec_name": spec.spec_name,
            "stock": spec.stock,
            "price": float(spec.price),
        })
    
    return success({
        "goods_id": goods.goods_id,
        "goods_name": goods.goods_name,
        "price": float(goods.price),
        "original_price": float(goods.original_price) if goods.original_price else None,
        "description": goods.description,
        "images": images,
        "specs": specs_data,
        "stock": total_stock,
        "sales": goods.sales,
    })
