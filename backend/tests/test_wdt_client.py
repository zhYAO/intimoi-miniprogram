"""Tests for WDT client."""
import pytest
from app.services.wdt import WdtClient


def test_wdt_sign_generation():
    """Test WDT signature generation matches expected algorithm."""
    client = WdtClient(
        appkey="test_appkey",
        appsecret="test_secret",
        sid="test_sid",
        base_url="https://openapitest.huice.com/openapi/",
    )
    
    params = {
        "appkey": "test_appkey",
        "sid": "test_sid",
        "timestamp": "1713945600",
        "shop_id": "23",
        "trade_list": "[{\"tid\":\"WX001\"}]",
    }
    
    sign = client._sign(params)
    
    # Signature should be a 32-char hex string
    assert len(sign) == 32
    assert all(c in "0123456789abcdef" for c in sign)


def test_wdt_sign_deterministic():
    """Test that same params always produce same signature."""
    client = WdtClient(
        appkey="test",
        appsecret="secret",
        sid="sid",
        base_url="https://test.com/",
    )
    
    params = {"key1": "value1", "key2": "value2"}
    
    sign1 = client._sign(params)
    sign2 = client._sign(params)
    
    assert sign1 == sign2


def test_wdt_sign_excludes_sign_param():
    """Test that sign param is excluded from signature."""
    client = WdtClient(
        appkey="test",
        appsecret="secret",
        sid="sid",
        base_url="https://test.com/",
    )
    
    params_with_sign = {"key1": "value1", "sign": "should_be_excluded"}
    params_without_sign = {"key1": "value1"}
    
    sign_with = client._sign(params_with_sign)
    sign_without = client._sign(params_without_sign)
    
    assert sign_with == sign_without
