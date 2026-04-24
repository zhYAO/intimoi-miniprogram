"""用户信息接口。"""
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.response import ok

router = APIRouter()


@router.get("/user/profile")
async def get_profile(user_id: str = Depends(get_current_user)):
    """
    获取用户信息。
    注意：本项目无积分系统。
    """
    return ok({
        "id": user_id,
        "nickname": "intimoi_user",
        "avatar": "",
        "phone": "",
    })
