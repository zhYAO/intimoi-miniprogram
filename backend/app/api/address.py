"""收货地址接口。"""
import uuid
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.core.redis_ import RedisClient
from app.schemas.response import ok, fail, Err

router = APIRouter()

ADDR_KEY_PREFIX = "addr:"


class AddressStore:
    """收货地址存储（Redis Hash）。"""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.key = f"{ADDR_KEY_PREFIX}{user_id}"

    async def _r(self):
        return await RedisClient.get_client()

    async def get_all(self) -> dict:
        client = await self._r()
        raw = await client.hgetall(self.key)
        return {k: __import__("json").loads(v) for k, v in raw.items()}

    async def get(self, addr_id: str) -> dict:
        client = await self._r()
        raw = await client.hget(self.key, addr_id)
        if not raw:
            return {}
        return __import__("json").loads(raw)

    async def save(self, addr_id: str, data: dict) -> None:
        client = await self._r()
        await client.hset(self.key, addr_id, __import__("json").dumps(data, ensure_ascii=False))
        # 如果是默认地址，取消其他默认
        if data.get("is_default"):
            all_addr = await self.get_all()
            for k, v in all_addr.items():
                if k != addr_id and v.get("is_default"):
                    v["is_default"] = False
                    await client.hset(self.key, k, __import__("json").dumps(v, ensure_ascii=False))

    async def delete(self, addr_id: str) -> None:
        client = await self._r()
        await client.hdel(self.key, addr_id)


@router.get("/address")
async def list_addresses(user_id: str = Depends(get_current_user)):
    """收货地址列表。"""
    store = AddressStore(user_id)
    items = await store.get_all()
    return ok({"items": list(items.values())})


@router.post("/address")
async def create_address(
    name: str,
    mobile: str,
    province: str,
    city: str,
    district: str,
    address: str,
    is_default: bool = False,
    user_id: str = Depends(get_current_user),
):
    """添加收货地址。"""
    if not all([name, mobile, province, city, district, address]):
        return fail(Err.PARAM_ERROR, "地址信息不完整")
    addr_id = f"addr_{uuid.uuid4().hex[:12]}"
    data = {
        "id": addr_id,
        "name": name,
        "mobile": mobile,
        "province": province,
        "city": city,
        "district": district,
        "address": address,
        "is_default": is_default,
    }
    store = AddressStore(user_id)
    await store.save(addr_id, data)
    return ok({"id": addr_id})


@router.put("/address/{addr_id}")
async def update_address(
    addr_id: str,
    name: str = "",
    mobile: str = "",
    province: str = "",
    city: str = "",
    district: str = "",
    address: str = "",
    is_default: bool = False,
    user_id: str = Depends(get_current_user),
):
    """更新收货地址。"""
    store = AddressStore(user_id)
    existing = await store.get(addr_id)
    if not existing:
        return fail(Err.PARAM_ERROR, "地址不存在")
    data = {
        "id": addr_id,
        "name": name or existing.get("name", ""),
        "mobile": mobile or existing.get("mobile", ""),
        "province": province or existing.get("province", ""),
        "city": city or existing.get("city", ""),
        "district": district or existing.get("district", ""),
        "address": address or existing.get("address", ""),
        "is_default": is_default,
    }
    await store.save(addr_id, data)
    return ok()


@router.delete("/address/{addr_id}")
async def delete_address(
    addr_id: str,
    user_id: str = Depends(get_current_user),
):
    """删除收货地址。"""
    store = AddressStore(user_id)
    await store.delete(addr_id)
    return ok()
