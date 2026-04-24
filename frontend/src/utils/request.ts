/* ============================================================
   intimoi API 客户端
   基于 api-contract.md v1.1.0
   ============================================================ */

import Taro from '@tarojs/taro'

// API Base URL — 从小程序配置读取，支持环境切换
// 开发/测试：使用本地配置；生产：替换为正式地址
const BASE_URL = 'https://api.intimoi.com'

// ----------------------------------------------------------------
// 工具函数
// ----------------------------------------------------------------

export function getToken(): string {
  return Taro.getStorageSync('token') || ''
}

export function formatPrice(cent: number): string {
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
  get: () =>
    request<{ items: CartItem[]; total_amount: number }>({
      url: '/api/v1/cart',
      needAuth: true
    }),

  add: (goodsId: string, specId: string, num = 1) =>
    request<{ cart_item_id: number; cart_count: number }>({
      url: '/api/v1/cart',
      method: 'POST',
      data: { goods_id: goodsId, spec_id: specId, num },
      needAuth: true
    }),

  updateNum: (itemId: number, num: number) =>
    request({ url: `/api/v1/cart/${itemId}`, method: 'PUT', data: { num }, needAuth: true }),

  remove: (itemId: number) =>
    request({ url: `/api/v1/cart/${itemId}`, method: 'DELETE', needAuth: true }),

  selectAll: (selected: boolean) =>
    request({ url: '/api/v1/cart/select-all', method: 'PUT', data: { selected }, needAuth: true })
}

// ----------------------------------------------------------------
// 收藏 API
// ----------------------------------------------------------------

export const favoriteApi = {
  list: (params?: { page?: number; page_size?: number }) =>
    request<{ items: GoodsItem[] }>({ url: '/api/v1/favorites', data: params, needAuth: true }),

  add: (goodsId: string) =>
    request({ url: '/api/v1/favorites', method: 'POST', data: { goods_id: goodsId }, needAuth: true }),

  remove: (goodsId: string) =>
    request({ url: `/api/v1/favorites/${goodsId}`, method: 'DELETE', needAuth: true })
}

// ----------------------------------------------------------------
// 订单 API（待 WDT 对接后完善）
// ----------------------------------------------------------------

export const orderApi = {
  list: (params?: { page?: number; page_size?: number }) =>
    request<{ items: unknown[] }>({ url: '/api/v1/orders', data: params, needAuth: true })
}
