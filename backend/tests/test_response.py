"""响应格式单元测试。"""
import pytest
from app.schemas.response import ok, fail, Err


class TestResponse:
    def test_ok_with_data(self):
        r = ok({"name": "test"})
        assert r["code"] == 0
        assert r["message"] == "success"
        assert r["data"] == {"name": "test"}

    def test_ok_without_data(self):
        r = ok()
        assert r["code"] == 0
        assert r["message"] == "success"
        assert r["data"] is None

    def test_fail(self):
        r = fail(Err.PARAM_ERROR, "参数错误")
        assert r["code"] == 1001
        assert r["message"] == "参数错误"
        assert r["data"] is None

    def test_fail_with_data(self):
        r = fail(Err.WDT_ERROR, "WDT 调用失败", {"detail": "timeout"})
        assert r["code"] == 4001
        assert r["data"] == {"detail": "timeout"}

    def test_err_constants(self):
        assert Err.OK == 0
        assert Err.PARAM_ERROR == 1001
        assert Err.STOCK_ERROR == 2001
        assert Err.ORDER_NOT_FOUND == 3001
        assert Err.WDT_ERROR == 4001
        assert Err.UNAUTHORIZED == 5001
