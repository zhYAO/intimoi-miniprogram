import React, { useState } from 'react'
import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { useDidShow } from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { TabBar } from '../../components/TabBar'
import { goodsApi, GoodsItem } from '../../utils/request'
import './index.css'

const TAB_BAR_ITEMS = [
  { pagePath: 'pages/index/index', text: '发现', icon: 'home' },
  { pagePath: 'pages/category/index', text: '分类', icon: 'grid' },
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
  const params = Taro.getCurrentInstance().router?.params as { keyword?: string; category_id?: string } | undefined

  const [goods, setGoods] = useState<GoodsItem[]>([])
  const [sort, setSort] = useState<string>('default')
  const [loading, setLoading] = useState(false)

  async function fetchGoods() {
    setLoading(true)
    try {
      const res = await goodsApi.list({
        keyword: params?.keyword,
        category_id: params?.category_id ? Number(params.category_id) : undefined,
        sort: sort as 'default' | 'price_asc' | 'price_desc' | 'sales',
        page_size: 20
      })
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

  React.useEffect(() => {
    fetchGoods()
  }, [sort])

  function handleSortChange(newSort: string) {
    setSort(newSort)
  }

  function handleGoodsClick(goodsId: number) {
    Taro.navigateTo({ url: `/pages/goods_detail/index?goodsId=${goodsId}` })
  }

  return (
    <View className="page-goods-list">
      <NavBar title={params?.keyword ? `搜索：${params.keyword}` : '精选'} />

      <View className="page-goods-list__content">
        {/* 筛选栏 */}
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

        {/* 商品列表 */}
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
                onClick={() => handleGoodsClick(item.goods_id)}
              >
                <View className="goods-card__image">
                  <View className="goods-card__image-placeholder" />
                </View>
                <View className="goods-card__info">
                  <Text className="goods-card__name" numberOfLines={2}>{item.goods_name}</Text>
                  <View className="goods-card__price-row">
                    <Text className="goods-card__price">¥{(item.price / 100).toFixed(2)}</Text>
                    {item.original_price > item.price && (
                      <Text className="goods-card__original-price">
                        ¥{(item.original_price / 100).toFixed(2)}
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
