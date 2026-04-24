import React, { useState } from 'react'
import { View, Text, ScrollView } from '@tarojs/components'
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

interface Category {
  id: number
  label: string
}

const SORT_OPTIONS = [
  { key: 'default', label: '推荐' },
  { key: 'sales', label: '销量' },
  { key: 'price_asc', label: '价格 ↑' },
  { key: 'price_desc', label: '价格 ↓' }
]

export default function Category() {
  const [activeCategoryId, setActiveCategoryId] = useState<number>(1)
  const [activeSort, setActiveSort] = useState<string>('default')
  const [goods, setGoods] = useState<GoodsItem[]>([])
  const [loading, setLoading] = useState(false)

  const categories: Category[] = [
    { id: 1, label: '美妆' },
    { id: 2, label: '女装' },
    { id: 3, label: '配饰' },
    { id: 4, label: '家居' },
    { id: 5, label: '护肤' },
    { id: 6, label: '香水' }
  ]

  async function fetchGoods() {
    setLoading(true)
    try {
      const res = await goodsApi.list({
        category_id: activeCategoryId,
        sort: activeSort as 'default' | 'price_asc' | 'price_desc' | 'sales',
        page_size: 20
      })
      setGoods(res.items)
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  React.useEffect(() => {
    fetchGoods()
  }, [activeCategoryId, activeSort])

  function handleCategoryClick(id: number) {
    setActiveCategoryId(id)
  }

  function handleSortClick(key: string) {
    setActiveSort(key)
  }

  return (
    <View className="page-category">
      <NavBar title="分类" />

      <View className="page-category__body">
        {/* 左侧类目列表 */}
        <ScrollView
          className="category-left"
          scroll-y
          enhanced
          bounces={false}
        >
          {categories.map(cat => (
            <View
              key={cat.id}
              className={`category-left__item ${activeCategoryId === cat.id ? 'category-left__item--active' : ''}`}
              onClick={() => handleCategoryClick(cat.id)}
            >
              <Text className="category-left__label">{cat.label}</Text>
            </View>
          ))}
        </ScrollView>

        {/* 右侧商品列表 */}
        <View className="category-right">
          {/* 筛选栏 */}
          <View className="category-filter">
            {SORT_OPTIONS.map(opt => (
              <Text
                key={opt.key}
                className={`category-filter__item ${activeSort === opt.key ? 'category-filter__item--active' : ''}`}
                onClick={() => handleSortClick(opt.key)}
              >
                {opt.label}
              </Text>
            ))}
          </View>

          {/* 商品网格 */}
          <ScrollView className="category-goods" scroll-y enhanced>
            {loading ? (
              <View className="category-loading">
                <Text className="caption">加载中...</Text>
              </View>
            ) : goods.length === 0 ? (
              <View className="category-empty">
                <Text className="caption">暂无商品</Text>
              </View>
            ) : (
              <View className="goods-grid">
                {goods.map(item => (
                  <View
                    key={item.goods_id}
                    className="goods-card"
                    onClick={() => {
                      // Taro.navigateTo({ url: `/pages/goods_detail/index?goodsId=${item.goods_id}` })
                    }}
                  >
                    <View className="goods-card__image">
                      {item.goods_img ? (
                        <View className="goods-card__image-placeholder" />
                      ) : (
                        <View className="goods-card__image-placeholder" />
                      )}
                    </View>
                    <View className="goods-card__info">
                      <Text className="goods-card__name" numberOfLines={2}>{item.goods_name}</Text>
                      <View className="goods-card__price-row">
                        <Text className="goods-card__price">¥{item.price}</Text>
                        {item.original_price > item.price && (
                          <Text className="goods-card__original-price">¥{item.original_price}</Text>
                        )}
                      </View>
                    </View>
                  </View>
                ))}
              </View>
            )}
          </ScrollView>
        </View>
      </View>

      <TabBar items={TAB_BAR_ITEMS} />
    </View>
  )
}
