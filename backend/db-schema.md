# intimoi 小程序数据库表结构设计

> 版本：v1.1.0
> 日期：2026-04-24
> 数据库：MySQL 8.0+
> 更新说明：v1.1.0 删除积分系统（member_points_log 表及相关接口），生产 WDT 地址留空

---

## 概述

本设计覆盖 intimoi 小程序后端所需的数据表，包括：

- 会员
- 购物车
- 商品（WDT 商品实时拉取缓存 + 微页面用）
- 收藏
- 订单（WDT 订单本地缓存）
- WDT 集成配置

> **关于 WDT 数据同步**：WDT 是外部 ERP 系统，商品/库存等主数据以 WDT 为权威来源。本系统做本地缓存表，字段设计尽量与 WDT 响应结构保持一致，方便后续同步。订单表记录推送历史，避免重复推送。

---

## ER 关系概览

```
member (会员)
  ├── cart (购物车)
  ├── favorites (收藏)
  └── orders (订单)

goods (商品缓存)
  └── goods_spec (规格缓存)
```

---

## 表设计

### 1. member（会员表）

存储通过微信登录的会员基本信息。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 会员 ID |
| open_id | VARCHAR(64) | UNIQUE, NOT NULL | 微信 OpenID |
| session_key | VARCHAR(128) | NULL | 微信 Session Key（仅临时存储） |
| nickname | VARCHAR(64) | NULL | 昵称 |
| avatar_url | VARCHAR(512) | NULL | 头像 URL |
| phone | VARCHAR(20) | UNIQUE, NULL | 手机号 |
| level | TINYINT | NOT NULL, DEFAULT 1 | 会员等级：1=普通，2=银卡，3=金卡 |
| last_login_at | DATETIME | NULL | 最后登录时间 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 注册时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_open_id` ON (`open_id`)
- `idx_phone` ON (`phone`)

---

### 2. cart（购物车表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 购物车项 ID |
| member_id | BIGINT | FK → member.id, NOT NULL | 会员 ID |
| goods_id | VARCHAR(32) | NOT NULL | WDT 商品 ID |
| spec_id | VARCHAR(32) | NOT NULL | WDT 规格 ID |
| num | INT | NOT NULL, DEFAULT 1 | 数量 |
| selected | TINYINT | NOT NULL, DEFAULT 1 | 是否选中结算：0=未选，1=选中 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 加入时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_member_goods_spec` ON (`member_id`, `goods_id`, `spec_id`) — UNIQUE，防止重复加车
- `idx_member_id` ON (`member_id`)

**说明**：
- `goods_id` + `spec_id` 联合唯一索引，支持同一商品不同规格分别加车

---

### 3. goods（商品缓存表）

从 WDT 同步的商品主数据缓存，作为微页面展示的数据源。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 自增 ID |
| goods_id | VARCHAR(32) | UNIQUE, NOT NULL | WDT 商品 ID |
| goods_no | VARCHAR(32) | NULL | 商品货号 |
| goods_name | VARCHAR(256) | NOT NULL | 商品名称 |
| category_id | INT | NULL | 分类 ID |
| price | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | 售价 |
| original_price | DECIMAL(10,2) | NULL | 划线价 |
| description | TEXT | NULL | 商品详情（富文本） |
| images | JSON | NULL | 商品图片列表 |
| sales | INT | NOT NULL, DEFAULT 0 | 销量 |
| is_on_sale | TINYINT | NOT NULL, DEFAULT 1 | 是否上架：0=下架，1=上架 |
| wdt_synced_at | DATETIME | NULL | 最近一次从 WDT 同步的时间 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 首次同步时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_goods_id` ON (`goods_id`)
- `idx_category` ON (`category_id`)
- `idx_is_on_sale` ON (`is_on_sale`)

---

### 4. goods_spec（规格缓存表）

从 WDT 同步的规格数据，与 goods 一对多。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 自增 ID |
| spec_id | VARCHAR(32) | UNIQUE, NOT NULL | WDT 规格 ID |
| goods_id | VARCHAR(32) | FK → goods.goods_id, NOT NULL | WDT 商品 ID |
| spec_no | VARCHAR(32) | NULL | 规格编码 |
| spec_name | VARCHAR(128) | NOT NULL | 规格名称（如"30ml"、"M码"） |
| price | DECIMAL(10,2) | NOT NULL | 规格单价 |
| stock | INT | NOT NULL, DEFAULT 0 | 库存 |
| is_on_sale | TINYINT | NOT NULL, DEFAULT 1 | 是否上架 |
| wdt_synced_at | DATETIME | NULL | 最近一次从 WDT 同步的时间 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 首次同步时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_spec_id` ON (`spec_id`)
- `idx_goods_id` ON (`goods_id`)

