"""API v1 router."""
from fastapi import APIRouter
from app.api.v1 import member, cart, goods, favorites, address, wdt

router = APIRouter()

router.include_router(member.router, prefix="/member", tags=["会员"])
router.include_router(cart.router, prefix="/cart", tags=["购物车"])
router.include_router(goods.router, prefix="/goods", tags=["商品"])
router.include_router(favorites.router, prefix="/favorites", tags=["收藏"])
router.include_router(address.router, prefix="/addresses", tags=["收货地址"])
router.include_router(wdt.router, prefix="/wdt", tags=["WDT直通接口"])
