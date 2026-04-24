"""JWT 认证单元测试。"""
import pytest
import time
from datetime import datetime, timezone
from jose import jwt

from app.core.security import create_token, decode_token
from app.config import settings


class TestJWT:
    def test_create_token_returns_string(self):
        """create_token 应返回非空字符串。"""
        token = create_token("user_123")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_token_returns_payload(self):
        """decode_token 应正确解析 payload。"""
        user_id = "user_abc"
        token = create_token(user_id)
        payload = decode_token(token)
        assert payload["sub"] == user_id

    def test_decode_invalid_token_raises(self):
        """无效 token 应抛出 HTTPException。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            decode_token("invalid.token.here")
        assert exc_info.value.status_code == 401

    def test_token_expired(self):
        """过期的 token 应被拒绝。"""
        from fastapi import HTTPException
        from datetime import timedelta
        now = datetime.now(timezone.utc)
        expired_payload = {
            "sub": "user_123",
            "iat": now,
            "exp": now - timedelta(seconds=60),  # 1分钟前过期
        }
        expired_token = jwt.encode(
            expired_payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        with pytest.raises(HTTPException) as exc_info:
            decode_token(expired_token)
        assert exc_info.value.status_code == 401

    def test_token_with_extra_claims(self):
        """create_token 支持额外字段。"""
        token = create_token("user_123", extra={"role": "admin"})
        payload = decode_token(token)
        assert payload["sub"] == "user_123"
        assert payload["role"] == "admin"
