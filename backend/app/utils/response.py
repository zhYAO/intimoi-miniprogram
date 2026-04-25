"""Standard API response utilities."""
from typing import Any, Optional
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Standard API response format."""
    code: int = 0
    message: str = "操作成功"
    data: Optional[Any] = None


def success(data: Any = None, message: str = "操作成功") -> dict:
    """Return a success response."""
    return {"code": 0, "message": message, "data": data}


def error(code: int, message: str, data: Any = None) -> dict:
    """Return an error response."""
    return {"code": code, "message": message, "data": data}


# Error codes
ERR_BAD_REQUEST = 400
ERR_UNAUTHORIZED = 401
ERR_FORBIDDEN = 403
ERR_NOT_FOUND = 404
ERR_WDT_FAILED = 1001
ERR_WDT_SIGN_FAILED = 1002
ERR_WDT_PARSE_FAILED = 1003
ERR_INTERNAL = 500
