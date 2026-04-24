"""订单接口。"""
import json
import uuid
from datetime import datetime, timezone
from typing import Optional, List

from fastapi import APIRouter, Depends, Query

from app.core.wdt import WdtClient
from app.core.security import get_current_user
from app.core.redis_ import CartStore
from app.schemas.response import ok, fail, Err
from app.config import settings

router = APIRouter()
wdt = WdtClient()

# 状态映射
STATUS_MAP = {
    (10, 0): "pending",     # 待付款
    (20, 1): "paid",        # 已付款待发货
    (30, 1): "shipped",     # 已发货
    (40, 1): "completed",   # 已完成
}
REFUND_STATUS = "refund"


def _trade_to_status(trade_status: int, pay_status: int) -> str:
    return STATUS_MAP.get((trade_status, pay_status), "pending")


def _generate_tid() -> str:
    """生成外部订单号。"""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"INTIMOI{ts}{uuid.uuid4().hex[:4].upper()}"


@router.post("/orders")
async def create_order(
    address_id: str,
    cart_item_ids: Optional[List[str]] = None,
    remark: str = "",
    user_id: str = Depends(get_current_user),
):
    """
    提交订单（推送至 WDT）。
    流程：查地址 → 查商品价格/库存 → 组装 trade_push → 推 WDT → 清购物车
    """
    # TODO: 地址服务（ad hoc 实现，待替换为真实地址查询）
    address = {
        "name": "用户",
        "mobile": "00000000000",
        "province": "省",
        "city": "市",
        "district": "区",
        "address": "地址",
    }

    cart_store = CartStore(user_id)
    cart_items = await cart_store.get_all()

    if not cart_items:
        return fail(Err.PARAM_ERROR, "购物车为空")

    # 过滤出要结算的项
    target_spec_ids = set(cart_items.keys())
    if cart_item_ids:
        target_spec_ids &= set(cart_item_ids)

    if not target_spec_ids:
        return fail(Err.PARAM_ERROR, "没有可结算的商品")

    # 查询商品实时价格/库存
    try:
        stock_info = await wdt.get_goods_stock(list(target_spec_ids))
    except Exception as e:
        return fail(Err.WDT_ERROR, f"查询商品信息失败: {e}")

    stock_map = {}
    if isinstance(stock_info, dict):
        for item in stock_info.get("data", []):
            for spec in item.get("specs", []):
                stock_map[spec.get("spec_id", "")] = spec

    # 组装 order_list
    order_list = []
    total_paid = 0
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    tid = _generate_tid()

    for idx, spec_id in enumerate(target_spec_ids):
        cart_item = cart_items.get(spec_id, {})
        num = cart_item.get("num", 1)
        spec_detail = stock_map.get(spec_id, {})
        price = float(spec_detail.get("price", 0) or 0)
        goods_id = spec_detail.get("goods_id", "")
        goods_no = spec_detail.get("goods_no", "")
        goods_name = spec_detail.get("goods_name", "")
        spec_no = spec_detail.get("spec_no", "")
        spec_name = spec_detail.get("spec_name", "")
        stock = int(spec_detail.get("stock", 0) or 0)

        if stock < num:
            return fail(Err.STOCK_ERROR, f"商品 {goods_name} 库存不足")

        order_list.append({
            "oid": f"{tid}-{idx + 1}",
            "goods_id": goods_id,
            "spec_id": spec_id,
            "goods_no": goods_no,
            "goods_name": goods_name,
            "spec_no": spec_no,
            "spec_name": spec_name,
            "price": price,
            "num": num,
            "discount": 0,
            "refund_status": 0,
        })
        total_paid += price * num

    # 组装 trade_push 参数
    trade_list = [{
        "tid": tid,
        "trade_status": 20,       # 已付款（微信支付回调后更新）
        "pay_status": 1,
        "delivery_term": 2,
        "trade_time": now_str,
        "buyer_nick": user_id,
        "receiver_mobile": address["mobile"],
        "receiver_name": address["name"],
        "receiver_province": address["province"],
        "receiver_city": address["city"],
        "receiver_district": address["district"],
        "receiver_address": address["address"],
        "logistics_type": 4,
        "post_amount": 0,
        "paid": total_paid,
        "order_list": order_list,
    }]

    # 推送至 WDT
    try:
        wdt_resp = await wdt.trade_push(trade_list)
        if wdt_resp.get("code") != 0 and wdt_resp.get("code") != "0":
            return fail(Err.WDT_ERROR, f"WDT 返回错误: {wdt_resp.get('message', '未知错误')}")
    except Exception as e:
        return fail(Err.WDT_ERROR, f"推送订单到 WDT 失败: {e}")

    # 清已结算的购物车项
    for spec_id in target_spec_ids:
        await cart_store.remove_item(spec_id)

    return ok({
        "order_id": tid,
        "amount": total_paid,
        "pay_url": "",  # 微信支付统一下单待接入
    })


