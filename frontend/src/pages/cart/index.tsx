import React, { useState } from 'react'
import { View, Text, Image } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { useDidShow } from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { TabBar } from '../../components/TabBar'
import { Button } from '../../components/Button'
import { cartApi, CartItem } from '../../utils/request'
import './index.css'

const TAB_BAR_ITEMS = [
  { pagePath: 'pages/index/index', text: '发现', icon: 'home' },
  { pagePath: 'pages/category/index', text: '分类', icon: 'grid' },
  { pagePath: 'pages/cart/index', text: '购物车', icon: 'cart' },
  { pagePath: 'pages/profile/index', text: '我的', icon: 'user' }
]

export default function Cart() {
  const [items, setItems] = useState<CartItem[]>([])
  const [totalAmount, setTotalAmount] = useState(0)
  const [allSelected, setAllSelected] = useState(false)
  const [loading, setLoading] = useState(false)
  const [updating, setUpdating] = useState<number | null>(null)

  async function fetchCart() {
    setLoading(true)
    try {
      const res = await cartApi.get()
      setItems(res.items)
      setTotalAmount(res.total_amount)
      setAllSelected(res.items.every(item => item.selected))
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  useDidShow(() => {
    fetchCart()
  })

  async function handleToggleSelect(item: CartItem) {
    // 乐观更新
    setItems(prev =>
      prev.map(i => i.id === item.id ? { ...i, selected: !i.selected } : i)
    )
  }

  async function handleUpdateNum(item: CartItem, newNum: number) {
    if (newNum < 0) return
    setUpdating(item.id)
    try {
      if (newNum === 0) {
        await cartApi.remove(item.id)
        setItems(prev => prev.filter(i => i.id !== item.id))
      } else {
        await cartApi.updateNum(item.id, newNum)
        setItems(prev =>
          prev.map(i => i.id === item.id ? { ...i, num: newNum } : i)
        )
      }
      // 重新计算总价
      const res = await cartApi.get()
      setTotalAmount(res.total_amount)
    } catch {
      fetchCart() // 回滚
    } finally {
      setUpdating(null)
    }
  }

  async function handleSelectAll() {
    const newSelected = !allSelected
    setAllSelected(newSelected)
    try {
      await cartApi.selectAll(newSelected)
      setItems(prev => prev.map(i => ({ ...i, selected: newSelected })))
    } catch {
      setAllSelected(!newSelected)
      fetchCart()
    }
  }

  const selectedItems = items.filter(i => i.selected)
  const selectedAmount = selectedItems.reduce((sum, i) => sum + i.price * i.num, 0)

  return (
    <View className="page-cart">
      <NavBar title={`购物车 ${items.length}`} />

      <View className="page-cart__content">
        {loading ? (
          <View className="cart-loading">
            <Text className="caption">加载中...</Text>
          </View>
        ) : items.length === 0 ? (
          <View className="cart-empty">
            <Text className="cart-empty__icon">□</Text>
            <Text className="caption">购物车为空</Text>
            <View style="margin-top: 16px">
              <Button type="secondary" size="sm" onClick={() => {}}>去精选</Button>
            </View>
          </View>
        ) : (
          <>
            {/* 全选 */}
            <View className="cart-select-all" onClick={handleSelectAll}>
              <View className={`cart-checkbox ${allSelected ? 'cart-checkbox--checked' : ''}`} />
              <Text className="caption">全选</Text>
            </View>

            {/* 商品列表 */}
            <View className="cart-list">
              {items.map(item => (
                <View key={item.id} className="cart-item">
                  <View
                    className={`cart-checkbox ${item.selected ? 'cart-checkbox--checked' : ''}`}
                    onClick={() => handleToggleSelect(item)}
                  />
                  <View className="cart-item__image-wrap">
                    {item.thumbnail ? (
                      <Image className="cart-item__image" src={item.thumbnail} mode="aspectFill" />
                    ) : (
                      <View className="cart-item__image cart-item__image--placeholder" />
                    )}
                  </View>
                  <View className="cart-item__info">
                    <Text className="cart-item__name">{item.goods_name}</Text>
                    <Text className="caption cart-item__spec">{item.spec_name}</Text>
                    <View className="cart-item__bottom">
                      <Text className="cart-item__price">¥{item.price}</Text>
                      <View className="cart-item__num">
                        <View
                          className="cart-item__num-btn"
                          onClick={() => handleUpdateNum(item, item.num - 1)}
                        >−</View>
                        <Text className="cart-item__num-text">{item.num}</Text>
                        <View
                          className="cart-item__num-btn"
                          onClick={() => handleUpdateNum(item, item.num + 1)}
                        >+</View>
                      </View>
                    </View>
                    {item.stock < 10 && (
                      <Text className="cart-item__stock-warning">库存紧张</Text>
                    )}
                  </View>
                </View>
              ))}
            </View>

            {/* 底部结算 */}
            <View className="cart-footer">
              <View className="cart-footer__info">
                <Text className="caption">合计</Text>
                <Text className="cart-footer__total">¥{selectedAmount}</Text>
              </View>
              <Button
                type="primary"
                disabled={selectedItems.length === 0}
                onClick={() => Taro.navigateTo({ url: '/pages/order_confirm/index' })}
              >
                结算 {selectedItems.length > 0 && `(${selectedItems.length})`}
              </Button>
            </View>
          </>
        )}
      </View>

      <TabBar items={TAB_BAR_ITEMS} />
    </View>
  )
}
