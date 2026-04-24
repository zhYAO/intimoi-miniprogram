# intimoi 小程序 API 契约文档

> 版本：v1.1.0
> 日期：2026-04-24
> 状态：草稿（已按CEO反馈更新）

---

## 概述

intimoi 小程序是连接微信前端与 WDT 旺店通 ERP 的桥接层。

- **定位**：小程序调用本后端 API，后端调用 WDT 接口，将 WDT 的响应结构化后返回
- **编码**：UTF-8，请求/响应均为 JSON，字符编码 `application/x-www-form-urlencoded;charset=UTF-8`
- **签名**：WDT 签名算法由 WdtClient 封装（`length-key:length-value;...;appsecret` → MD5 → hex lowercase）

### WDT 基础信息

| 环境 | Base URL |
|------|-----------|
| 测试 | `https://openapitest.huice.com/openapi/` |
| 正式 | `（接入时配置）` |

> ⚠️ 正式环境 WDT Base URL 待 WDT 方提供后配置至 `wdt_config` 表。

---

## 目录

1. [WDT 直通接口](#1-wdt-直通接口)
   - 1.1 订单推送（创建原始订单）
   - 1.2 订单查询
   - 1.3 称重申传
2. [业务接口](#2-业务接口)
   - 2.1 会员
   - 2.2 购物车
   - 2.3 商品
   - 2.4 收藏
3. [通用约定](#3-通用约定)

---

## 1. WDT 直通接口

> 以下接口是 WDT 现有能力的透传，后端不做业务逻辑，仅做参数透传和响应转发。

### 1.1 订单推送（创建原始订单）

将微信用户确认的订单推送至 WDT 生成正式销售订单。

**路径**：`POST /api/v1/wdt/trade/push`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| shop_id | string | ✅ | 店铺编号，对应 WDT 店铺 |
| trade_list | string (JSON) | ✅ | 订单列表 JSON 数组，见下方结构 |

**trade_list 子结构**（每个元素即一笔订单）：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| tid | string | ✅ | 订单号（小程序生成，需保证唯一） |
| trade_status | int | ✅ | 订单状态；`20`=已付款待发货 |
| pay_status | string | ✅ | 支付状态；`1`=已支付 |
| delivery_term | int | ✅ | 发货条件；`2`=款到发货 |
| trade_time | string | ✅ | 下单时间，格式 `YYYY-MM-DD HH:MM:SS` |
| buyer_nick | string | ✅ | 买家昵称（微信昵称） |
| receiver_mobile | string | ✅ | 收货人手机号 |
| receiver_name | string | ✅ | 收货人姓名 |
| receiver_province | string | ✅ | 收货省份 |
| receiver_city | string | ✅ | 收货城市 |
| receiver_district | string | ✅ | 收货区县 |
| receiver_address | string | ✅ | 详细地址 |
| logistics_type | int | ✅ | 物流类型；`4`=快递 |
| post_amount | number | ✅ | 运费（单位：元） |
| cod_amount | number | ✅ | 货到付款金额（款到发货填 `0`） |
| paid | number | ✅ | 已支付金额 |
| order_list | array | ✅ | 订单明细列表 |

**order_list 子结构**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| oid | string | ✅ | 子订单号（小程序生成，需唯一） |
| num | int | ✅ | 购买数量 |
| price | number | ✅ | 商品单价 |
| status | int | ✅ | 订单项状态；`30`=已付款 |
| refund_status | int | ✅ | 退款状态；`0`=无退款 |
| goods_id | string | ✅ | WDT 商品 ID |
| spec_id | string | ✅ | WDT 规格 ID |
| goods_no | string | ✅ | 商品货号 |
| goods_name | string | ✅ | 商品名称 |
| spec_no | string | ✅ | 规格编码 |
| spec_name | string | ✅ | 规格名称（如颜色/尺码） |
| discount | number | ✅ | 优惠金额 |
| adjust_amount | number | ✅ | 调整金额（一般填 `0`） |
| share_discount | number | ✅ | 分摊优惠（一般填 `0`） |

**请求示例**：

```json
{
  "shop_id": "23",
  "trade_list": "[{\"tid\":\"WX202604240001\",\"trade_status\":20,\"pay_status\":\"1\",\"delivery_term\":2,\"trade_time\":\"2026-04-24 15:00:00\",\"buyer_nick\":\"小鱼\",\"receiver_mobile\":\"13800138000\",\"receiver_name\":\"李晓\",\"receiver_province\":\"上海市\",\"receiver_city\":\"上海市\",\"receiver_district\":\"浦东新区\",\"receiver_address\":\"东方路123号\",\"logistics_type\":4,\"post_amount\":0,\"cod_amount\":0,\"paid\":1280,\"order_list\":[{\"oid\":\"WX202604240001-1\",\"num\":1,\"price\":1280,\"status\":30,\"refund_status\":0,\"goods_id\":\"18344\",\"spec_id\":\"18656\",\"goods_no\":\"GH001\",\"goods_name\":\"精粹修护精华液\",\"spec_no\":\"GHSKU001\",\"spec_name\":\"30ml\",\"discount\":0,\"adjust_amount\":0,\"share_discount\":0}]}]"
}
```

**响应参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码；`0`=成功 |
| message | string | 状态信息 |
| data | object | 返回数据 |

**响应示例（成功）**：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "success_count": 1,
    "fail_count": 0,
    "results": [
      { "tid": "WX202604240001", "wdt_tid": "AT202604240001", "status": "success" }
    ]
  }
}
```

**响应示例（失败）**：

```json
{
  "code": 1001,
  "message": "WDT接口调用失败",
  "data": {
    "error_code": "TRADE_PUSH_ERROR",
    "wdt_response": "..."
  }
}
```

---

### 1.2 订单查询

按时间范围查询 WDT 订单列表。

**路径**：`POST /api/v1/wdt/trade/query`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| start_time | string | ✅ | 开始时间，格式 `YYYY-MM-DD HH:MM:SS` |
| end_time | string | ✅ | 结束时间，格式 `YYYY-MM-DD HH:MM:SS` |
| page_no | int | ✅ | 页码，从 `0` 开始 |
| page_size | int | ✅ | 每页条数（建议 ≤100） |

**请求示例**：

```json
{
  "start_time": "2026-04-24 00:00:00",
  "end_time": "2026-04-24 23:59:59",
  "page_no": 0,
  "page_size": 20
}
```

**响应参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码；`0`=成功 |
| message | string | 状态信息 |
| data | object | 返回数据 |

**响应示例（成功）**：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "total": 100,
    "page_no": 0,
    "page_size": 20,
    "orders": [
      {
        "tid": "AT202604240001",
        "trade_status": 20,
        "pay_status": "1",
        "trade_time": "2026-04-24 15:00:00",
        "buyer_nick": "小鱼",
        "receiver_mobile": "13800138000",
        "receiver_name": "李晓",
        "receiver_province": "上海市",
        "receiver_city": "上海市",
        "receiver_district": "浦东新区",
        "receiver_address": "东方路123号",
        "logistics_type": 4,
        "post_amount": 0,
        "paid": 1280,
        "order_list": [
          {
            "oid": "WX202604240001-1",
            "goods_name": "精粹修护精华液",
            "spec_name": "30ml",
            "num": 1,
            "price": 1280
          }
        ]
      }
    ]
  }
}
```

---

### 1.3 称重申传

将发货重量回传至 WDT，用于计算运费和物流追踪。

**路径**：`POST /api/v1/wdt/weight/push`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| logistics_no | string | ✅ | 物流单号 |
| weight | number | ✅ | 重量（单位：kg） |
| is_setting | int | ✅ | 是否覆盖；`0`=首次录入，`1`=覆盖 |

**请求示例**：

```json
{
  "logistics_no": "JT12121212122",
  "weight": 0.5,
  "is_setting": 0
}
```

**响应示例**：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "logistics_no": "JT12121212122",
    "weight": 0.5,
    "status": "success"
  }
}
```

---

## 2. 业务接口

> 以下接口 WDT 不提供，由 intimoi 后端自主实现。

### 2.1 会员

#### 2.1.1 微信授权登录

通过微信小程序 code 换取 session。

**路径**：`POST /api/v1/member/login`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | string | ✅ | 微信小程序 wx.login() 获取的 code |

**响应参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 状态信息 |
| data.open_id | string | 微信 OpenID |
| data.session_key | string | Session Key（需安全存储） |
| data.token | string | 本后端颁发的访问令牌 |
| data.member_id | int | 会员 ID（首次登录自动创建） |

**响应示例**：

```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "open_id": "oXXXXXXXXXXXXXXXXX",
    "session_key": "xxxxxxx",
    "token": "eyJhbGciOiJIUzI1NiJ9...",
    "member_id": 10001
  }
}
```

---

#### 2.1.2 获取会员信息

**路径**：`GET /api/v1/member/info`

**请求 Header**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Authorization | string | ✅ | Bearer {token} |

**响应参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 状态信息 |
| data.id | int | 会员 ID |
| data.open_id | string | 微信 OpenID |
| data.nickname | string | 昵称 |
| data.avatar_url | string | 头像 URL |
| data.phone | string | 手机号 |
| data.level | int | 会员等级（1=普通，2=银卡，3=金卡） |
| data.created_at | string | 注册时间 |

**响应示例**：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "id": 10001,
    "open_id": "oXXXXXXXXXXXXXXXXX",
    "nickname": "小鱼",
    "avatar_url": "https://example.com/avatar/10001.jpg",
    "phone": "138****8000",
    "level": 2,
    "created_at": "2026-01-15 10:30:00"
  }
}
```