@router.get("/orders")
async def list_orders(
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: str = Depends(get_current_user),
):
    """订单列表（从 WDT 查询）。"""
    # 反向映射：小程序状态 → WDT 状态
    status_reverse = {v: k for k, v in STATUS_MAP.items()}
    if status and status in status_reverse:
        trade_status, pay_status = status_reverse[status]
    else:
        trade_status, pay_status = None, None

    # 时间范围：最近 90 天
    now = datetime.now(timezone.utc)
    start = (now - datetime.timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
    end = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        raw = await wdt.trade_query(
            start_time=start,
            end_time=end,
            page_no=page,
            page_size=page_size,
        )
        trades = raw.get("trade_list", []) if isinstance(raw, dict) else []
        total = int(raw.get("total", len(trades)) if isinstance(raw, dict) else 0)
    except Exception as e:
        return fail(Err.WDT_ERROR, f"查询订单失败: {e}")

    items = []
    for t in trades:
        ts = t.get("trade_status")
        ps = int(t.get("pay_status", 0) or 0)
        items.append({
            "order_id": t.get("tid", ""),
            "trade_status": ts,
            "pay_status": ps,
            "paid": float(t.get("paid", 0) or 0),
            "trade_time": t.get("trade_time", ""),
            "goods_thumbnails": [
                g.get("image", "") for g in t.get("order_list", [])[:3]
            ],
            "goods_count": len(t.get("order_list", [])),
        })

    return ok({
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "has_more": page * page_size < total,
        },
    })


@router.get("/orders/{order_id}")
async def get_order(
    order_id: str,
    user_id: str = Depends(get_current_user),
):
    """订单详情（从 WDT 查询）。"""
    # WDT 不支持按订单号精确查询，用时间范围兜底
    # 生产环境应缓存订单到本地库，此处为简化实现
    now = datetime.now(timezone.utc)
    start = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    end = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        raw = await wdt.trade_query(start_time=start, end_time=end)
        trades = raw.get("trade_list", []) if isinstance(raw, dict) else []
    except Exception as e:
        return fail(Err.WDT_ERROR, f"查询订单详情失败: {e}")

    for t in trades:
        if t.get("tid") == order_id:
            receiver = t.get("receiver", {})
            logistics = t.get("logistics", {})
            order_goods = []
            for g in t.get("order_list", []):
                order_goods.append({
                    "oid": g.get("oid", ""),
                    "goods_name": g.get("goods_name", ""),
                    "spec_name": g.get("spec_name", ""),
                    "price": float(g.get("price", 0) or 0),
                    "num": int(g.get("num", 0) or 0),
                    "image": g.get("image", ""),
                })
            return ok({
                "order_id": order_id,
                "trade_status": t.get("trade_status"),
                "pay_status": int(t.get("pay_status", 0) or 0),
                "paid": float(t.get("paid", 0) or 0),
                "post_amount": float(t.get("post_amount", 0) or 0),
                "trade_time": t.get("trade_time", ""),
                "pay_time": t.get("pay_time", ""),
                "receiver": {
                    "name": receiver.get("name", ""),
                    "mobile": receiver.get("mobile", ""),
                    "province": receiver.get("province", ""),
                    "city": receiver.get("city", ""),
                    "district": receiver.get("district", ""),
                    "address": receiver.get("address", ""),
                },
                "logistics": {
                    "company": logistics.get("company", ""),
                    "tracking_no": logistics.get("tracking_no", ""),
                },
                "goods": order_goods,
                "remark": t.get("remark", ""),
            })

    return fail(Err.ORDER_NOT_FOUND, "订单不存在")


@router.post("/orders/{order_id}/cancel")
async def cancel_order(
    order_id: str,
    user_id: str = Depends(get_current_user),
):
    """取消订单。"""
    try:
        await wdt.trade_cancel(order_id, reason="用户取消")
        return ok()
    except Exception as e:
        return fail(Err.WDT_ERROR, f"取消订单失败: {e}")
