"""WDT direct pass-through API endpoints."""
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.wdt import get_wdt_client
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.middleware.auth import get_current_member_id
from app.utils.response import success, error, ERR_BAD_REQUEST, ERR_WDT_FAILED, ERR_WDT_SIGN_FAILED, ERR_WDT_PARSE_FAILED, ERR_INTERNAL
from typing import Optional
import json
from datetime import datetime

router = APIRouter()


@router.post("/trade/push")
async def trade_push(
    shop_id: str = Form(...),
    trade_list: str = Form(...),
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """订单推送（创建原始订单）"""
    try:
        # Parse trade_list JSON
        trades = json.loads(trade_list)
    except json.JSONDecodeError:
        return error(ERR_BAD_REQUEST, "trade_list 格式错误，应为JSON数组")
    
    if not isinstance(trades, list) or len(trades) == 0:
        return error(ERR_BAD_REQUEST, "trade_list 至少需要包含一个订单")
    
    client = get_wdt_client("test")  # TODO: use env from config
    
    try:
        wdt_resp = client.trade_push(shop_id, trade_list)
    except Exception as e:
        return error(ERR_WDT_FAILED, f"WDT接口调用失败: {str(e)}")
    
    if wdt_resp.get("code") != 0 and wdt_resp.get("code") != "0":
        return error(ERR_WDT_FAILED, f"WDT接口调用失败: {wdt_resp.get('message', 'unknown')}", {
            "error_code": "TRADE_PUSH_ERROR",
            "wdt_response": str(wdt_resp),
        })
    
    # Save orders locally
    results = wdt_resp.get("data", {}).get("results", [])
    success_count = 0
    fail_count = 0
    
    for i, trade in enumerate(trades):
        tid = trade.get("tid")
        wdt_result = next((r for r in results if r.get("tid") == tid), {})
        wdt_tid = wdt_result.get("wdt_tid")
        status = wdt_result.get("status", "success") if wdt_result else "success"
        
        # Save order
        order = Order(
            order_id=tid,
            wdt_tid=wdt_tid,
            member_id=member_id,
            trade_status=trade.get("trade_status", 20),
            pay_status=trade.get("pay_status", "1"),
            logistics_type=trade.get("logistics_type", 4),
            receiver_name=trade.get("receiver_name", ""),
            receiver_mobile=trade.get("receiver_mobile", ""),
            receiver_province=trade.get("receiver_province", ""),
            receiver_city=trade.get("receiver_city", ""),
            receiver_district=trade.get("receiver_district", ""),
            receiver_address=trade.get("receiver_address", ""),
            post_amount=trade.get("post_amount", 0),
            total_amount=trade.get("paid", 0),
            paid_amount=trade.get("paid", 0),
            trade_time=datetime.strptime(trade.get("trade_time", "2000-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S"),
            push_status=1 if status == "success" else 2,
            push_msg="" if status == "success" else str(wdt_resp),
        )
        db.add(order)
        db.flush()
        
        # Save order items
        order_list = trade.get("order_list", [])
        for order_item in order_list:
            item = OrderItem(
                order_id=tid,
                sub_order_id=order_item.get("oid", ""),
                goods_id=order_item.get("goods_id", ""),
                spec_id=order_item.get("spec_id", ""),
                goods_name=order_item.get("goods_name", ""),
                spec_name=order_item.get("spec_name", ""),
                price=order_item.get("price", 0),
                num=order_item.get("num", 1),
                refund_status=order_item.get("refund_status", 0),
            )
            db.add(item)
        
        if status == "success":
            success_count += 1
        else:
            fail_count += 1
    
    db.commit()
    
    return success({
        "success_count": success_count,
        "fail_count": fail_count,
        "results": results,
    })


@router.post("/trade/query")
async def trade_query(
    start_time: str,
    end_time: str,
    page_no: int = 0,
    page_size: int = 20,
    db: Session = Depends(get_db),
):
    """订单查询"""
    client = get_wdt_client("test")
    
    try:
        wdt_resp = client.trade_query(start_time, end_time, page_no, page_size)
    except Exception as e:
        return error(ERR_WDT_FAILED, f"WDT接口调用失败: {str(e)}")
    
    if wdt_resp.get("code") != 0 and wdt_resp.get("code") != "0":
        return error(ERR_WDT_FAILED, f"WDT接口调用失败: {wdt_resp.get('message', 'unknown')}")
    
    return success({
        "total": wdt_resp.get("data", {}).get("total", 0),
        "page_no": page_no,
        "page_size": page_size,
        "orders": wdt_resp.get("data", {}).get("orders", []),
    })


@router.post("/weight/push")
async def weight_push(
    logistics_no: str,
    weight: float,
    is_setting: int = 0,
):
    """称重申传"""
    client = get_wdt_client("test")
    
    try:
        wdt_resp = client.weight_push(logistics_no, weight, is_setting)
    except Exception as e:
        return error(ERR_WDT_FAILED, f"WDT接口调用失败: {str(e)}")
    
    return success({
        "logistics_no": logistics_no,
        "weight": weight,
        "status": "success",
    })
