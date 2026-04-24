# intimoi 小程序 API 契约

> 文档版本：v1.1
> 更新日期：2026-04-24
> 更新说明：
> - v1.1：商品仅拉取（不做推送）| 删除积分系统 | 生产地址留空

---

## 一、核心变更说明

### 1.1 商品仅拉取，不做推送

小程序商品数据来源为 WDT 旺店通系统，**仅从 WDT 拉取**，不向 WDT 推送商品。

| 方向 | 说明 |
|---|---|
| 拉取（✅） | 小程序 → 后端 → WDT：查询商品列表、库存、规格 |
| 推送（❌） | ~~小程序 → 后端 → WDT：新建/编辑商品~~ 已废弃 |

小程序侧只需关注**商品展示**（列表、详情、库存），商品录入和管理在 WDT 侧完成。

### 1.2 删除积分系统

本项目**不使用积分、成长值、会员积分等任何积分体系**。相关字段和接口均不涉及。

### 1.3 生产地址留空

订单提交时，**不向用户展示仓库/工厂地址**。收货地址仅含用户自己的配送信息，由用户在小程序内添加管理。

---

## 二、系统边界

```
微信小程序（前端）
    │
    ▼
后端 API（本契约约定）
    │
    ├──► WDT 旺店通（商品拉取 / 订单推送 / 订单查询）
    └──► 微信支付（支付下单 / 支付查询）
```

**注**：小程序前端调用后端 HTTPS API，后端聚合 WDT 接口和数据，不做前后端直连 WDT。

---

## 三、接口列表

| # | 接口 | 方向 | 说明 |
|---|---|---|---|
| 1 | `GET /api/products` | 小程序→后端 | 商品列表（分页、筛选） |
| 2 | `GET /api/products/:id` | 小程序→后端 | 商品详情（含规格、库存） |
| 3 | `POST /api/cart` | 小程序→后端 | 添加购物车 |
| 4 | `GET /api/cart` | 小程序→后端 | 获取购物车 |
| 5 | `PUT /api/cart/:item_id` | 小程序→后端 | 更新购物车数量 |
| 6 | `DELETE /api/cart/:item_id` | 小程序→后端 | 删除购物车项 |
| 7 | `POST /api/orders` | 小程序→后端 | 提交订单（推送至 WDT） |
| 8 | `GET /api/orders` | 小程序→后端 | 订单列表（从 WDT 查询） |
| 9 | `GET /api/orders/:id` | 小程序→后端 | 订单详情 |
| 10 | `POST /api/orders/:id/cancel` | 小程序→后端 | 取消订单 |
| 11 | `GET /api/logistics/:no` | 小程序→后端 | 物流查询 |
| 12 | `POST /api/refund` | 小程序→后端 | 申请售后 |
| 13 | `GET /api/refund` | 小程序→后端 | 售后列表 |
| 14 | `POST /api/auth/login` | 小程序→后端 | 微信登录 |
| 15 | `GET /api/address` | 小程序→后端 | 收货地址列表 |
| 16 | `POST /api/address` | 小程序→后端 | 添加收货地址 |
| 17 | `PUT /api/address/:id` | 小程序→后端 | 更新收货地址 |
| 18 | `DELETE /api/address/:id` | 小程序→后端 | 删除收货地址 |
| 19 | `GET /api/user/profile` | 小程序→后端 | 用户信息 |

---

## 四、接口详情

---

### 4.1 商品接口

#### `GET /api/products` — 商品列表

**Query 参数**：

| 参数 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| `page` | int | 否 | 页码，从 1 开始 | `1` |
| `page_size` | int | 否 | 每页条数，默认 20 | `20` |
| `category_id` | int | 否 | 一级类目 ID | `3` |
| `keyword` | string | 否 | 搜索关键词 | `精华液` |
| `sort` | string | 否 | 排序：`default`/`price_asc`/`price_desc` | `price_asc` |

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "18344",
        "name": "精华液 30ml",
        "subtitle": "修护肌肤屏障",
        "price": 1280,
        "original_price": 1680,
        "image": "https://cdn.example.com/products/18344/cover.jpg",
        "stock": 50,
        "stock_status": "sufficient"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 128,
      "has_more": true
    }
  }
}
```

**状态说明**：
- `sufficient`：库存充足
- `low`：库存紧张（低于阈值，显示警示色 `#B88B4A`）

