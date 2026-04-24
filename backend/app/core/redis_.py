"""Redis 客户端（异步）。"""
import json
import redis.asyncio as redis
from typing import Optional

from app.config import settings


class RedisClient:
    _pool: Optional[redis.ConnectionPool] = None

    @classmethod
    async def get_pool(cls) -> redis.ConnectionPool:
        if cls._pool is None:
            cls._pool = redis.ConnectionPool(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password or None,
                decode_responses=True,
            )
        return cls._pool

    @classmethod
    async def get_client(cls) -> redis.Redis:
        pool = await cls.get_pool()
        return redis.Redis(connection_pool=pool)

    @classmethod
    async def close(cls) -> None:
        if cls._pool is not None:
            await cls._pool.disconnect()
            cls._pool = None


class CartStore:
    """购物车存储（Redis Hash）。"""

    KEY_PREFIX = "cart:"

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.key = f"{self.KEY_PREFIX}{user_id}"

    async def _r(self) -> redis.Redis:
        return await RedisClient.get_client()

    async def get_all(self) -> dict:
        """返回整个购物车 dict。"""
        client = await self._r()
        raw = await client.hgetall(self.key)
        return {k: json.loads(v) for k, v in raw.items()}

    async def add_item(self, spec_id: str, num: int = 1) -> None:
        """添加或增加商品数量。"""
        client = await self._r()
        existing = await client.hget(self.key, spec_id)
        if existing:
            item = json.loads(existing)
            item["num"] += num
        else:
            item = {"spec_id": spec_id, "num": num}
        await client.hset(self.key, spec_id, json.dumps(item, ensure_ascii=False))

    async def update_num(self, spec_id: str, num: int) -> None:
        """更新商品数量。"""
        client = await self._r()
        if num <= 0:
            await client.hdel(self.key, spec_id)
        else:
            await client.hset(
                self.key, spec_id, json.dumps({"spec_id": spec_id, "num": num}, ensure_ascii=False)
            )

    async def remove_item(self, spec_id: str) -> None:
        """删除单个商品。"""
        client = await self._r()
        await client.hdel(self.key, spec_id)

    async def clear(self) -> None:
        """清空购物车。"""
        client = await self._r()
        await client.delete(self.key)

    async def items(self) -> list:
        """返回购物车商品列表。"""
        all_items = await self.get_all()
        return list(all_items.values())

    async def total_items(self) -> int:
        """返回商品项数。"""
        client = await self._r()
        return await client.hlen(self.key)
