import React from 'react'
import { View, Text } from '@tarojs/components'
import './navbar.css'

interface NavBarProps {
  title?: string
  showBack?: boolean
  onBack?: () => void
  right?: React.ReactNode
  className?: string
}

export function NavBar({ title = '', showBack = false, onBack, right, className = '' }: NavBarProps) {
  return (
    <View className={`nav-bar ${className}`}>
      <View className="nav-bar__inner">
        <View className="nav-bar__left">
          {showBack && (
            <View className="nav-bar__back" onClick={onBack}>
              <Text>←</Text>
            </View>
          )}
        </View>
        <View className="nav-bar__title">{title}</View>
        <View className="nav-bar__right">{right}</View>
      </View>
    </View>
  )
}
