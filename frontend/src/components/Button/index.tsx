import React from 'react'
import { View } from '@tarojs/components'
import './button.css'

interface ButtonProps {
  type?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  block?: boolean
  disabled?: boolean
  loading?: boolean
  onClick?: () => void
  children?: React.ReactNode
  className?: string
}

export function Button({
  type = 'primary',
  size = 'md',
  block = false,
  disabled = false,
  loading = false,
  onClick,
  children,
  className = ''
}: ButtonProps) {
  const classes = [
    'btn',
    `btn--${type}`,
    size !== 'md' ? `btn--${size}` : '',
    block ? 'btn--block' : '',
    loading ? 'btn--loading' : '',
    className
  ].filter(Boolean).join(' ')

  return (
    <View className={classes} onClick={disabled || loading ? undefined : onClick}>
      {loading ? '...' : children}
    </View>
  )
}
