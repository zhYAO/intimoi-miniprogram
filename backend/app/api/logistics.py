"""物流接口。"""
from fastapi import APIRouter
from app.schemas.response import ok, fail, Err

router = APIRouter()

# 注：实际快递100/快递公司接口待接入


@router.get("/logistics/{tracking_no}")
async def get_logistics(tracking_no: str):
    """
    查询物流信息。
    实际调用快递100或快递公司官方接口（参考 WDT logistics_sync）。
    此处为占位返回。
    """
    return ok({
        "company": "",
        "tracking_no": tracking_no,
        "nodes": [],
    })
