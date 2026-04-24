import React, { useState } from 'react'
import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { TabBar } from '../../components/TabBar'
import { Button } from '../../components/Button'
import './index.css'

const TAB_BAR_ITEMS = [
  { pagePath: 'pages/index/index', text: '发现', icon: 'home' },
  { pagePath: 'pages/category/index', text: '分类', icon: 'grid' },
  { pagePath: 'pages/cart/index', text: '购物车', icon: 'cart' },
  { pagePath: 'pages/profile/index', text: '我的', icon: 'user' }
]

interface Address {
  id: number
  receiver_name: string
  receiver_mobile: string
  province: string
  city: string
  district: string
  address: string
  is_default: number
}

export default function Address() {
  const [addresses, setAddresses] = useState<Address[]>([])
  const [loading, setLoading] = useState(false)

  async function fetchAddresses() {
    setLoading(true)
    try {
      // TODO: 调用后端地址列表接口
      // const res = await addressApi.list()
      // setAddresses(res.items)
      setAddresses([])
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  React.useEffect(() => {
    fetchAddresses()
  }, [])

  function handleAdd() {
    Taro.navigateTo({ url: '/pages/address_edit/index' })
  }

  function handleEdit(addr: Address) {
    Taro.navigateTo({ url: `/pages/address_edit/index?id=${addr.id}` })
  }

  function handleSetDefault(addr: Address) {
    // TODO: 调用后端设置默认地址接口
    setAddresses(prev =>
      prev.map(a => ({ ...a, is_default: a.id === addr.id ? 1 : 0 }))
    )
  }

  function handleDelete(addr: Address) {
    Taro.showModal({
      title: '确认删除',
      content: '确定要删除该收货地址吗？',
      success: res => {
        if (res.confirm) {
          // TODO: 调用后端删除接口
          setAddresses(prev => prev.filter(a => a.id !== addr.id))
        }
      }
    })
  }

  return (
    <View className="page-address">
      <NavBar title="收货地址" showBack />

      <View className="page-address__content">
        {loading ? (
          <View className="address-loading">
            <Text className="caption">加载中...</Text>
          </View>
        ) : addresses.length === 0 ? (
          <View className="address-empty">
            <Text className="caption">暂无收货地址</Text>
          </View>
        ) : (
          <View className="address-list">
            {addresses.map(addr => (
              <View key={addr.id} className="address-card">
                <View className="address-card__info" onClick={() => handleEdit(addr)}>
                  <View className="address-card__top">
                    <Text className="address-card__name">{addr.receiver_name}</Text>
                    <Text className="address-card__mobile">{addr.receiver_mobile}</Text>
                    {addr.is_default === 1 && (
                      <Text className="address-card__default">默认</Text>
                    )}
                  </View>
                  <Text className="address-card__detail">
                    {addr.province}{addr.city}{addr.district}{addr.address}
                  </Text>
                </View>
                <View className="address-card__actions">
                  <Text
                    className="address-card__action"
                    onClick={() => handleSetDefault(addr)}
                  >
                    {addr.is_default === 1 ? '✓ 已默认' : '设为默认'}
                  </Text>
                  <Text
                    className="address-card__action"
                    onClick={() => handleEdit(addr)}
                  >
                    编辑
                  </Text>
                  <Text
                    className="address-card__action address-card__action--danger"
                    onClick={() => handleDelete(addr)}
                  >
                    删除
                  </Text>
                </View>
              </View>
            ))}
          </View>
        )}

        <View className="address-add">
          <Button type="primary" onClick={handleAdd}>
            新增收货地址
          </Button>
        </View>
      </View>

      <TabBar items={TAB_BAR_ITEMS} />
    </View>
  )
}
