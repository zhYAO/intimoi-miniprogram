"""WeChat API service."""
import httpx
from app.config import get_settings

settings = get_settings()


async def code2session(code: str) -> dict:
    """
    Exchange WeChat login code for session info.
    Returns: {"openid": "...", "session_key": "...", "unionid": "..."}
    """
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": settings.wechat_appid,
        "secret": settings.wechat_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        
        if "errcode" in data and data["errcode"] != 0:
            raise Exception(f"WeChat API error: {data.get('errmsg', 'unknown')}")
        
        return data