---

#### 2.1.3 更新会员信息

**路径**：`PUT /api/v1/member/info`

**请求 Header**：`Authorization: Bearer {token}`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| nickname | string | 否 | 昵称 |
| avatar_url | string | 否 | 头像 URL |
| phone | string | 否 | 手机号 |

**响应示例**：

```json
{
  "code": 0,
  "message": "更新成功",
  "data": null
}
```

---

### 2.2 购物车

#### 2.2.1 获取购物车列表

**路径**：`GET /api/v1/cart`

**请求 Header**：`Authorization: Bearer {token}`

**响应参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 状态信息 |
| data.items | array | 购物车明细列表 |
| data.total_amount | number | 购物车总价（未扣优惠） |

**items 子结构**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 购物车项 ID |
| goods_id | string | WDT 商品 ID |
| spec_id | string | WDT 规格 ID |
| goods_name | string | 商品名称 |
| spec_name | string | 规格名称 |
| price | number | 单价 |
| num | int | 数量 |
| stock | int | 当前库存 |
| thumbnail | string | 商品缩略图 |
| selected | boolean | 是否选中结算 |

**响应示例**：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "items": [
      {
        "id": 1,
        "goods_id": "18344",
        "spec_id": "18656",
        "goods_name": "精粹修护精华液",
        "spec_name": "30ml",
        "price": 1280,
        "num": 1,
        "stock": 99,
        "thumbnail": "https://example.com/goods/18344/thumb.jpg",
        "selected": true
      }
    ],
    "total_amount": 1280
  }
}
```

---

#### 2.2.2 添加商品至购物车

**路径**：`POST /api/v1/cart`

**请求 Header**：`Authorization: Bearer {token}`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| goods_id | string | ✅ | WDT 商品 ID |
| spec_id | string | ✅ | WDT 规格 ID |
| num | int | ✅ | 数量，默认 `1` |

**响应示例**：

```json
{
  "code": 0,
  "message": "已加入购物车",
  "data": {
    "cart_item_id": 5,
    "cart_count": 3
  }
}
```

---

#### 2.2.3 更新购物车商品数量

**路径**：`PUT /api/v1/cart/{item_id}`

**请求 Header**：`Authorization: Bearer {token}`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| num | int | ✅ | 更新后数量（传 `0` 删除） |

**响应示例**：

```json
{
  "code": 0,
  "message": "更新成功",
  "data": null
}
```

---

#### 2.2.4 删除购物车商品

**路径**：`DELETE /api/v1/cart/{item_id}`

**请求 Header**：`Authorization: Bearer {token}`

**响应示例**：

```json
{
  "code": 0,
  "message": "已删除",
  "data": null
}
```

---

#### 2.2.5 全选/取消全选购物车

**路径**：`PUT /api/v1/cart/select-all`

**请求 Header**：`Authorization: Bearer {token}`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| selected | boolean | ✅ | `true`=全选，`false`=取消全选 |

**响应示例**：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": null
}
```

