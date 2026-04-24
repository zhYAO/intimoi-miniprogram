"""WDT SDK client wrapper service."""
import json
import hashlib
import time
import requests
from typing import Any, Optional
from app.config import get_settings

settings = get_settings()


class WdtClient:
    """WDT API client with signature generation."""

    def __init__(self, appkey: str, appsecret: str, sid: str, base_url: str):
        self.appkey = appkey
        self.appsecret = appsecret
        self.sid = sid
        self.base_url = base_url.rstrip("/") + "/"

    def _sign(self, params: dict) -> str:
        """Generate WDT signature."""
        keys = sorted(k for k in params.keys() if k != "sign")
        query_parts = []
        for key in keys:
            value = str(params[key])
            query_parts.append(f"{len(key):02d}-{key}:{len(value):04d}-{value}")
        query_str = ";".join(query_parts) + self.appsecret
        m = hashlib.md5()
        m.update(query_str.encode("utf8"))
        return m.hexdigest()

    def _post(self, relative_url: str, params: dict) -> dict:
        """Execute a WDT API call."""
        params.update({
            "appkey": self.appkey,
            "sid": self.sid,
            "timestamp": str(int(time.time())),
        })
        params["sign"] = self._sign(params)
        
        # WDT expects application/x-www-form-urlencoded
        url = self.base_url + relative_url
        resp = requests.post(url, data=params, timeout=(3, 15))
        resp.raise_for_status()
        return resp.json()

    def trade_push(self, shop_id: str, trade_list: str) -> dict:
        """Push orders to WDT."""
        return self._post("trade_push.php", {"shop_id": shop_id, "trade_list": trade_list})

    def trade_query(self, start_time: str, end_time: str, page_no: int, page_size: int) -> dict:
        """Query orders from WDT."""
        return self._post("trade_query.php", {
            "start_time": start_time,
            "end_time": end_time,
            "page_no": str(page_no),
            "page_size": str(page_size),
        })

    def weight_push(self, logistics_no: str, weight: float, is_setting: int) -> dict:
        """Push weight to WDT."""
        return self._post("vip_stockout_sales_weight_push.php", {
            "logistics_no": logistics_no,
            "weight": str(weight),
            "is_setting": str(is_setting),
        })


def get_wdt_client(env: str = "test") -> WdtClient:
    """Get WDT client for specified environment."""
    # Import here to avoid circular import
    from app.models.wdt_config import WdtConfig
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        config = db.query(WdtConfig).filter(WdtConfig.env == env, WdtConfig.is_active == 1).first()
        if not config:
            # Fallback to constants from wdt_constants.py
            from app.services.wdt_constants import WDT_CONFIG
            cfg = WDT_CONFIG[env]
            return WdtClient(cfg["appkey"], cfg["appsecret"], cfg["sid"], cfg["base_url"])
        
        # Decrypt appsecret
        from app.utils.crypto import decrypt_aes256
        appsecret = decrypt_aes256(config.appsecret)
        return WdtClient(config.appkey, appsecret, config.sid, config.base_url)
    finally:
        db.close()
