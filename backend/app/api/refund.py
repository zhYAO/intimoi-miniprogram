"""售后接口。"""
from typing import Optional, List
from fastapi import APIRouter, Depends

from app.core.wdt import WdtClient
from app.core.security import get_current_user
from app.schemas.response import ok, fail, Err

router = APIRouter()
wdt = WdtClient()


@router.post("/refund")
async def apply_refund(
    order_id: str,
    oid: str,
    type: str,  # refund / return
    reason: str,
    description: str = "",
    images: Optional[List[str]] = None,
    user_id: str = Depends(get_current_user),
):
    """申请售后（退款/退货）。"""
    if type not in ("refund", "return"):
        return fail(Err.PARAM_ERROR, "type 必须为 refund 或 return")
    try:
        result = await wdt.refund_apply(
            tid=order_id,
            oid=oid,
            refund_type=type,
            reason=reason,
            description=description,
            images=images,
        )
        if result.get("code") != 0:
            return fail(Err.WDT_ERROR, f"申请售后失败: {result.get('message')}")
        return ok({"refund_id": result.get("refund_id", "")})
    except Exception as e:
        return fail(Err.WDT_ERROR, f"申请售后失败: {e}")


@router.get("/refund")
async def list_refunds(
    user_id: str = Depends(get_current_user),
):
    """售后列表。"""
    try:
        raw = await wdt.refund_list()
        items = raw.get("refund_list", []) if isinstance(raw, dict) else []
        return ok({"items": items})
    except Exception as e:
        return fail(Err.WDT_ERROR, f"查询售后列表失败: {e}")
