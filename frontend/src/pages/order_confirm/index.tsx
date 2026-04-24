import React, { useState, useEffect } from 'react'
import { View, Text, Image, Input } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { Button } from '../../components/Button'
import { cartApi, addressApi } from '../../utils/request'
import './index.css'

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

interface CartItemForConfirm {
  id: number
  goods_id: number
  goods_name: string
  spec_name: string
  price: number
  num: number
  goods_img: string
  selected: boolean
}

export default function OrderConfirm() {
  const [address, setAddress] = useState<Address | null>(null)
  const [cartItems, setCartItems] = useState<CartItemForConfirm[]>([])
  const [goodsAmount, setGoodsAmount] = useState(0)
  const [freight, setFreight] = useState(0)
  const [remark, setRemark] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function fetchData() {
    try {
      // 获取默认地址
      // const addrRes = await addressApi.getDefault()
      // setAddress(addrRes)

      // 获取已选购物车商品
      const cartRes = await cartApi.get()
      const selected = cartRes.items.filter((item: CartItemForConfirm) => item.selected)
      setCartItems(selected)

      const total = selected.reduce((sum: number, item: CartItemForConfirm) => {
        return sum + item.price * item.num
      }, 0)
      setGoodsAmount(total)
      // 运费规则：满300免运费，暂定
      setFreight(total >= 30000 ? 0 : 1000)
    } catch {
      // 错误已由 request 统一处理
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  function handleAddAddress() {
    Taro.navigateTo({ url: '/pages/address/index' })
  }

  function handleEditAddress() {
    if (address) {
      Taro.navigateTo({ url: `/pages/address_edit/index?id=${address.id}` })
    }
  }

  async function handleSubmit() {
    if (!address) {
      Taro.showToast({ title: '请先添加收货地址', icon: 'none' })
      return
    }
    if (cartItems.length === 0) {
      Taro.showToast({ title: '请选择商品', icon: 'none' })
      return
    }
    setSubmitting(true)
    try {
      // TODO: 调用后端提交订单接口
      // await orderApi.submit({
      //   address_id: address.id,
      //   remark,
      //   items: cartItems.map(item => ({
      //     goods_id: item.goods_id,
      //     spec_name: item.spec_name,
      //     price: item.price,
      //     num: item.num
      //   }))
      // })
      Taro.showToast({ title: '订单提交成功', icon: 'success' })
      setTimeout(() => {
        Taro.redirectTo({ url: '/pages/order/index' })
      }, 1500)
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <View className="page-order-confirm">
      <NavBar title="确认订单" showBack />

      <View className="page-order-confirm__content">
        {/* 收货地址 */}
        {address ? (
          <View className="confirm-section confirm-address" onClick={handleEditAddress}>
            <View className="confirm-address__info">
              <View className="confirm-address__top">
                <Text className="confirm-address__name">{address.receiver_name}</Text>
                <Text className="confirm-address__mobile">{address.receiver_mobile}</Text>
              </View>
              <Text className="confirm-address__detail">
                {address.province}{address.city}{address.district}{address.address}
              </Text>
            </View>
            <Text className="confirm-address__arrow">›</Text>
          </View>
        ) : (
          <View className="confirm-section confirm-address confirm-address--empty" onClick={handleAddAddress}>
            <Text className="confirm-address__empty-text">添加收货地址</Text>
            <Text className="confirm-address__arrow">›</Text>
          </View>
        )}

        <View className="divider" />

        {/* 商品清单 */}
        <View className="confirm-section confirm-goods">
          <View className="confirm-goods__header">
            <Text className="eyebrow">商品清单</Text>
          </View>
          {cartItems.length === 0 ? (
            <View className="confirm-goods__empty">
              <Text className="caption">暂无选中的商品</Text>
            </View>
          ) : (
            cartItems.map(item => (
              <View key={item.id} className="confirm-goods__item">
                <View className="confirm-goods__image-placeholder" />
                <View className="confirm-goods__info">
                  <Text className="confirm-goods__name" numberOfLines={2}>{item.goods_name}</Text>
                  <Text className="caption">{item.spec_name}</Text>
                </View>
                <View className="confirm-goods__right">
                  <Text className="confirm-goods__price">¥{(item.price / 100).toFixed(2)}</Text>
                  <Text className="caption">x{item.num}</Text>
                </View>
              </View>
            ))
          )}
        </View>

        <View className="divider" />

        {/* 配送信息 */}
        <View className="confirm-section confirm-delivery">
          <Text className="form__label">配送方式</Text>
          <Text className="confirm-delivery__value">快递</Text>
        </View>

        <View className="divider" />

        {/* 订单备注 */}
        <View className="confirm-section confirm-remark">
          <Text className="form__label">订单备注</Text>
          <Input
            className="confirm-remark__input"
            placeholder="订单备注（选填）"
            value={remark}
            onInput={e => setRemark(e.detail.value)}
            maxlength={100}
          />
        </View>

        <View className="divider" />

        {/* 价格明细 */}
        <View className="confirm-section confirm-prices">
          <View className="confirm-prices__row">
            <Text className="caption">商品总额</Text>
            <Text className="confirm-prices__value">¥{(goodsAmount / 100).toFixed(2)}</Text>
          </View>
          <View className="confirm-prices__row">
            <Text className="caption">运费</Text>
            <Text className="confirm-prices__value">
              {freight === 0 ? '免运费' : `¥${(freight / 100).toFixed(2)}`}
            </Text>
          </View>
          <View className="confirm-prices__row confirm-prices__row--total">
            <Text className="confirm-prices__label">应付总额</Text>
            <Text className="confirm-prices__total">¥{((goodsAmount + freight) / 100).toFixed(2)}</Text>
          </View>
        </View>
      </View>

      {/* 底部提交 */}
      <View className="confirm-submit">
        <View className="confirm-submit__total">
          <Text className="caption">合计</Text>
          <Text className="confirm-submit__amount">¥{((goodsAmount + freight) / 100).toFixed(2)}</Text>
        </View>
        <Button
          type="primary"
          className="confirm-submit__btn"
          loading={submitting}
          onClick={handleSubmit}
        >
          提交订单
        </Button>
      </View>
    </View>
  )
}
