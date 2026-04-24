"""WDT 旺店通 SDK 封装 — 使用 httpx 异步调用。"""
import json
import hashlib
import time
import httpx
from typing import Any, Dict, List, Optional

from app.config import settings


class WdtClient:
    """旺店通 OpenAPI 客户端（异步版本）。"""

    connect_timeout = 3000  # ms
    read_timeout = 15000   # ms

    def __init__(
        self,
        appkey: Optional[str] = None,
        appsecret: Optional[str] = None,
        sid: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.appkey = appkey or settings.wdt_appkey
        self.appsecret = appsecret or settings.wdt_appsecret
        self.sid = sid or settings.wdt_sid
        self.base_url = (base_url or settings.wdt_base_url).rstrip("/") + "/"

    @staticmethod
    def _md5(text: str) -> bytes:
        m = hashlib.md5()
        m.update(text.encode("utf8"))
        return m.digest()

    @staticmethod
    def _byte2hex(data: bytes) -> str:
        return "".join(f"{(b & 0xFF):02X}" for b in data).lower()

    def _sign(self, params: Dict[str, str]) -> str:
        """计算 WDT 签名。"""
        keys = sorted(k for k in params if k != "sign")
        query_parts = []
        for key in keys:
            value = params[key]
            query_parts.append(f"{len(key):02d}-{key}:{len(value):04d}-{value}")
        query = "".join(query_parts) + self.appsecret
        return self._byte2hex(self._md5(query))

    def _build_form(self, params: Dict[str, Any]) -> Dict[str, str]:
        """将所有值转为字符串并计算 sign。"""
        flat: Dict[str, str] = {}
        for k, v in params.items():
            if isinstance(v, (list, dict)):
                flat[k] = json.dumps(v, ensure_ascii=False)
            elif v is None:
                flat[k] = ""
            else:
                flat[k] = str(v)
        flat["appkey"] = self.appkey
        flat["sid"] = self.sid
        flat["timestamp"] = str(int(time.time()))
        flat["sign"] = self._sign(flat)
        return flat

    async def execute(self, relative_url: str, params: Dict[str, Any]) -> Any:
        """POST 请求到 WDT 接口，返回解析后的 JSON 数据。"""
        form = self._build_form(params)
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=self.connect_timeout / 1000,
                read=self.read_timeout / 1000,
            )
        ) as client:
            resp = await client.post(self.base_url + relative_url, data=form)
            resp.raise_for_status()
            return resp.json()

    # ─── 商品接口 ────────────────────────────────────────────────

    async def get_goods_list(
        self,
        page_no: int = 1,
        page_size: int = 20,
        keyword: str = "",
        category_id: str = "",
    ) -> Dict[str, Any]:
        """
        获取商品列表（从 WDT 拉取）。
        WDT 实际接口以商家后台商品查询接口为准，此处为占位。
        """
        params = {
            "page_no": str(page_no),
            "page_size": str(page_size),
        }
        if keyword:
            params["keyword"] = keyword
        if category_id:
            params["category_id"] = category_id
        return await self.execute("goods_query.php", params)

    async def get_goods_detail(self, goods_id: str) -> Dict[str, Any]:
        """获取商品详情（从 WDT 拉取）。"""
        return await self.execute("goods_detail.php", {"goods_id": goods_id})

    async def get_goods_stock(self, spec_ids: List[str]) -> Dict[str, Any]:
        """批量查询规格库存。"""
        return await self.execute(
            "goods_stock_query.php",
            {"spec_ids": json.dumps(spec_ids)},
        )

    # ─── 订单接口 ────────────────────────────────────────────────

    async def trade_push(self, trade_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        推送订单到 WDT（trade_push.php）。
        :param trade_list: 订单列表，格式见 api-contract.md
        """
        return await self.execute(
            "trade_push.php",
            {"shop_id": settings.wdt_sid, "trade_list": trade_list},
        )

    async def trade_query(
        self,
        start_time: str,
        end_time: str,
        page_no: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        查询订单列表（trade_query.php）。
        :param start_time: YYYY-MM-DD HH:MM:SS
        :param end_time:   YYYY-MM-DD HH:MM:SS
        """
        return await self.execute(
            "trade_query.php",
            {
                "start_time": start_time,
                "end_time": end_time,
                "page_no": str(page_no),
                "page_size": str(page_size),
            },
        )

    async def trade_cancel(self, tid: str, reason: str = "") -> Dict[str, Any]:
        """取消订单（trade_cancel.php）。"""
        return await self.execute(
            "trade_cancel.php",
            {"tid": tid, "reason": reason},
        )

    # ─── 退款接口 ────────────────────────────────────────────────

    async def refund_apply(
        self,
        tid: str,
        oid: str,
        refund_type: str,
        reason: str,
        description: str = "",
        images: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        申请退款（refund_apply.php）。
        :param refund_type: refund=仅退款 / return=退货退款
        """
        params = {
            "tid": tid,
            "oid": oid,
            "refund_type": refund_type,
            "reason": reason,
        }
        if description:
            params["description"] = description
        if images:
            params["images"] = json.dumps(images)
        return await self.execute("refund_apply.php", params)

    async def refund_list(self, page_no: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """查询退款列表（refund_list.php）。"""
        return await self.execute(
            "refund_list.php",
            {"page_no": str(page_no), "page_size": str(page_size)},
        )
