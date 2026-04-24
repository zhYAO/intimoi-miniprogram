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

const SORT_OPTIONS = [
  { key: 'default', label: '推荐' },
  { key: 'sales', label: '销量' },
  { key: 'price_asc', label: '价格 ↑' },
  { key: 'price_desc', label: '价格 ↓' }
]

export default function GoodsList() {
  const [goods, setGoods] = useState<GoodsItem[]>([])
  const [sort, setSort] = useState<string>('default')
  const [loading, setLoading] = useState(false)

  async function fetchGoods() {
    setLoading(true)
    try {
      const res = await goodsApi.list({ sort: sort as 'default' | 'price_asc' | 'price_desc' | 'sales', page_size: 20 })
      setGoods(res.items)
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  useDidShow(() => {
    fetchGoods()
  })

  function handleSortChange(newSort: string) {
    setSort(newSort)
    fetchGoods()
  }

  return (
    <View className="page-goods-list">
      <NavBar title="精选" />
      <View className="page-goods-list__content">
        <View className="goods-filter">
          {SORT_OPTIONS.map(opt => (
            <Text
              key={opt.key}
              className={`goods-filter__item ${sort === opt.key ? 'goods-filter__item--active' : ''}`}
              onClick={() => handleSortChange(opt.key)}
            >
              {opt.label}
            </Text>
          ))}
        </View>

        {loading ? (
          <View className="goods-loading">
            <Text className="caption">加载中...</Text>
          </View>
        ) : goods.length === 0 ? (
          <View className="goods-empty">
            <Text className="caption">暂无商品</Text>
          </View>
        ) : (
          <View className="goods-grid">
            {goods.map(item => (
              <View
                key={item.goods_id}
                className="goods-card"
                onClick={() => {
                  // 跳转商品详情
                }}
              >
                <View className="goods-card__image-wrap">
                  {item.thumbnail ? (
                    <View className="goods-card__image" style={`background-image: url(${item.thumbnail})`} />
                  ) : (
                    <View className="goods-card__image goods-card__image--placeholder" />
                  )}
                </View>
                <View className="goods-card__body">
                  <Text className="goods-card__title">{item.goods_name}</Text>
                  <View className="goods-card__price-row">
                    <Text className="goods-card__price">¥{item.price}</Text>
                    {item.original_price > item.price && (
                      <Text className="goods-card__original-price">¥{item.original_price}</Text>
                    )}
                  </View>
                  {item.sales > 0 && (
                    <Text className="goods-card__sales">已售 {item.sales}</Text>
                  )}
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
