"""统一响应格式 Pydantic 模型。"""
from typing import Any, Optional
from pydantic import BaseModel


class Response(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None


# 错误码定义
class Err:
    OK = 0
    PARAM_ERROR = 1001
    SIGN_ERROR = 1002
    STOCK_ERROR = 2001
    GOODS_NOT_FOUND = 2002
    ORDER_NOT_FOUND = 3001
    ORDER_STATUS_ERROR = 3002
    WDT_ERROR = 4001
    UNAUTHORIZED = 5001


def ok(data: Any = None) -> dict:
    return {"code": Err.OK, "message": "success", "data": data}


def fail(code: int, message: str, data: Any = None) -> dict:
    return {"code": code, "message": message, "data": data}
