import React, { useState, useEffect } from 'react'
import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { useDidShow } from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { TabBar } from '../../components/TabBar'
import { memberApi } from '../../utils/request'
import './index.css'

const TAB_BAR_ITEMS = [
  { pagePath: 'pages/index/index', text: '发现', icon: 'home' },
  { pagePath: 'pages/category/index', text: '分类', icon: 'grid' },
  { pagePath: 'pages/cart/index', text: '购物车', icon: 'cart' },
  { pagePath: 'pages/profile/index', text: '我的', icon: 'user' }
]

const MENU_ITEMS = [
  { key: 'orders', label: '我的订单', url: '/pages/order/index' },
  { key: 'address', label: '收货地址', url: '/pages/address/index' },
  { key: 'favorites', label: '我的收藏', url: '/pages/favorites/index' }
]

const LEVEL_MAP: Record<number, string> = {
  1: '普通会员',
  2: '银卡会员',
  3: '金卡会员'
}

export default function Profile() {
  const [member, setMember] = useState<{
    nickname: string
    avatar_url: string
    level: number
    phone: string
  } | null>(null)
  const [loading, setLoading] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  async function fetchMemberInfo() {
    const token = Taro.getStorageSync('token')
    if (!token) {
      setIsLoggedIn(false)
      return
    }
    setLoading(true)
    try {
      const res = await memberApi.getInfo()
      setMember(res)
      setIsLoggedIn(true)
    } catch {
      setIsLoggedIn(false)
    } finally {
      setLoading(false)
    }
  }

  useDidShow(() => {
    fetchMemberInfo()
  })

  async function handleWxLogin() {
    // 微信小程序登录
    try {
      const loginRes = await Taro.login()
      if (!loginRes.code) return

      // 调用后端登录接口
      const res = await memberApi.login(loginRes.code)
      Taro.setStorageSync('token', res.token)
      Taro.setStorageSync('member_id', res.member_id)
      Taro.setStorageSync('open_id', res.open_id)
      setIsLoggedIn(true)
      fetchMemberInfo()
    } catch (err) {
      console.error('登录失败', err)
    }
  }

  return (
    <View className="page-profile">
      <NavBar title="我的" />

      <View className="page-profile__content">
        {/* 用户信息区 */}
        {isLoggedIn && member ? (
          <View className="profile-header">
            <View className="profile-avatar">
              {member.avatar_url
                ? <View className="profile-avatar__img" />
                : <Text className="profile-avatar__placeholder">{member.nickname?.[0] || '用'}</Text>
              }
            </View>
            <View className="profile-info">
              <Text className="profile-info__name">{member.nickname || '用户'}</Text>
              <Text className="caption">{LEVEL_MAP[member.level] || '普通会员'}</Text>
            </View>
          </View>
        ) : (
          <View className="profile-header profile-header--guest" onClick={handleWxLogin}>
            <View className="profile-avatar">
              <Text className="profile-avatar__placeholder">登</Text>
            </View>
            <View className="profile-info">
              <Text className="profile-info__name">点击登录</Text>
              <Text className="caption">微信快捷登录</Text>
            </View>
          </View>
        )}

        {/* 会员卡 */}
        <View className="profile-member-card">
          <View>
            <Text className="eyebrow" style="color: rgba(255,255,255,0.6)">intimoi 会员</Text>
            <Text className="profile-member-card__tier">
              {isLoggedIn && member ? LEVEL_MAP[member.level] || '普通会员' : '未登录'}
            </Text>
          </View>
          <Text style="color: rgba(255,255,255,0.6); font-size: 12px">→</Text>
        </View>

        {/* 菜单 */}
        <View className="profile-menu">
          {MENU_ITEMS.map(item => (
            <View
              key={item.key}
              className="profile-menu__item"
              onClick={() => item.url && Taro.navigateTo({ url: item.url })}
            >
              <Text className="profile-menu__label">{item.label}</Text>
              <Text className="profile-menu__arrow">›</Text>
            </View>
          ))}
        </View>
      </View>

      <TabBar items={TAB_BAR_ITEMS} />
    </View>
  )
}