---

### 5. favorites（收藏表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 收藏 ID |
| member_id | BIGINT | FK → member.id, NOT NULL | 会员 ID |
| goods_id | VARCHAR(32) | FK → goods.goods_id, NOT NULL | WDT 商品 ID |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 收藏时间 |

**索引**：
- `idx_member_goods` ON (`member_id`, `goods_id`) — UNIQUE，防止重复收藏
- `idx_member_id` ON (`member_id`)

---

### 6. orders（订单表）

本地缓存已推送至 WDT 的订单记录。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 自增 ID |
| order_id | VARCHAR(64) | UNIQUE, NOT NULL | 小程序订单号（对应 WDT tid） |
| wdt_tid | VARCHAR(64) | NULL | WDT 生成的订单号（推送后获得） |
| member_id | BIGINT | FK → member.id, NOT NULL | 会员 ID |
| trade_status | TINYINT | NOT NULL | 订单状态（对应 WDT trade_status） |
| pay_status | VARCHAR(8) | NOT NULL | 支付状态：paid/unpaid |
| logistics_type | TINYINT | NOT NULL | 物流类型 |
| receiver_name | VARCHAR(64) | NOT NULL | 收货人 |
| receiver_mobile | VARCHAR(20) | NOT NULL | 联系电话 |
| receiver_province | VARCHAR(32) | NOT NULL | 省份 |
| receiver_city | VARCHAR(32) | NOT NULL | 城市 |
| receiver_district | VARCHAR(32) | NOT NULL | 区县 |
| receiver_address | VARCHAR(256) | NOT NULL | 详细地址 |
| post_amount | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | 运费 |
| total_amount | DECIMAL(10,2) | NOT NULL | 订单总金额 |
| paid_amount | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | 已支付金额 |
| trade_time | DATETIME | NOT NULL | 下单时间 |
| push_status | TINYINT | NOT NULL, DEFAULT 0 | 推送状态：0=待推送，1=已推送，2=推送失败 |
| push_msg | VARCHAR(256) | NULL | 推送失败原因 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_order_id` ON (`order_id`)
- `idx_member_id` ON (`member_id`)
- `idx_wdt_tid` ON (`wdt_tid`)
- `idx_trade_time` ON (`trade_time`)

---

### 7. order_items（订单明细表）

与 orders 一对多。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 自增 ID |
| order_id | VARCHAR(64) | FK → orders.order_id, NOT NULL | 主订单号 |
| sub_order_id | VARCHAR(64) | UNIQUE, NOT NULL | 子订单号（对应 WDT oid） |
| goods_id | VARCHAR(32) | NOT NULL | WDT 商品 ID |
| spec_id | VARCHAR(32) | NOT NULL | WDT 规格 ID |
| goods_name | VARCHAR(256) | NOT NULL | 商品名称 |
| spec_name | VARCHAR(128) | NOT NULL | 规格名称 |
| price | DECIMAL(10,2) | NOT NULL | 单价 |
| num | INT | NOT NULL | 数量 |
| refund_status | TINYINT | NOT NULL, DEFAULT 0 | 退款状态：0=无退款，1=部分退款，2=全部退款 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**索引**：
- `idx_order_id` ON (`order_id`)
- `idx_sub_order_id` ON (`sub_order_id`)

---

### 8. wdt_config（WDT 配置表）

存储 WDT 账号配置信息（加密存储 AppSecret）。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 配置 ID |
| env | ENUM('test','prod') | UNIQUE, NOT NULL | 环境：测试/正式 |
| appkey | VARCHAR(64) | NOT NULL | WDT AppKey |
| appsecret | VARCHAR(128) | NOT NULL | WDT AppSecret（建议加密存储） |
| sid | VARCHAR(32) | NOT NULL | WDT SID |
| base_url | VARCHAR(128) | NOT NULL | API Base URL |
| is_active | TINYINT | NOT NULL, DEFAULT 1 | 是否启用 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

---

### 9. category（商品分类表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 分类 ID |
| name | VARCHAR(64) | NOT NULL | 分类名称 |
| parent_id | BIGINT | FK → category.id, NULL | 父分类 ID（顶级为 NULL） |
| sort | INT | NOT NULL, DEFAULT 0 | 排序（越小越靠前） |
| is_active | TINYINT | NOT NULL, DEFAULT 1 | 是否启用 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**索引**：
- `idx_parent_id` ON (`parent_id`)

---

## 附录：初始化 SQL 片段

```sql
-- 会员表
CREATE TABLE member (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    open_id VARCHAR(64) NOT NULL UNIQUE,
    session_key VARCHAR(128) NULL,
    nickname VARCHAR(64) NULL,
    avatar_url VARCHAR(512) NULL,
    phone VARCHAR(20) NULL UNIQUE,
    level TINYINT NOT NULL DEFAULT 1,
    last_login_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_open_id (open_id),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 购物车表
CREATE TABLE cart (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id BIGINT NOT NULL,
    goods_id VARCHAR(32) NOT NULL,
    spec_id VARCHAR(32) NOT NULL,
    num INT NOT NULL DEFAULT 1,
    selected TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE INDEX idx_member_goods_spec (member_id, goods_id, spec_id),
    INDEX idx_member_id (member_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 商品缓存表
CREATE TABLE goods (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    goods_id VARCHAR(32) NOT NULL UNIQUE,
    goods_no VARCHAR(32) NULL,
    goods_name VARCHAR(256) NOT NULL,
    category_id BIGINT NULL,
    price DECIMAL(10,2) NOT NULL DEFAULT 0,
    original_price DECIMAL(10,2) NULL,
    description TEXT NULL,
    images JSON NULL,
    sales INT NOT NULL DEFAULT 0,
    is_on_sale TINYINT NOT NULL DEFAULT 1,
    wdt_synced_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_goods_id (goods_id),
    INDEX idx_category (category_id),
    INDEX idx_is_on_sale (is_on_sale)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 规格缓存表
CREATE TABLE goods_spec (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    spec_id VARCHAR(32) NOT NULL UNIQUE,
    goods_id VARCHAR(32) NOT NULL,
    spec_no VARCHAR(32) NULL,
    spec_name VARCHAR(128) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    is_on_sale TINYINT NOT NULL DEFAULT 1,
    wdt_synced_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_spec_id (spec_id),
    INDEX idx_goods_id (goods_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 收藏表
CREATE TABLE favorites (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id BIGINT NOT NULL,
    goods_id VARCHAR(32) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE INDEX idx_member_goods (member_id, goods_id),
    INDEX idx_member_id (member_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单表
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(64) NOT NULL UNIQUE,
    wdt_tid VARCHAR(64) NULL,
    member_id BIGINT NOT NULL,
    trade_status TINYINT NOT NULL,
    pay_status VARCHAR(8) NOT NULL,
    logistics_type TINYINT NOT NULL,
    receiver_name VARCHAR(64) NOT NULL,
    receiver_mobile VARCHAR(20) NOT NULL,
    receiver_province VARCHAR(32) NOT NULL,
    receiver_city VARCHAR(32) NOT NULL,
    receiver_district VARCHAR(32) NOT NULL,
    receiver_address VARCHAR(256) NOT NULL,
    post_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    trade_time DATETIME NOT NULL,
    push_status TINYINT NOT NULL DEFAULT 0,
    push_msg VARCHAR(256) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id),
    INDEX idx_member_id (member_id),
    INDEX idx_wdt_tid (wdt_tid),
    INDEX idx_trade_time (trade_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单明细表
CREATE TABLE order_items (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(64) NOT NULL,
    sub_order_id VARCHAR(64) NOT NULL UNIQUE,
    goods_id VARCHAR(32) NOT NULL,
    spec_id VARCHAR(32) NOT NULL,
    goods_name VARCHAR(256) NOT NULL,
    spec_name VARCHAR(128) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    num INT NOT NULL,
    refund_status TINYINT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id),
    INDEX idx_sub_order_id (sub_order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- WDT配置表
CREATE TABLE wdt_config (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    env ENUM('test','prod') NOT NULL UNIQUE,
    appkey VARCHAR(64) NOT NULL,
    appsecret VARCHAR(128) NOT NULL,
    sid VARCHAR(32) NOT NULL,
    base_url VARCHAR(128) NOT NULL,
    is_active TINYINT NOT NULL DEFAULT 1,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 商品分类表
CREATE TABLE category (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    parent_id BIGINT NULL,
    sort INT NOT NULL DEFAULT 0,
    is_active TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_parent_id (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
