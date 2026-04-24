/* ============================================================
   intimoi API 客户端
   基于 api-contract.md v1.1.0
   ============================================================ */

import Taro from '@tarojs/taro'

// TODO: 后端部署后替换为实际地址
const BASE_URL = 'https://api.intimoi.com'

// ----------------------------------------------------------------
// 工具函数
// ----------------------------------------------------------------

function getToken(): string {
  return Taro.getStorageSync('token') || ''
}

// 格式化 price（分 → 元）
function formatPrice(cent: number): string {
  return (cent / 100).toFixed(2)
}

// ----------------------------------------------------------------
// 响应类型
// ----------------------------------------------------------------

interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

// ----------------------------------------------------------------
// 请求封装
// ----------------------------------------------------------------

async function request<T = unknown>(options: {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, unknown>
  needAuth?: boolean
}): Promise<T> {
  const { url, method = 'GET', data, needAuth = false } = options
  const fullUrl = url.startsWith('http') ? url : `${BASE_URL}${url}`

  const header: Record<string, string> = {
    'Content-Type': 'application/json; charset=UTF-8'
  }

  if (needAuth) {
    const token = getToken()
    if (token) {
      header['Authorization'] = `Bearer ${token}`
    }
  }

  try {
    const res = await Taro.request({
      url: fullUrl,
      method,
      data,
      header
    })

    const result = res.data as ApiResponse<T>

    if (result.code === 0) {
      return result.data as T
    }

    // 401 未登录
    if (result.code === 401) {
      Taro.removeStorageSync('token')
      Taro.removeStorageSync('member_id')
      Taro.showToast({ title: '请先登录', icon: 'none' })
    }

    throw new Error(result.message || `请求失败 code=${result.code}`)
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : '网络错误'
    Taro.showToast({ title: message, icon: 'none' })
    throw err
  }
}

// ----------------------------------------------------------------
// 会员 API
// ----------------------------------------------------------------

export const memberApi = {
  /** 微信授权登录 */
  login: (code: string) =>
    request<{
      open_id: string
      session_key: string
      token: string
      member_id: number
    }>({
      url: '/api/v1/member/login',
      method: 'POST',
      data: { code }
    }),

  /** 获取会员信息 */
  getInfo: () =>
    request<{
      id: number
      open_id: string
      nickname: string
      avatar_url: string
      phone: string
      level: number
      created_at: string
    }>({ url: '/api/v1/member/info', needAuth: true }),

  /** 更新会员信息 */
  updateInfo: (data: { nickname?: string; avatar_url?: string; phone?: string }) =>
    request({ url: '/api/v1/member/info', method: 'PUT', data, needAuth: true })
}

// ----------------------------------------------------------------
// 商品 API
// ----------------------------------------------------------------

export interface GoodsItem {
  goods_id: string
  goods_name: string
  price: number
  original_price: number
  thumbnail: string
  sales: number
}

export interface GoodsSpec {
  spec_id: string
  spec_name: string
  stock: number
  price: number
}

export interface GoodsDetail {
  goods_id: string
  goods_name: string
  price: number
  original_price: number
  description: string
  images: string[]
  specs: GoodsSpec[]
  stock: number
  sales: number
}

export const goodsApi = {
  /** 商品列表 */
  list: (params?: {
    category_id?: number
    page?: number
    page_size?: number
    sort?: 'default' | 'price_asc' | 'price_desc' | 'sales'
  }) =>
    request<{ items: GoodsItem[]; total: number }>({
      url: '/api/v1/goods',
      data: params
    }),

  /** 商品详情 */
  detail: (goodsId: string) =>
    request<GoodsDetail>({ url: `/api/v1/goods/${goodsId}` })
}

// ----------------------------------------------------------------
// 购物车 API
// ----------------------------------------------------------------

export interface CartItem {
  id: number
  goods_id: string
  spec_id: string
  goods_name: string
  spec_name: string
  price: number
  num: number
  stock: number
  thumbnail: string
  selected: boolean
}

export const cartApi = {
  /** 获取购物车列表 */
  get: () =>
    request<{ items: CartItem[]; total_amount: number }>({
      url: '/api/v1/cart',
      needAuth: true
    }),

  /** 添加商品至购物车 */
  add: (goodsId: string, specId: string, num = 1) =>
    request<{ cart_item_id: number; cart_count: number }>({
      url: '/api/v1/cart',
      method: 'POST',
      data: { goods_id: goodsId, spec_id: specId, num },
      needAuth: true
    }),

  /** 更新购物车商品数量 */
  updateNum: (itemId: number, num: number) =>
    request({ url: `/api/v1/cart/${itemId}`, method: 'PUT', data: { num }, needAuth: true }),

  /** 删除购物车商品 */
  remove: (itemId: number) =>
    request({ url: `/api/v1/cart/${itemId}`, method: 'DELETE', needAuth: true }),

  /** 全选/取消全选 */
  selectAll: (selected: boolean) =>
    request({ url: '/api/v1/cart/select-all', method: 'PUT', data: { selected }, needAuth: true })
}

// ----------------------------------------------------------------
// 收藏 API
// ----------------------------------------------------------------

export const favoriteApi = {
  /** 收藏列表 */
  list: (params?: { page?: number; page_size?: number }) =>
    request<{ items: GoodsItem[] }>({ url: '/api/v1/favorites', data: params, needAuth: true }),

  /** 添加收藏 */
  add: (goodsId: string) =>
    request({ url: '/api/v1/favorites', method: 'POST', data: { goods_id: goodsId }, needAuth: true }),

  /** 取消收藏 */
  remove: (goodsId: string) =>
    request({ url: `/api/v1/favorites/${goodsId}`, method: 'DELETE', needAuth: true })
}

// ----------------------------------------------------------------
// 订单 API（骨架，待 WDT 对接后完善）
// ----------------------------------------------------------------

export const orderApi = {
  /** 订单列表 */
  list: (params?: { page?: number; page_size?: number }) =>
    request<{ items: unknown[] }>({ url: '/api/v1/orders', data: params, needAuth: true })
}

// ----------------------------------------------------------------
// 工具
// ----------------------------------------------------------------

export { formatPrice, getToken }
