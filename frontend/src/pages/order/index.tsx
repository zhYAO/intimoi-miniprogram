import React, { useState } from 'react'
import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { TabBar } from '../../components/TabBar'
import { orderApi } from '../../utils/request'
import './index.css'

const TAB_BAR_ITEMS = [
  { pagePath: 'pages/index/index', text: '发现', icon: 'home' },
  { pagePath: 'pages/category/index', text: '分类', icon: 'grid' },
  { pagePath: 'pages/cart/index', text: '购物车', icon: 'cart' },
  { pagePath: 'pages/profile/index', text: '我的', icon: 'user' }
]

type StatusKey = '全部' | '待付款' | '待发货' | '已完成'

const ORDER_STATUS_MAP: Record<StatusKey, number | null> = {
  '全部': null,
  '待付款': 10,
  '待发货': 20,
  '已完成': 40
}

interface OrderItem {
  oid: number
  goods_name: string
  spec_name: string
  price: number
  num: number
}

interface Order {
  tid: string
  trade_status: number
  pay_status: number
  created_at: string
  items: OrderItem[]
  total_amount: number
}

const STATUS_LABEL: Record<number, string> = {
  10: '待付款',
  20: '待发货',
  30: '已发货',
  40: '已完成'
}

const STATUS_COLOR: Record<number, string> = {
  10: 'var(--fg-price)',
  20: 'var(--warning)',
  30: 'var(--success)',
  40: 'var(--fg-tertiary)'
}

export default function Order() {
  const [activeTab, setActiveTab] = useState<StatusKey>('全部')
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(false)

  async function fetchOrders() {
    setLoading(true)
    try {
      const status = ORDER_STATUS_MAP[activeTab]
      const res = await orderApi.list(status ?? undefined)
      setOrders(res.items || [])
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  React.useEffect(() => {
    fetchOrders()
  }, [activeTab])

  function handleTabClick(tab: StatusKey) {
    setActiveTab(tab)
  }

  function handleOrderClick(order: Order) {
    Taro.navigateTo({ url: `/pages/order_detail/index?tid=${order.tid}` })
  }

  function handlePay(order: Order) {
    // TODO: 调用支付接口
    Taro.showToast({ title: '支付功能待接入', icon: 'none' })
  }

  function handleCancel(order: Order) {
    Taro.showModal({
      title: '确认取消',
      content: '确定要取消该订单吗？',
      success: res => {
        if (res.confirm) {
          // TODO: 调用取消接口
          setOrders(prev => prev.filter(o => o.tid !== order.tid))
        }
      }
    })
  }

  const tabs: StatusKey[] = ['全部', '待付款', '待发货', '已完成']

  return (
    <View className="page-order">
      <NavBar title="我的订单" showBack />

      <View className="page-order__content">
        {/* Tab 栏 */}
        <View className="order-tabs">
          {tabs.map(tab => (
            <Text
              key={tab}
              className={`order-tab ${activeTab === tab ? 'order-tab--active' : ''}`}
              onClick={() => handleTabClick(tab)}
            >
              {tab}
            </Text>
          ))}
        </View>

        {/* 订单列表 */}
        {loading ? (
          <View className="order-loading">
            <Text className="caption">加载中...</Text>
          </View>
        ) : orders.length === 0 ? (
          <View className="order-empty">
            <Text className="caption">暂无订单</Text>
          </View>
        ) : (
          <View className="order-list">
            {orders.map(order => (
              <View
                key={order.tid}
                className="order-card"
                onClick={() => handleOrderClick(order)}
              >
                <View className="order-card__header">
                  <Text className="order-card__no">订单号 {order.tid}</Text>
                  <Text
                    className="order-card__status"
                    style={{ color: STATUS_COLOR[order.trade_status] }}
                  >
                    {STATUS_LABEL[order.trade_status] || '未知'}
                  </Text>
                </View>

                <View className="order-card__goods">
                  {order.items.slice(0, 3).map((item, idx) => (
                    <View key={item.oid} className="order-card__goods-item">
                      <View className="order-card__goods-img-placeholder" />
                      <View className="order-card__goods-info">
                        <Text className="order-card__goods-name" numberOfLines={1}>{item.goods_name}</Text>
                        <Text className="caption">{item.spec_name}</Text>
                      </View>
                      <Text className="order-card__goods-price">¥{(item.price / 100).toFixed(2)}</Text>
                    </View>
                  ))}
                  {order.items.length > 3 && (
                    <Text className="caption" style="padding-left: 80px">
                      还有{order.items.length - 3}件商品 ›
                    </Text>
                  )}
                </View>

                <View className="order-card__footer">
                  <Text className="order-card__time">{order.created_at}</Text>
                  <View className="order-card__actions">
                    {order.trade_status === 10 && (
                      <>
                        <Text
                          className="order-card__action order-card__action--text"
                          onClick={e => { e.stopPropagation(); handleCancel(order) }}
                        >
                          取消订单
                        </Text>
                        <Text
                          className="order-card__action order-card__action--primary"
                          onClick={e => { e.stopPropagation(); handlePay(order) }}
                        >
                          去支付
                        </Text>
                      </>
                    )}
                    {order.trade_status === 30 && (
                      <Text
                        className="order-card__action order-card__action--primary"
                        onClick={e => { e.stopPropagation(); Taro.navigateTo({ url: `/pages/logistics/index?tid=${order.tid}` }) }}
                      >
                        查看物流
                      </Text>
                    )}
                  </View>
                </View>
              </View>
            ))}
          </View>
        )}
      </View>

      <TabBar items={TAB_BAR_ITEMS} />
    </View>
  )
}