---

#### `GET /api/products/:id` — 商品详情

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "18344",
    "name": "精华液 30ml",
    "subtitle": "修护肌肤屏障",
    "price": 1280,
    "original_price": 1680,
    "images": [
      "https://cdn.example.com/products/18344/1.jpg",
      "https://cdn.example.com/products/18344/2.jpg"
    ],
    "stock": 50,
    "stock_status": "sufficient",
    "specs": [
      {
        "spec_id": "18656",
        "spec_name": "黑色",
        "price": 1280,
        "stock": 30
      },
      {
        "spec_id": "18657",
        "spec_name": "白色",
        "price": 1280,
        "stock": 20
      }
    ],
    "detail_html": "<p>商品详情图文...</p>"
  }
}
```

**说明**：
- `specs` 为规格列表（如颜色/尺码），由 WDT `goods_no` / `spec_id` 映射
- `detail_html` 为富文本商品详情，由 WDT 回传
- **无积分字段**

---

### 4.2 购物车接口

#### `POST /api/cart` — 添加购物车

**请求**：

```json
{
  "spec_id": "18656",
  "num": 1
}
```

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "cart_item_id": "ci_xxx",
    "total_items": 3
  }
}
```

---

#### `GET /api/cart` — 获取购物车

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "cart_item_id": "ci_xxx",
        "spec_id": "18656",
        "goods_name": "精华液 30ml",
        "spec_name": "黑色",
        "price": 1280,
        "num": 1,
        "image": "https://cdn.example.com/products/18344/cover.jpg",
        "stock_status": "sufficient",
        "checked": true
      }
    ],
    "total_amount": 1280
  }
}
```

**说明**：
- 购物车数据后端暂存 Redis（用户登录后持久化）
- **无积分、积分抵扣字段**

---

#### `PUT /api/cart/:item_id` — 更新数量

**请求**：

```json
{
  "num": 2
}
```

---

#### `DELETE /api/cart/:item_id` — 删除购物车项

**响应**：

```json
{
  "code": 0,
  "message": "success"
}
```

---

### 4.3 订单接口

#### `POST /api/orders` — 提交订单（推送至 WDT）

**请求**：

```json
{
  "address_id": "addr_xxx",
  "cart_item_ids": ["ci_xxx", "ci_yyy"],
  "remark": "请发圆通快递",
  "coupon_id": null
}
```

**后端处理**：

1. 读取收货地址
2. 查询商品实时价格和库存（从 WDT）
3. 组装 `trade_push.php` 参数，推送至 WDT
4. 清除已提交的购物车项
5. 返回订单号

**请求至 WDT**（`trade_push.php`）：

| 参数 | 说明 | 示例 |
|---|---|---|
| `shop_id` | 店铺编号 | `23` |
| `trade_list`（JSON） | 订单列表 | — |
| `├ tid` | 外部订单号 | `INTIMOI20260425001` |
| `├ trade_status` | 订单状态 | `20`（已付款待发货） |
| `├ pay_status` | 支付状态 | `1`（已支付） |
| `├ delivery_term` | 发货条件 | `2`（款到发货） |
| `├ trade_time` | 下单时间 | `2026-04-25 10:00:00` |
| `├ buyer_nick` | 买家昵称 | `intimoi_user` |
| `├ receiver_mobile` | 收货人手机 | `176xxxx1203` |
| `├ receiver_name` | 收货人姓名 | `张三` |
| `├ receiver_province` | 收货省份 | `广东省` |
| `├ receiver_city` | 收货城市 | `深圳市` |
| `├ receiver_district` | 收货区县 | `南山区` |
| `├ receiver_address` | 详细地址 | `科技园xxx路xx号` |
| `├ logistics_type` | 物流方式 | `4`（快递） |
| `├ post_amount` | 运费 | `0` |
| `├ paid` | 已支付金额 | `1280` |
| `└ order_list`（JSON） | 商品明细 | — |
| ` ├ oid` | 子订单号 | `INTIMOI20260425001-1` |
| `　 ├ goods_id` | 商品ID | `18344` |
| `　 ├ spec_id` | 规格ID | `18656` |
| `　 ├ goods_no` | 商品编号 | `GH001` |
| `　 ├ goods_name` | 商品名 | `精华液 30ml` |
| `　 ├ spec_no` | 规格编号 | `GH001-BLK` |
| `　 ├ spec_name` | 规格名 | `黑色` |
| `　 ├ price` | 单价 | `1280` |
| `　 ├ num` | 数量 | `1` |
| `　 ├ discount` | 折扣 | `0` |
| `　 └ refund_status` | 退款状态 | `0`（无退款） |

**说明**：
- **生产地址留空**：不向用户展示仓库地址，仓库地址仅在 WDT 内部配置
- **无积分抵扣**：paid = 商品总价（无积分抵扣逻辑）
- **无积分字段**：订单回传不含任何积分相关字段

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": "INTIMOI20260425001",
    "amount": 1280,
    "pay_url": "https://wx.tenpay.com/..."
  }
}
```

