import React, { useState } from 'react'
import { View, Text } from '@tarojs/components'
import { NavBar } from '../../components/NavBar'
import { TabBar } from '../../components/TabBar'
import './index.css'

const TAB_BAR_ITEMS = [
  { pagePath: 'pages/index/index', text: '发现', icon: 'home' },
  { pagePath: 'pages/category/index', text: '分类', icon: 'grid' },
  { pagePath: 'pages/cart/index', text: '购物车', icon: 'cart' },
  { pagePath: 'pages/profile/index', text: '我的', icon: 'user' }
]

interface FavoriteItem {
  id: number
  goods_id: number
  goods_name: string
  price: number
  original_price: number
  goods_img: string
  created_at: string
}

export default function Favorites() {
  const [favorites, setFavorites] = useState<FavoriteItem[]>([])
  const [loading, setLoading] = useState(false)

  async function fetchFavorites() {
    setLoading(true)
    try {
      // TODO: 调用后端收藏列表接口
      // const res = await favoriteApi.list()
      // setFavorites(res.items)
      setFavorites([])
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  React.useEffect(() => {
    fetchFavorites()
  }, [])

  function handleRemove(item: FavoriteItem) {
    // TODO: 调用后端取消收藏接口
    setFavorites(prev => prev.filter(f => f.id !== item.id))
  }

  return (
    <View className="page-favorites">
      <NavBar title="我的收藏" showBack />

      <View className="page-favorites__content">
        {loading ? (
          <View className="favorites-loading">
            <Text className="caption">加载中...</Text>
          </View>
        ) : favorites.length === 0 ? (
          <View className="favorites-empty">
            <Text className="caption">暂无收藏商品</Text>
          </View>
        ) : (
          <View className="favorites-grid">
            {favorites.map(item => (
              <View key={item.id} className="favorite-card">
                <View className="favorite-card__image-placeholder" />
                <View className="favorite-card__info">
                  <Text className="favorite-card__name" numberOfLines={2}>{item.goods_name}</Text>
                  <View className="favorite-card__price-row">
                    <Text className="favorite-card__price">¥{(item.price / 100).toFixed(2)}</Text>
                    {item.original_price > item.price && (
                      <Text className="favorite-card__original-price">
                        ¥{(item.original_price / 100).toFixed(2)}
                      </Text>
                    )}
                  </View>
                </View>
                <Text
                  className="favorite-card__remove"
                  onClick={() => handleRemove(item)}
                >
                  取消收藏
                </Text>
              </View>
            ))}
          </View>
        )}
      </View>

      <TabBar items={TAB_BAR_ITEMS} />
    </View>
  )
}
