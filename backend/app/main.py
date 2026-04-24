"""FastAPI 应用入口。"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    products,
    cart,
    orders,
    logistics,
    refund,
    auth,
    address,
    user,
)
from app.core.redis_ import RedisClient

app = FastAPI(title="intimoi API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api", tags=["认证"])
app.include_router(products.router, prefix="/api", tags=["商品"])
app.include_router(cart.router, prefix="/api", tags=["购物车"])
app.include_router(orders.router, prefix="/api", tags=["订单"])
app.include_router(logistics.router, prefix="/api", tags=["物流"])
app.include_router(refund.router, prefix="/api", tags=["售后"])
app.include_router(address.router, prefix="/api", tags=["地址"])
app.include_router(user.router, prefix="/api", tags=["用户"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("shutdown")
async def shutdown():
    await RedisClient.close()