---

#### `GET /api/orders` — 订单列表

**Query 参数**：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `status` | string | 否 | 订单状态筛选：`pending`/`paid`/`shipped`/`completed`/`refund` |
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页条数，默认 20 |

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "order_id": "INTIMOI20260425001",
        "trade_status": 20,
        "pay_status": 1,
        "paid": 1280,
        "trade_time": "2026-04-25 10:00:00",
        "goods_thumbnails": [
          "https://cdn.example.com/...",
          "https://cdn.example.com/..."
        ],
        "goods_count": 2
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 5,
      "has_more": false
    }
  }
}
```

**状态映射（WDT → 小程序）**：

| trade_status | pay_status | 含义 | 小程序显示 |
|---|---|---|---|
| 10 | 0 | 未付款 | 待付款 |
| 20 | 1 | 已付款 | 待发货 |
| 30 | 1 | 已发货 | 已发货 |
| 40 | 1 | 已完成 | 已完成 |
| — | — | 退款中 | 售后中 |

**说明**：后端调用 WDT `trade_query.php`，按时间范围查询用户订单。

---

#### `GET /api/orders/:id` — 订单详情

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": "INTIMOI20260425001",
    "trade_status": 20,
    "pay_status": 1,
    "paid": 1280,
    "post_amount": 0,
    "trade_time": "2026-04-25 10:00:00",
    "pay_time": "2026-04-25 10:01:00",
    "receiver": {
      "name": "张三",
      "mobile": "176xxxx1203",
      "province": "广东省",
      "city": "深圳市",
      "district": "南山区",
      "address": "科技园xxx路xx号"
    },
    "logistics": {
      "company": "圆通快递",
      "tracking_no": "YT1234567890"
    },
    "goods": [
      {
        "oid": "INTIMOI20260425001-1",
        "goods_name": "精华液 30ml",
        "spec_name": "黑色",
        "price": 1280,
        "num": 1,
        "image": "https://cdn.example.com/..."
      }
    ],
    "remark": "请发圆通快递"
  }
}
```

**说明**：**无生产地址字段**，仅含收货人地址。

---

#### `POST /api/orders/:id/cancel` — 取消订单

**说明**：调用 WDT 取消接口（或标记订单状态）。WDT 退款由原路退回。

---

### 4.4 物流接口

#### `GET /api/logistics/:tracking_no` — 物流查询

