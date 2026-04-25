"""Tests for JWT authentication."""
import pytest
import jwt
import datetime
from app.middleware.auth import create_token, decode_token
from app.config import get_settings

settings = get_settings()


def test_create_and_decode_token():
    """Test token creation and decoding."""
    token = create_token(member_id=123, open_id="test_open_id")
    
    payload = decode_token(token)
    
    assert payload["member_id"] == 123
    assert payload["open_id"] == "test_open_id"


def test_token_contains_expiration():
    """Test that token has expiration."""
    token = create_token(member_id=1, open_id="test")
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    
    assert "exp" in payload
    assert "iat" in payload
    assert payload["exp"] > payload["iat"]


def test_invalid_token_raises():
    """Test that invalid token raises HTTPException."""
    from fastapi import HTTPException
    
    with pytest.raises(HTTPException) as exc_info:
        decode_token("invalid.token.here")
    
    assert exc_info.value.status_code == 401
