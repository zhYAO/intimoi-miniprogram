import React from 'react'
import { View } from '@tarojs/components'
import './styles/global.css'

export function App({ children }: { children: React.ReactNode }) {
  return <View id="app" className="glow-bg">{children}</View>
}