**说明**：调用快递100或快递公司官方接口（参考 WDT `logistics_sync`）。

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "company": "圆通快递",
    "tracking_no": "YT1234567890",
    "nodes": [
      {
        "time": "2026-04-26 08:30:00",
        "status": "已发出",
        "location": "深圳转运中心",
        "is_latest": true
      },
      {
        "time": "2026-04-25 20:00:00",
        "status": "已揽收",
        "location": "深圳市南山区",
        "is_latest": false
      }
    ]
  }
}
```

---

### 4.5 售后接口

#### `POST /api/refund` — 申请售后

**请求**：

```json
{
  "order_id": "INTIMOI20260425001",
  "oid": "INTIMOI20260425001-1",
  "type": "refund",
  "reason": "商品损坏",
  "description": "收到时包装已破损",
  "images": ["https://cdn.example.com/refund/1.jpg"]
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `type` | string | `refund`=仅退款 / `return`=退货退款 |
| `images` | string[] | 凭证图片 URLs |

**说明**：后端调用 WDT 退款接口，记录售后申请。

---

### 4.6 用户接口

#### `POST /api/auth/login` — 微信登录

**请求**：

```json
{
  "code": "微信授权code"
}
```

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": "user_xxx",
      "nickname": "intimoi_user",
      "avatar": "https://cdn.example.com/avatar.jpg",
      "phone": "176xxxx1203"
    }
  }
}
```

**说明**：
- 后端用 code 换取 openid/session_key，向微信后台上报
- 返回 JWT token 作为身份凭证
- **无积分、会员积分字段**

---

#### `GET /api/user/profile` — 用户信息

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "user_xxx",
    "nickname": "intimoi_user",
    "avatar": "https://cdn.example.com/avatar.jpg",
    "phone": "176xxxx1203"
  }
}
```

**说明**：**无积分、会员等级积分字段**。

---

### 4.7 收货地址接口

#### 地址列表 `GET /api/address`

**响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "addr_xxx",
        "name": "张三",
        "mobile": "176xxxx1203",
        "province": "广东省",
        "city": "深圳市",
        "district": "南山区",
        "address": "科技园xxx路xx号",
        "is_default": true
      }
    ]
  }
}
```

#### 添加地址 `POST /api/address`

**请求**：

```json
{
  "name": "张三",
  "mobile": "176xxxx1203",
  "province": "广东省",
  "city": "深圳市",
  "district": "南山区",
  "address": "科技园xxx路xx号",
  "is_default": true
}
```

#### 删除地址 `DELETE /api/address/:id`

---

## 五、通用响应格式

所有接口统一响应格式：

```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

| code | 说明 |
|---|---|
| `0` | 成功 |
| `1001` | 参数错误 |
| `1002` | 签名错误 |
| `2001` | 库存不足 |
| `2002` | 商品不存在 |
| `3001` | 订单不存在 |
| `3002` | 订单状态不允许此操作 |
| `4001` | WDT 接口调用失败 |
| `5001` | 未登录或登录已过期 |

---

## 六、字段汇总（不含积分）

### 订单字段（含 WDT 回传）

| 字段 | 存在 | 类型 | 说明 |
|---|---|---|---|
| `tid` | ✅ | string | 外部订单号 |
| `trade_status` | ✅ | int | 订单状态 |
| `pay_status` | ✅ | int | 支付状态 |
| `paid` | ✅ | decimal | 已支付金额 |
| `post_amount` | ✅ | decimal | 运费 |
| `receiver_*` | ✅ | string | 收货人信息 |
| `logistics_type` | ✅ | int | 物流方式 |
| `order_list` | ✅ | array | 商品明细 |
| `goods_id/spec_id/price/num` | ✅ | — | 商品信息 |
| `discount` | ✅ | decimal | 折扣 |
| `refund_status` | ✅ | int | 退款状态 |
| **积分相关** | **❌ 已删除** | — | — |

### 用户字段

| 字段 | 存在 | 说明 |
|---|---|---|
| id | ✅ | 用户ID |
| nickname | ✅ | 昵称 |
| avatar | ✅ | 头像 |
| phone | ✅ | 手机号 |
| **积分/成长值** | **❌ 已删除** | — |

---

## 七、WDT 接口对应关系

| 小程序接口 | WDT 接口 | 方向 |
|---|---|---|
| `GET /api/products` | WDT 商品查询 | 后端→WDT（拉取） |
| `GET /api/products/:id` | WDT 商品查询 | 后端→WDT（拉取） |
| `POST /api/orders` | `trade_push.php` | 后端→WDT（推送） |
| `GET /api/orders` | `trade_query.php` | 后端→WDT（拉取） |
| `GET /api/orders/:id` | `trade_query.php` | 后端→WDT（拉取） |
| `GET /api/logistics/:no` | 快递100/物流接口 | 后端→第三方 |
| `POST /api/refund` | WDT refund 接口 | 后端→WDT（推送） |

**商品管理（新增/编辑/上下架）：WDT 管理后台操作，不通过本 API**
