import React from 'react'
import { View, Text } from '@tarojs/components'
import './tabbar.css'

export interface TabBarItem {
  pagePath: string
  text: string
  badge?: number
}

interface TabBarProps { items: TabBarItem[] }

export function TabBar({ items }: TabBarProps) {
  const currentPath = '/' + (items[0]?.pagePath.split('/')[1] || '')

  return (
    <View className="tab-bar">
      <View className="tab-bar__inner">
        {items.map((item) => (
          <View
            key={item.pagePath}
            className={`tab-bar__item ${currentPath === `/${item.pagePath.split('/')[1]}` ? 'tab-bar__item--active' : ''}`}
          >
            <View className="tab-bar__icon"><Text>○</Text></View>
            <Text className="tab-bar__text">{item.text}</Text>
            {item.badge && item.badge > 0 && (
              <View className="tab-bar__badge">{item.badge > 99 ? '99+' : item.badge}</View>
            )}
          </View>
        ))}
      </View>
    </View>
  )
}
