import React, { useState } from 'react'
import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { orderApi } from '../../utils/request'
import './index.css'

interface LogisticsNode {
  time: string
  status: string
  is_latest?: boolean
}

interface OrderDetail {
  tid: string
  trade_status: number
  pay_status: number
  created_at: string
  paid_at?: string
  logistics_company?: string
  logistics_no?: string
  receiver_name: string
  receiver_mobile: string
  receiver_province: string
  receiver_city: string
  receiver_district: string
  receiver_address: string
  items: Array<{
    oid: string
    goods_name: string
    spec_name: string
    price: number
    num: number
  }>
  goods_amount: number
  freight: number
  total_amount: number
}

const STATUS_LABEL: Record<number, string> = {
  10: '待付款',
  20: '已付款待发货',
  30: '已发货',
  40: '已完成'
}

export default function OrderDetail() {
  const { params } = Taro.getCurrentInstance().router!
  const tid = (params as { tid?: string }).tid || ''

  const [order, setOrder] = useState<OrderDetail | null>(null)
  const [logistics, setLogistics] = useState<LogisticsNode[]>([])
  const [loading, setLoading] = useState(false)

  async function fetchOrderDetail() {
    if (!tid) return
    setLoading(true)
    try {
      const res = await orderApi.detail(tid)
      setOrder(res as unknown as OrderDetail)
      // 模拟物流节点
      if (res.logistics_no) {
        setLogistics([
          { time: '2026-04-25 14:30:00', status: '包裹已签收，签收人：本人', is_latest: true },
          { time: '2026-04-25 09:20:00', status: '正在派送，联系电话：138xxxx1203' },
          { time: '2026-04-25 07:00:00', status: '到达【上海分拨中心】' },
          { time: '2026-04-24 20:00:00', status: '已发货' }
        ])
      }
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  React.useEffect(() => {
    fetchOrderDetail()
  }, [tid])

  function handleCopyOrderNo() {
    if (order?.tid) {
      Taro.setClipboardData({ data: order.tid })
      Taro.showToast({ title: '订单号已复制', icon: 'none' })
    }
  }

  if (loading) {
    return (
      <View className="page-order-detail">
        <NavBar title="订单详情" showBack />
        <View className="order-detail-loading">
          <Text className="caption">加载中...</Text>
        </View>
      </View>
    )
  }

  if (!order) {
    return (
      <View className="page-order-detail">
        <NavBar title="订单详情" showBack />
        <View className="order-detail-loading">
          <Text className="caption">订单不存在</Text>
        </View>
      </View>
    )
  }

  return (
    <View className="page-order-detail">
      <NavBar title="订单详情" showBack />

      <View className="page-order-detail__content">
        {/* 订单状态 */}
        <View className="order-detail-status">
          <Text className="order-detail-status__label">
            {STATUS_LABEL[order.trade_status] || '未知状态'}
          </Text>
        </View>

        {/* 物流信息（已发货后显示） */}
        {order.trade_status >= 30 && order.logistics_no && (
          <>
            <View className="divider" />
            <View className="order-detail-section">
              <View className="order-detail-section__header">
                <Text className="eyebrow">物流信息</Text>
              </View>
              <View className="logistics-info">
                <Text className="logistics-info__company">{order.logistics_company || '快递'}</Text>
                <Text
                  className="logistics-info__no"
                  onClick={() => {
                    Taro.setClipboardData({ data: order.logistics_no || '' })
                    Taro.showToast({ title: '运单号已复制', icon: 'none' })
                  }}
                >
                  {order.logistics_no} ›
                </Text>
              </View>
              <View className="logistics-timeline">
                {logistics.map((node, idx) => (
                  <View key={idx} className="logistics-node">
                    <View className={`logistics-node__dot ${node.is_latest ? 'logistics-node__dot--latest' : ''}`} />
                    <View className="logistics-node__info">
                      <Text className="logistics-node__status">{node.status}</Text>
                      <Text className="logistics-node__time">{node.time}</Text>
                    </View>
                  </View>
                ))}
              </View>
            </View>
          </>
        )}

        <View className="divider" />

        {/* 收货地址 */}
        <View className="order-detail-section">
          <View className="order-detail-section__header">
            <Text className="eyebrow">收货地址</Text>
          </View>
          <View className="order-detail-address">
            <View className="order-detail-address__top">
              <Text className="order-detail-address__name">{order.receiver_name}</Text>
              <Text className="order-detail-address__mobile">{order.receiver_mobile}</Text>
            </View>
            <Text className="order-detail-address__detail">
              {order.receiver_province}{order.receiver_city}{order.receiver_district}{order.receiver_address}
            </Text>
          </View>
        </View>

        <View className="divider" />

        {/* 商品列表 */}
        <View className="order-detail-section">
          <View className="order-detail-section__header">
            <Text className="eyebrow">商品清单</Text>
          </View>
          {order.items.map(item => (
            <View key={item.oid} className="order-detail-goods">
              <View className="order-detail-goods__img-placeholder" />
              <View className="order-detail-goods__info">
                <Text className="order-detail-goods__name" numberOfLines={2}>{item.goods_name}</Text>
                <Text className="caption">{item.spec_name}</Text>
              </View>
              <View className="order-detail-goods__right">
                <Text className="order-detail-goods__price">¥{(item.price / 100).toFixed(2)}</Text>
                <Text className="caption">x{item.num}</Text>
              </View>
            </View>
          ))}
        </View>

        <View className="divider" />

        {/* 订单信息 */}
        <View className="order-detail-section">
          <View className="order-detail-section__header">
            <Text className="eyebrow">订单信息</Text>
          </View>
          <View className="order-detail-info">
            <View className="order-detail-info__row">
              <Text className="caption">订单编号</Text>
              <Text className="order-detail-info__value" onClick={handleCopyOrderNo}>
                {order.tid} ›
              </Text>
            </View>
            <View className="order-detail-info__row">
              <Text className="caption">下单时间</Text>
              <Text className="order-detail-info__value">{order.created_at}</Text>
            </View>
            {order.paid_at && (
              <View className="order-detail-info__row">
                <Text className="caption">支付时间</Text>
                <Text className="order-detail-info__value">{order.paid_at}</Text>
              </View>
            )}
          </View>
        </View>

        <View className="divider" />

        {/* 价格明细 */}
        <View className="order-detail-section">
          <View className="order-detail-prices">
            <View className="order-detail-prices__row">
              <Text className="caption">商品总额</Text>
              <Text className="order-detail-prices__value">¥{(order.goods_amount / 100).toFixed(2)}</Text>
            </View>
            <View className="order-detail-prices__row">
              <Text className="caption">运费</Text>
              <Text className="order-detail-prices__value">
                {order.freight === 0 ? '免运费' : `¥${(order.freight / 100).toFixed(2)}`}
              </Text>
            </View>
            <View className="order-detail-prices__row order-detail-prices__row--total">
              <Text className="order-detail-prices__label">实付金额</Text>
              <Text className="order-detail-prices__total">¥{(order.total_amount / 100).toFixed(2)}</Text>
            </View>
          </View>
        </View>
      </View>
    </View>
  )
}
