"""商品接口。"""
import uuid
from typing import Optional
from fastapi import APIRouter, Query

from app.core.wdt import WdtClient
from app.schemas.response import ok, fail, Err

router = APIRouter()
wdt = WdtClient()

STOCK_LOW_THRESHOLD = 10


def _stock_status(stock: int) -> str:
    return "low" if 0 < stock <= STOCK_LOW_THRESHOLD else "sufficient"


def _map_goods(wdt_goods: dict) -> dict:
    """将 WDT 商品数据映射为小程序商品格式。"""
    goods_id = str(wdt_goods.get("goods_id", ""))
    price = float(wdt_goods.get("price", 0) or 0)
    original_price = float(wdt_goods.get("original_price", 0) or 0)
    stock = int(wdt_goods.get("stock", 0) or 0)
    images = wdt_goods.get("images", [])
    if isinstance(images, str):
        images = [images]
    return {
        "id": goods_id,
        "name": wdt_goods.get("goods_name", ""),
        "subtitle": wdt_goods.get("subtitle", ""),
        "price": price,
        "original_price": original_price,
        "image": images[0] if images else "",
        "images": images,
        "stock": stock,
        "stock_status": _stock_status(stock),
        "specs": [
            {
                "spec_id": s.get("spec_id", ""),
                "spec_name": s.get("spec_name", ""),
                "price": float(s.get("price", 0) or 0),
                "stock": int(s.get("stock", 0) or 0),
            }
            for s in wdt_goods.get("specs", [])
        ],
        "detail_html": wdt_goods.get("detail_html", ""),
    }


@router.get("/products")
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: Optional[str] = None,
    keyword: Optional[str] = None,
    sort: str = Query("default"),
):
    """商品列表（从 WDT 拉取）。"""
    try:
        raw = await wdt.get_goods_list(
            page_no=page,
            page_size=page_size,
            keyword=keyword or "",
            category_id=category_id or "",
        )
        goods_list = raw.get("goods_list", []) if isinstance(raw, dict) else []
        total = int(raw.get("total", len(goods_list)) if isinstance(raw, dict) else 0)

        items = [_map_goods(g) for g in goods_list]

        # 价格排序（由后端排序，WDT 通常支持）
        if sort == "price_asc":
            items.sort(key=lambda x: x["price"])
        elif sort == "price_desc":
            items.sort(key=lambda x: -x["price"])

        return ok({
            "items": items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "has_more": page * page_size < total,
            },
        })
    except Exception as e:
        return fail(Err.WDT_ERROR, f"获取商品列表失败: {e}")


@router.get("/products/{goods_id}")
async def get_product(goods_id: str):
    """商品详情（从 WDT 拉取）。"""
    try:
        raw = await wdt.get_goods_detail(goods_id)
        goods = raw if isinstance(raw, dict) else {}
        return ok(_map_goods(goods))
    except Exception as e:
        return fail(Err.WDT_ERROR, f"获取商品详情失败: {e}")
