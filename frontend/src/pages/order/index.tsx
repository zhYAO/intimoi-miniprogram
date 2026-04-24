import React, { useState } from 'react'
import { View, Text } from '@tarojs/components'
import { useDidShow } from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { orderApi } from '../../utils/request'
import './index.css'

const ORDER_TABS = ['全部', '待付款', '待发货', '已完成']

export default function Order() {
  const [activeTab, setActiveTab] = useState('全部')
  const [orders, setOrders] = useState<unknown[]>([])
  const [loading, setLoading] = useState(false)

  async function fetchOrders() {
    setLoading(true)
    try {
      const res = await orderApi.list()
      setOrders(res.items)
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  useDidShow(() => {
    fetchOrders()
  })

  return (
    <View className="page-order">
      <NavBar title="我的订单" showBack />

      <View className="page-order__content">
        <View className="order-tabs">
          {ORDER_TABS.map(tab => (
            <Text
              key={tab}
              className={`order-tab ${activeTab === tab ? 'order-tab--active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </Text>
          ))}
        </View>

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
            {/* TODO: 订单列表渲染，等后端完成订单接口后实现 */}
          </View>
        )}
      </View>
    </View>
  )
}
