"""JWT 认证工具。"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings
from app.schemas.response import Err

# HTTP Bearer scheme
bearer = HTTPBearer()


def create_token(user_id: str, extra: Optional[dict] = None) -> str:
    """生成 JWT token。"""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_expire_minutes),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    """解析 JWT token，返回 payload。"""
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail={"code": Err.UNAUTHORIZED, "message": "Token 无效或已过期"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> str:
    """FastAPI 依赖：从 Bearer token 中提取 user_id。"""
    payload = decode_token(credentials.credentials)
    user_id: str = payload.get("sub", "")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail={"code": Err.UNAUTHORIZED, "message": "Token 无效"},
        )
    return user_id
