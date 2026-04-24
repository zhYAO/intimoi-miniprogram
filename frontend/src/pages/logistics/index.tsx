import React, { useState } from 'react'
import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import './index.css'

interface LogisticsNode {
  time: string
  status: string
  is_latest?: boolean
}

export default function Logistics() {
  const { params } = Taro.getCurrentInstance().router!
  const logisticsNo = (params as { logisticsNo?: string }).logisticsNo || ''

  const [nodes] = useState<LogisticsNode[]>([
    { time: '2026-04-25 14:30:00', status: '已签收，签收人：本人', is_latest: true },
    { time: '2026-04-25 09:20:00', status: '正在派送，联系电话：138xxxx1203' },
    { time: '2026-04-25 07:00:00', status: '到达【上海分拨中心】' },
    { time: '2026-04-24 22:00:00', status: '离开【杭州转运中心】，发往上海' },
    { time: '2026-04-24 20:30:00', status: '到达【杭州转运中心】' },
    { time: '2026-04-24 18:00:00', status: '已发货' }
  ])

  function handleCopy() {
    if (logisticsNo) {
      Taro.setClipboardData({ data: logisticsNo })
      Taro.showToast({ title: '运单号已复制', icon: 'none' })
    }
  }

  return (
    <View className="page-logistics">
      <NavBar title="物流详情" showBack />

      <View className="page-logistics__content">
        {/* 运单信息顶栏 */}
        <View className="logistics-header">
          <View className="logistics-header__info">
            <Text className="logistics-header__label">快递公司</Text>
            <Text className="logistics-header__value">顺丰速运</Text>
          </View>
          <View className="logistics-header__info">
            <Text className="logistics-header__label">运单号</Text>
            <Text className="logistics-header__value logistics-header__value--clickable" onClick={handleCopy}>
              {logisticsNo || 'SF1234567890'} ›
            </Text>
          </View>
        </View>

        {/* 时间轴 */}
        <View className="logistics-timeline">
          {nodes.map((node, idx) => (
            <View key={idx} className="logistics-node">
              <View className={`logistics-node__dot ${node.is_latest ? 'logistics-node__dot--latest' : ''}`} />
              <View className="logistics-node__info">
                <Text className={`logistics-node__status ${node.is_latest ? 'logistics-node__status--latest' : ''}`}>
                  {node.status}
                </Text>
                <Text className="logistics-node__time">{node.time}</Text>
              </View>
            </View>
          ))}
        </View>
      </View>
    </View>
  )
}