---

### 2.3 商品

#### 2.3.1 获取商品列表（微页面用）

**路径**：`GET /api/v1/goods`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| category_id | int | 否 | 分类 ID |
| page | int | 否 | 页码，默认 `0` |
| page_size | int | 否 | 每页条数，默认 `20` |
| sort | string | 否 | 排序：`default`/`price_asc`/`price_desc`/`sales` |

**响应参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 状态信息 |
| data.items | array | 商品列表 |
| data.total | int | 总条数 |

**items 子结构**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| goods_id | string | WDT 商品 ID |
| goods_name | string | 商品名称 |
| price | number | 售价 |
| original_price | number | 划线价 |
| thumbnail | string | 缩略图 |
| sales | int | 销量 |

**响应示例**：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "items": [
      {
        "goods_id": "18344",
        "goods_name": "精粹修护精华液",
        "price": 1280,
        "original_price": 1680,
        "thumbnail": "https://example.com/goods/18344/thumb.jpg",
        "sales": 328
      }
    ],
    "total": 56
  }
}
```

---

#### 2.3.2 获取商品详情

**路径**：`GET /api/v1/goods/{goods_id}`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| goods_id | string | ✅ | WDT 商品 ID |

**响应参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 状态信息 |
| data.goods_id | string | WDT 商品 ID |
| data.goods_name | string | 商品名称 |
| data.price | number | 售价 |
| data.original_price | number | 划线价 |
| data.description | string | 商品详情（富文本） |
| data.images | array | 商品图片列表 |
| data.specs | array | 规格列表 |
| data.stock | int | 总库存 |
| data.sales | int | 销量 |

**响应示例**：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "goods_id": "18344",
    "goods_name": "精粹修护精华液",
    "price": 1280,
    "original_price": 1680,
    "description": "<p>富含高浓度精粹成分，专注修护肌肤屏障。</p>",
    "images": [
      "https://example.com/goods/18344/img1.jpg",
      "https://example.com/goods/18344/img2.jpg"
    ],
    "specs": [
      { "spec_id": "18656", "spec_name": "30ml", "stock": 99, "price": 1280 },
      { "spec_id": "18657", "spec_name": "50ml", "stock": 50, "price": 1980 }
    ],
    "stock": 149,
    "sales": 328
  }
}
```

