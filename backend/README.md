# intimoi-backend

intimoi 小程序后端，基于 FastAPI + WDT SDK。

## 环境

- Python 3.10+
- FastAPI
- Uvicorn
- Redis（购物车会话存储）
- httpx（WDT HTTP 调用）

## 本地运行

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 目录结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 入口
│   ├── config.py        # 配置（从环境变量读取）
│   ├── api/
│   │   ├── __init__.py
│   │   ├── products.py  # 商品接口
│   │   ├── cart.py      # 购物车接口
│   │   ├── orders.py    # 订单接口
│   │   ├── logistics.py # 物流接口
│   │   ├── refund.py    # 售后接口
│   │   ├── auth.py      # 登录接口
│   │   ├── address.py   # 收货地址接口
│   │   └── user.py      # 用户信息接口
│   ├── core/
│   │   ├── __init__.py
│   │   ├── wdt.py       # WDT SDK 封装
│   │   ├── redis.py     # Redis 客户端
│   │   └── security.py  # JWT / 签名
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── address.py
│   └── schemas/
│       ├── __init__.py
│       └── response.py  # 统一响应格式
├── tests/
│   ├── __init__.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
├── requirements.txt
└── .env.example
```

## API 基础路径

`/api`
