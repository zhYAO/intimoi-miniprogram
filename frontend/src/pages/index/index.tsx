import React, { useState, useEffect } from 'react'
import { View, Text } from '@tarojs/components'
import { useDidShow } from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { TabBar } from '../../components/TabBar'
import { goodsApi, GoodsItem } from '../../utils/request'
import './index.css'

const TAB_BAR_ITEMS = [
  { pagePath: 'pages/index/index', text: '首页', icon: 'home' },
  { pagePath: 'pages/goods_list/index', text: '精选', icon: 'grid' },
  { pagePath: 'pages/cart/index', text: '购物车', icon: 'cart' },
  { pagePath: 'pages/profile/index', text: '我的', icon: 'user' }
]

const CATEGORIES = [
  { id: 1, label: '美妆', icon: '◈' },
  { id: 2, label: '女装', icon: '◈' },
  { id: 3, label: '配饰', icon: '◈' },
  { id: 4, label: '家居', icon: '◈' }
]

export default function Index() {
  const [featured, setFeatured] = useState<GoodsItem[]>([])
  const [loading, setLoading] = useState(false)

  async function fetchFeatured() {
    setLoading(true)
    try {
      // 获取销量最高的商品作为编辑精选
      const res = await goodsApi.list({ sort: 'sales', page_size: 4 })
      setFeatured(res.items)
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  useDidShow(() => {
    fetchFeatured()
  })

  return (
    <View className="page-index">
      <NavBar title="intimoi" />

      <View className="page-index__content">
        {/* Banner */}
        <View className="index-banner">
          <View className="index-banner__placeholder">
            <Text className="eyebrow">编辑精选</Text>
          </View>
        </View>

        {/* 分类入口 */}
        <View className="index-categories">
          {CATEGORIES.map(cat => (
            <View key={cat.id} className="index-category">
              <View className="index-category__icon">{cat.icon}</View>
              <Text className="index-category__label">{cat.label}</Text>
            </View>
          ))}
        </View>

        {/* 本月上新 */}
        <View className="index-section">
          <View className="index-section__header">
            <Text className="h3">本月精选</Text>
            <Text
              className="caption"
              onClick={() => {}}
            >查看全部 →</Text>
          </View>

          {loading ? (
            <View className="index-section__loading">
              <Text className="caption">加载中...</Text>
            </View>
          ) : featured.length > 0 ? (
            <View className="index-section__grid">
              {featured.map(item => (
                <View key={item.goods_id} className="goods-card">
                  <View className="goods-card__image-placeholder" />
                  <View className="goods-card__body">
                    <Text className="goods-card__title">{item.goods_name}</Text>
                    <Text className="price">¥{item.price}</Text>
                  </View>
                </View>
              ))}
            </View>
          ) : (
            <View className="index-section__empty">
              <Text className="caption">暂无精选商品</Text>
            </View>
          )}
        </View>
      </View>

      <TabBar items={TAB_BAR_ITEMS} />
    </View>
  )
}
