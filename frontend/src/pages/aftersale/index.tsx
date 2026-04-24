import React, { useState } from 'react'
import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { TabBar } from '../../components/TabBar'
import './index.css'

const TAB_BAR_ITEMS = [
  { pagePath: 'pages/index/index', text: '发现', icon: 'home' },
  { pagePath: 'pages/category/index', text: '分类', icon: 'grid' },
  { pagePath: 'pages/cart/index', text: '购物车', icon: 'cart' },
  { pagePath: 'pages/profile/index', text: '我的', icon: 'user' }
]

interface AftersaleItem {
  id: number
  aftersale_type: '退款' | '退货' | '换货'
  status: '处理中' | '已完成' | '已取消'
  goods_name: string
  created_at: string
}

export default function Aftersale() {
  const [activeTab, setActiveTab] = useState<'全部' | '处理中' | '已完成'>('全部')
  const [list, setList] = useState<AftersaleItem[]>([])
  const [loading, setLoading] = useState(false)

  async function fetchList() {
    setLoading(true)
    try {
      // TODO: 调用后端售后列表接口
      // const res = await aftersaleApi.list()
      // setList(res.items)
      setList([])
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  React.useEffect(() => {
    fetchList()
  }, [activeTab])

  function filteredList() {
    if (activeTab === '全部') return list
    return list.filter(item =>
      activeTab === '处理中' ? item.status === '处理中' : item.status !== '处理中'
    )
  }

  return (
    <View className="page-aftersale">
      <NavBar title="我的售后" showBack />

      <View className="page-aftersale__content">
        <View className="aftersale-tabs">
          {(['全部', '处理中', '已完成'] as const).map(tab => (
            <Text
              key={tab}
              className={`aftersale-tab ${activeTab === tab ? 'aftersale-tab--active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </Text>
          ))}
        </View>

        {loading ? (
          <View className="aftersale-loading">
            <Text className="caption">加载中...</Text>
          </View>
        ) : filteredList().length === 0 ? (
          <View className="aftersale-empty">
            <Text className="caption">暂无售后记录</Text>
          </View>
        ) : (
          <View className="aftersale-list">
            {filteredList().map(item => (
              <View key={item.id} className="aftersale-card">
                <View className="aftersale-card__header">
                  <Text className="aftersale-card__type">{item.aftersale_type}</Text>
                  <Text className={`aftersale-card__status aftersale-card__status--${item.status}`}>
                    {item.status}
                  </Text>
                </View>
                <Text className="aftersale-card__goods">{item.goods_name}</Text>
                <Text className="aftersale-card__time">{item.created_at}</Text>
              </View>
            ))}
          </View>
        )}
      </View>

      <TabBar items={TAB_BAR_ITEMS} />
    </View>
  )
}
