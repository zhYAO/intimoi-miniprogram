import React, { useState } from 'react'
import { View, Text, Input } from '@tarojs/components'
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

const CATEGORIES = [
  { id: 1, label: '美妆', icon: '◈' },
  { id: 2, label: '女装', icon: '◈' },
  { id: 3, label: '配饰', icon: '◈' },
  { id: 4, label: '家居', icon: '◈' }
]

// 静态 Banner 数据（CMS 管理后替换）
const BANNERS = [
  { id: 1, image: '', alt: '新品上市' },
  { id: 2, image: '', alt: '春季精选' },
  { id: 3, image: '', alt: '会员专享' }
]

export default function Index() {
  const [featured, setFeatured] = useState<GoodsItem[]>([])
  const [newArrivals, setNewArrivals] = useState<GoodsItem[]>([])
  const [loading, setLoading] = useState(false)
  const [activeBanner, setActiveBanner] = useState(0)
  const [searchValue, setSearchValue] = useState('')

  async function fetchData() {
    setLoading(true)
    try {
      const [featuredRes, newRes] = await Promise.all([
        goodsApi.list({ sort: 'sales', page_size: 3 }),
        goodsApi.list({ sort: 'default', page_size: 4 })
      ])
      setFeatured(featuredRes.items)
      setNewArrivals(newRes.items)
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  useDidShow(() => {
    fetchData()
  })

  function handleSearch() {
    if (searchValue.trim()) {
      Taro.navigateTo({ url: `/pages/goods_list/index?keyword=${encodeURIComponent(searchValue)}` })
    }
  }

  function handleCategoryClick(id: number) {
    Taro.switchTab({ url: '/pages/category/index' })
  }

  function handleGoodsClick(goodsId: number) {
    Taro.navigateTo({ url: `/pages/goods_detail/index?goodsId=${goodsId}` })
  }

  return (
    <View className="page-index">
      <NavBar title="intimoi" />

      <View className="page-index__content">
        {/* 搜索栏 */}
        <View className="index-search">
          <View className="index-search__icon">🔍</View>
          <Input
            className="index-search__input"
            placeholder="搜索商品"
            value={searchValue}
            onInput={e => setSearchValue(e.detail.value)}
            onConfirm={handleSearch}
          />
        </View>

        {/* Banner 轮播 */}
        <View className="index-banner">
          <View className="index-banner__placeholder">
            <Text className="eyebrow">Banner</Text>
            <Text className="caption">（{BANNERS.length}张，CMS 管理）</Text>
          </View>
          <View className="index-banner__dots">
            {BANNERS.map((_, idx) => (
              <View
                key={idx}
                className={`index-banner__dot ${idx === activeBanner ? 'index-banner__dot--active' : ''}`}
                onClick={() => setActiveBanner(idx)}
              />
            ))}
          </View>
        </View>

        {/* 分类入口 */}
        <View className="index-categories">
          {CATEGORIES.map(cat => (
            <View
              key={cat.id}
              className="index-category"
              onClick={() => handleCategoryClick(cat.id)}
            >
              <View className="index-category__icon">{cat.icon}</View>
              <Text className="index-category__label">{cat.label}</Text>
            </View>
          ))}
        </View>

        {/* 编辑精选：左1右2 布局 */}
        <View className="index-section">
          <View className="index-section__header">
            <Text className="eyebrow">编辑精选</Text>
          </View>

          {loading ? (
            <View className="index-featured-loading">
              <Text className="caption">加载中...</Text>
            </View>
          ) : featured.length > 0 ? (
            <View className="index-featured">
              {/* 左侧大图 */}
              {featured[0] && (
                <View
                  className="index-featured__main"
                  onClick={() => handleGoodsClick(featured[0].goods_id)}
                >
                  <View className="index-featured__image-placeholder" />
                  <View className="index-featured__info">
                    <Text className="index-featured__name" numberOfLines={2}>{featured[0].goods_name}</Text>
                    <Text className="index-featured__price">¥{(featured[0].price / 100).toFixed(2)}</Text>
                  </View>
                </View>
              )}
              {/* 右侧两张小图 */}
              <View className="index-featured__side">
                {featured.slice(1, 3).map(item => (
                  <View
                    key={item.goods_id}
                    className="index-featured__side-item"
                    onClick={() => handleGoodsClick(item.goods_id)}
                  >
                    <View className="index-featured__side-image-placeholder" />
                    <View className="index-featured__info">
                      <Text className="index-featured__name" numberOfLines={2}>{item.goods_name}</Text>
                      <Text className="index-featured__price">¥{(item.price / 100).toFixed(2)}</Text>
                    </View>
                  </View>
                ))}
              </View>
            </View>
          ) : (
            <View className="index-featured-empty">
              <Text className="caption">暂无精选内容</Text>
            </View>
          )}
        </View>

        {/* 商品列表（同精选页） */}
        <View className="index-section">
          <View className="index-section__header">
            <Text className="eyebrow">更多推荐</Text>
            <Text
              className="caption"
              onClick={() => Taro.switchTab({ url: '/pages/goods_list/index' })}
            >
              查看全部 →
            </Text>
          </View>

          {newArrivals.length > 0 ? (
            <View className="goods-grid">
              {newArrivals.map(item => (
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
          ) : (
            <View className="index-section__empty">
              <Text className="caption">暂无商品</Text>
            </View>
          )}
        </View>
      </View>

      <TabBar items={TAB_BAR_ITEMS} />
    </View>
  )
}
