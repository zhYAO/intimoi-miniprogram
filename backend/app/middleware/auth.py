"""JWT authentication middleware."""
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import jwt
from app.config import get_settings

settings = get_settings()
security = HTTPBearer(auto_error=False)


def create_token(member_id: int, open_id: str) -> str:
    """Create a JWT token for a member."""
    import datetime
    payload = {
        "member_id": member_id,
        "open_id": open_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=settings.jwt_expiration_hours),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token."""
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的Token")


async def get_current_member_id(request: Request) -> int:
    """Get current member ID from Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录或Token已过期")
    
    token = auth_header[7:]
    payload = decode_token(token)
    return payload["member_id"]


class AuthMiddleware(BaseHTTPMiddleware):
    """Optional auth middleware - sets member_id if token present."""

    PUBLIC_PATHS = {
        "/api/v1/member/login",
        "/api/v1/wdt/trade/push",
        "/api/v1/wdt/trade/query",
        "/api/v1/wdt/weight/push",
        "/health",
    }

    async def dispatch(self, request: Request, call_next):
        # Skip auth for public paths
        if any(request.url.path.startswith(p) for p in self.PUBLIC_PATHS):
            return await call_next(request)
        
        response = await call_next(request)
        return response
