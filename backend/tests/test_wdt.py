"""WDT 签名算法单元测试。"""
import pytest
from app.core.wdt import WdtClient


class TestWdtSign:
    """测试 WDT 签名算法。"""

    def test_sign_consistency(self):
        """
        相同参数两次签名结果一致。
        WDT 签名要求：keys 排序后，按 len:key:len:value 拼接，最后加 appsecret。
        """
        client = WdtClient(
            appkey="test_appkey",
            appsecret="test_secret",
            sid="test_sid",
            base_url="https://example.com/",
        )
        params = {
            "appkey": "test_appkey",
            "sid": "test_sid",
            "timestamp": "1740000000",
            "goods_id": "18344",
        }
        sig1 = client._sign(params)
        sig2 = client._sign(params)
        assert sig1 == sig2
        assert len(sig1) == 32  # MD5 hex

    def test_sign_different_params_different_result(self):
        """不同参数应产生不同签名。"""
        client = WdtClient(
            appkey="test_appkey",
            appsecret="test_secret",
            sid="test_sid",
            base_url="https://example.com/",
        )
        params1 = {"appkey": "a", "sid": "b", "timestamp": "1", "goods_id": "1"}
        params2 = {"appkey": "a", "sid": "b", "timestamp": "1", "goods_id": "2"}
        sig1 = client._sign(params1)
        sig2 = client._sign(params2)
        assert sig1 != sig2

    def test_sign_excludes_sign_key(self):
        """签名计算时自动排除 sign 字段本身。"""
        client = WdtClient(
            appkey="test_appkey",
            appsecret="test_secret",
            sid="test_sid",
            base_url="https://example.com/",
        )
        params_with_sign = {"appkey": "a", "sid": "b", "timestamp": "1", "sign": "ignore_this"}
        params_without_sign = {"appkey": "a", "sid": "b", "timestamp": "1"}
        sig1 = client._sign(params_with_sign)
        sig2 = client._sign(params_without_sign)
        assert sig1 == sig2

    def test_build_form_adds_required_fields(self):
        """_build_form 自动注入 appkey/sid/timestamp/sign。"""
        client = WdtClient(
            appkey="my_appkey",
            appsecret="my_secret",
            sid="my_sid",
            base_url="https://example.com/",
        )
        form = client._build_form({"goods_id": "18344"})
        assert "appkey" in form
        assert "sid" in form
        assert "timestamp" in form
        assert "sign" in form
        assert form["appkey"] == "my_appkey"
        assert form["sid"] == "my_sid"
        assert len(form["sign"]) == 32

    def test_build_form_serializes_list_as_json(self):
        """_build_form 将 list/dict 序列化为 JSON 字符串。"""
        import json
        client = WdtClient(
            appkey="test_appkey",
            appsecret="test_secret",
            sid="test_sid",
            base_url="https://example.com/",
        )
        trade_list = [{"tid": "T001", "paid": 100}]
        form = client._build_form({"trade_list": trade_list, "shop_id": "23"})
        assert isinstance(form["trade_list"], str)
        assert json.loads(form["trade_list"]) == trade_list
