"""认证接口 — 微信登录。"""
from fastapi import APIRouter, HTTPException

from app.core.security import create_token
from app.schemas.response import ok, fail, Err

router = APIRouter()

# 注：微信登录需用 code 换 openid，此处为占位实现
# 真实场景：wx.login() → 小程序传 code → 后端调微信 API 换 openid/session_key


@router.post("/auth/login")
async def login(code: str = ""):
    """
    微信授权登录。
    :param code: 微信授权 code（小程序 wx.login() 获得）
    """
    if not code:
        return fail(Err.PARAM_ERROR, "code 不能为空")

    # TODO: 用 code 调用微信接口换 openid
    # 此处占位：用 code 摘要作为 user_id
    import hashlib
    user_id = "user_" + hashlib.sha256(code.encode()).hexdigest()[:16]

    token = create_token(user_id)
    return ok({
        "token": token,
        "user": {
            "id": user_id,
            "nickname": "intimoi_user",
            "avatar": "",
            "phone": "",
        },
    })
