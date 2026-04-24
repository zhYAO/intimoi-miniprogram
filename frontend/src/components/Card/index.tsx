import React from 'react'
import { View } from '@tarojs/components'
import './card.css'

interface CardProps {
  variant?: 'default' | 'bordered' | 'elevated'
  children?: React.ReactNode
  className?: string
  onClick?: () => void
}

export function Card({
  variant = 'default',
  children,
  className = '',
  onClick
}: CardProps) {
  const classes = [
    'card',
    variant !== 'default' ? `card--${variant}` : '',
    className
  ].filter(Boolean).join(' ')

  return (
    <View className={classes} onClick={onClick}>
      {children}
    </View>
  )
}
