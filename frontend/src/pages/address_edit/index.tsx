import React, { useState } from 'react'
import { View, Text, Input } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { Button } from '../../components/Button'
import './index.css'

interface AddressForm {
  receiver_name: string
  receiver_mobile: string
  province: string
  city: string
  district: string
  address: string
}

export default function AddressEdit() {
  const editId = (Taro.getCurrentInstance().router?.params as { id?: string })?.id
  const isEdit = Boolean(editId)

  const [form, setForm] = useState<AddressForm>({
    receiver_name: '',
    receiver_mobile: '',
    province: '',
    city: '',
    district: '',
    address: ''
  })
  const [submitting, setSubmitting] = useState(false)

  function updateField(key: keyof AddressForm, value: string) {
    setForm(prev => ({ ...prev, [key]: value }))
  }

  function validate(): boolean {
    if (!form.receiver_name.trim()) {
      Taro.showToast({ title: '请输入收货人姓名', icon: 'none' })
      return false
    }
    if (!form.receiver_mobile.trim() || !/^1\d{10}$/.test(form.receiver_mobile)) {
      Taro.showToast({ title: '请输入正确的手机号', icon: 'none' })
      return false
    }
    if (!form.province.trim() || !form.city.trim() || !form.district.trim()) {
      Taro.showToast({ title: '请选择省市区', icon: 'none' })
      return false
    }
    if (!form.address.trim()) {
      Taro.showToast({ title: '请输入详细地址', icon: 'none' })
      return false
    }
    return true
  }

  async function handleSubmit() {
    if (!validate()) return
    setSubmitting(true)
    try {
      // TODO: 调用后端地址创建/编辑接口
      // if (isEdit) {
      //   await addressApi.update(Number(editId), form)
      // } else {
      //   await addressApi.create(form)
      // }
      Taro.showToast({ title: '保存成功', icon: 'success' })
      setTimeout(() => Taro.navigateBack(), 1500)
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <View className="page-address-edit">
      <NavBar title={isEdit ? '编辑地址' : '新增地址'} showBack />

      <View className="form">
        <View className="form__group">
          <Text className="form__label">收货人</Text>
          <Input
            className="form__input"
            placeholder="请输入收货人姓名"
            value={form.receiver_name}
            onInput={e => updateField('receiver_name', e.detail.value)}
          />
        </View>

        <View className="form__group">
          <Text className="form__label">手机号</Text>
          <Input
            className="form__input"
            type="number"
            placeholder="请输入手机号"
            maxlength={11}
            value={form.receiver_mobile}
            onInput={e => updateField('receiver_mobile', e.detail.value)}
          />
        </View>

        <View className="form__group">
          <Text className="form__label">省市区</Text>
          <View className="form__region">
            <Input
              className="form__input form__input--region"
              placeholder="省"
              value={form.province}
              onInput={e => updateField('province', e.detail.value)}
            />
            <Input
              className="form__input form__input--region"
              placeholder="市"
              value={form.city}
              onInput={e => updateField('city', e.detail.value)}
            />
            <Input
              className="form__input form__input--region"
              placeholder="区"
              value={form.district}
              onInput={e => updateField('district', e.detail.value)}
            />
          </View>
        </View>

        <View className="form__group">
          <Text className="form__label">详细地址</Text>
          <Input
            className="form__input"
            placeholder="街道、门牌号等"
            value={form.address}
            onInput={e => updateField('address', e.detail.value)}
          />
        </View>

        <View className="form__submit">
          <Button
            type="primary"
            loading={submitting}
            onClick={handleSubmit}
          >
            保存地址
          </Button>
        </View>
      </View>
    </View>
  )
}
