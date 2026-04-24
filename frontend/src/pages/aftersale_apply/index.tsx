import React, { useState } from 'react'
import { View, Text, Input } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { Button } from '../../components/Button'
import './index.css'

type AftersaleType = '退款' | '退货' | '换货'

export default function AftersaleApply() {
  const { params } = Taro.getCurrentInstance().router!
  const orderId = (params as { orderId?: string }).orderId || ''

  const [type, setType] = useState<AftersaleType>('退款')
  const [reason, setReason] = useState('')
  const [description, setDescription] = useState('')
  const [submitting, setSubmitting] = useState(false)

  function validate(): boolean {
    if (!reason.trim()) {
      Taro.showToast({ title: '请选择退款原因', icon: 'none' })
      return false
    }
    if (!description.trim()) {
      Taro.showToast({ title: '请填写问题说明', icon: 'none' })
      return false
    }
    return true
  }

  async function handleSubmit() {
    if (!validate()) return
    setSubmitting(true)
    try {
      // TODO: 调用后端售后申请接口
      // await aftersaleApi.apply({ order_id: orderId, type, reason, description })
      Taro.showToast({ title: '申请已提交', icon: 'success' })
      setTimeout(() => Taro.navigateBack(), 1500)
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setSubmitting(false)
    }
  }

  const REASON_OPTIONS = ['商品破损', '商品错发', '商品与描述不符', '收到商品不喜欢', '其他']

  return (
    <View className="page-aftersale-apply">
      <NavBar title="申请售后" showBack />

      <View className="page-aftersale-apply__content">
        {/* 售后类型 */}
        <View className="apply-section">
          <Text className="form__label">售后类型</Text>
          <View className="apply-type-options">
            {(['退款', '退货', '换货'] as AftersaleType[]).map(t => (
              <View
                key={t}
                className={`apply-type-option ${type === t ? 'apply-type-option--active' : ''}`}
                onClick={() => setType(t)}
              >
                <Text className="apply-type-option__text">{t}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* 退款原因 */}
        <View className="apply-section">
          <Text className="form__label">退款原因</Text>
          <View className="apply-reason-options">
            {REASON_OPTIONS.map(r => (
              <View
                key={r}
                className={`apply-reason-option ${reason === r ? 'apply-reason-option--active' : ''}`}
                onClick={() => setReason(r)}
              >
                <Text className="apply-reason-option__text">{r}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* 问题说明 */}
        <View className="apply-section">
          <Text className="form__label">问题说明</Text>
          <View className="apply-desc">
            <Input
              className="apply-desc__input"
              placeholder="请详细描述您遇到的问题（选填）"
              value={description}
              onInput={e => setDescription(e.detail.value)}
              maxlength={200}
            />
            <Text className="apply-desc__count">{description.length}/200</Text>
          </View>
        </View>

        {/* 凭证 */}
        <View className="apply-section">
          <Text className="form__label">上传凭证（选填）</Text>
          <View className="apply-upload">
            <View className="apply-upload__placeholder">
              <Text className="caption">+ 添加图片</Text>
            </View>
          </View>
        </View>

        <View className="apply-submit">
          <Button
            type="primary"
            loading={submitting}
            onClick={handleSubmit}
          >
            提交申请
          </Button>
        </View>
      </View>
    </View>
  )
}
