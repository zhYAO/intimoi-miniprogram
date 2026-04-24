"""购物车接口。"""
import uuid
from fastapi import APIRouter, Depends

from app.core.redis_ import CartStore
from app.core.security import get_current_user
from app.core.wdt import WdtClient
from app.schemas.response import ok, fail, Err

router = APIRouter()
wdt = WdtClient()


@router.post("/cart")
async def add_cart(
    spec_id: str,
    num: int = 1,
    user_id: str = Depends(get_current_user),
):
    """添加购物车。"""
    if num < 1:
        return fail(Err.PARAM_ERROR, "数量必须大于0")
    store = CartStore(user_id)
    await store.add_item(spec_id, num)
    total = await store.total_items()
    cart_item_id = f"ci_{uuid.uuid4().hex[:12]}"
    return ok({"cart_item_id": cart_item_id, "total_items": total})


@router.get("/cart")
async def get_cart(user_id: str = Depends(get_current_user)):
    """获取购物车。"""
    store = CartStore(user_id)
    items_raw = await store.get_all()
    spec_ids = list(items_raw.keys())

    # 批量查询商品信息（名称/价格/图片/库存）
    if not spec_ids:
        return ok({"items": [], "total_amount": 0})

    try:
        stock_info = await wdt.get_goods_stock(spec_ids)
    except Exception:
        stock_info = {}

    # 解析 stock_info，建立 spec_id → 库存的映射
    stock_map = {}
    if isinstance(stock_info, dict):
        for item in stock_info.get("data", []):
            for spec in item.get("specs", []):
                stock_map[spec.get("spec_id", "")] = spec

    items = []
    total_amount = 0
    for spec_id, item_data in items_raw.items():
        num = item_data.get("num", 1)
        spec_detail = stock_map.get(spec_id, {})
        price = float(spec_detail.get("price", 0) or 0)
        stock = int(spec_detail.get("stock", 0) or 0)
        goods_name = spec_detail.get("goods_name", "")
        spec_name = spec_detail.get("spec_name", "")
        image = spec_detail.get("image", "")

        stock_status = "low" if 0 < stock <= 10 else "sufficient"

        items.append({
            "cart_item_id": f"ci_{spec_id}",
            "spec_id": spec_id,
            "goods_name": goods_name,
            "spec_name": spec_name,
            "price": price,
            "num": num,
            "image": image,
            "stock_status": stock_status,
            "checked": True,
        })
        total_amount += price * num

    return ok({"items": items, "total_amount": total_amount})


@router.put("/cart/{spec_id}")
async def update_cart(
    spec_id: str,
    num: int,
    user_id: str = Depends(get_current_user),
):
    """更新购物车商品数量。"""
    if num < 0:
        return fail(Err.PARAM_ERROR, "数量不能为负")
    store = CartStore(user_id)
    await store.update_num(spec_id, num)
    return ok()


@router.delete("/cart/{spec_id}")
async def delete_cart_item(
    spec_id: str,
    user_id: str = Depends(get_current_user),
):
    """删除购物车商品。"""
    store = CartStore(user_id)
    await store.remove_item(spec_id)
    return ok()