---

### 2.4 收藏

#### 2.4.1 获取收藏列表

**路径**：`GET /api/v1/favorites`

**请求 Header**：`Authorization: Bearer {token}`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认 `0` |
| page_size | int | 否 | 每页条数，默认 `20` |

**响应参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 状态信息 |
| data.items | array | 收藏列表 |

**items 子结构**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 收藏 ID |
| goods_id | string | WDT 商品 ID |
| goods_name | string | 商品名称 |
| price | number | 当前售价 |
| thumbnail | string | 缩略图 |
| created_at | string | 收藏时间 |

**响应示例**：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "items": [
      {
        "id": 1,
        "goods_id": "18344",
        "goods_name": "精粹修护精华液",
        "price": 1280,
        "thumbnail": "https://example.com/goods/18344/thumb.jpg",
        "created_at": "2026-04-20 10:00:00"
      }
    ]
  }
}
```

---

#### 2.4.2 添加收藏

**路径**：`POST /api/v1/favorites`

**请求 Header**：`Authorization: Bearer {token}`

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| goods_id | string | ✅ | WDT 商品 ID |

**响应示例**：

```json
{
  "code": 0,
  "message": "已收藏",
  "data": null
}
```

---

#### 2.4.3 取消收藏

**路径**：`DELETE /api/v1/favorites/{goods_id}`

**请求 Header**：`Authorization: Bearer {token}`

**响应示例**：

```json
{
  "code": 0,
  "message": "已取消收藏",
  "data": null
}
```

---

## 3. 通用约定

### 3.1 统一响应格式

所有接口响应均为 JSON，结构如下：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {}
}
```

### 3.2 状态码定义

| code | 说明 |
|------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未登录或 Token 过期 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 1001 | WDT 接口调用失败 |
| 1002 | WDT 签名校验失败 |
| 1003 | WDT 返回数据解析失败 |
| 500 | 服务器内部错误 |

### 3.3 WDT 签名机制（SDK 封装）

参考 `WdtClient.py` 中的 `signRequest` 方法：

1. 将所有参数（除 `sign` 外）按键名字典序排序
2. 拼接格式：`{key长度}-{key}:{value长度}-{value};...`
3. 拼接 AppSecret
4. 对整体做 MD5，取 hex lowercase

### 3.4 分页约定

- 默认页码从 `0` 开始
- `page_size` 上限 `100`
- 列表类接口返回 `total`、`page_no`、`page_size`

---

## 附录：WDT 接口路由速查

| WDT 接口 | 路由 | 方法 | 说明 |
|----------|------|------|------|
| trade_push.php | /api/v1/wdt/trade/push | POST | 创建订单 |
| trade_query.php | /api/v1/wdt/trade/query | POST | 查询订单 |
| vip_stockout_sales_weight_push.php | /api/v1/wdt/weight/push | POST | 称重申传 |
