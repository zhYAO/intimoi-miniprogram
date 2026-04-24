import React, { useState } from 'react'
import { View, Text, Image } from '@tarojs/components'
import { useRouter } from '@tarojs/taro'
import { NavBar } from '../../components/NavBar'
import { Button } from '../../components/Button'
import { goodsApi, cartApi, GoodsDetail, GoodsSpec } from '../../utils/request'
import './index.css'

export default function GoodsDetailPage() {
  const { params } = useRouter<{ goodsId?: string }>()
  const goodsId = params?.goodsId || ''

  const [goods, setGoods] = useState<GoodsDetail | null>(null)
  const [selectedSpec, setSelectedSpec] = useState<GoodsSpec | null>(null)
  const [loading, setLoading] = useState(false)
  const [adding, setAdding] = useState(false)
  const [activeImageIndex, setActiveImageIndex] = useState(0)

  async function fetchDetail() {
    if (!goodsId) return
    setLoading(true)
    try {
      const res = await goodsApi.detail(goodsId)
      setGoods(res)
      if (res.specs.length > 0) {
        setSelectedSpec(res.specs[0])
      }
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setLoading(false)
    }
  }

  // 页面加载时获取数据（原生小程序用 onLoad，H5 用 useEffect）
  React.useEffect(() => {
    fetchDetail()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [goodsId])

  async function handleAddToCart() {
    if (!selectedSpec) {
      return
    }
    setAdding(true)
    try {
      await cartApi.add(goodsId, selectedSpec.spec_id, 1)
      // 临时成功提示（等后端部署后可换为真实接口）
      // eslint-disable-next-line no-alert
      alert('已加入购物车')
    } catch {
      // 错误已由 request 统一处理
    } finally {
      setAdding(false)
    }
  }

  return (
    <View className="page-goods-detail">
      <NavBar title="商品详情" showBack />

      {loading ? (
        <View className="goods-detail__loading">
          <Text className="caption">加载中...</Text>
        </View>
      ) : !goods ? (
        <View className="goods-detail__loading">
          <Text className="caption">商品不存在</Text>
        </View>
      ) : (
        <>
          {/* 商品图片 */}
          <View className="goods-detail__images">
            {goods.images.length > 0 ? (
              <Image
                className="goods-detail__image"
                src={goods.images[activeImageIndex]}
                mode="aspectFill"
              />
            ) : (
              <View className="goods-detail__image-placeholder" />
            )}
            {goods.images.length > 1 && (
              <View className="goods-detail__image-dots">
                {goods.images.map((_, i) => (
                  <View
                    key={i}
                    className={`goods-detail__dot ${i === activeImageIndex ? 'goods-detail__dot--active' : ''}`}
                    onClick={() => setActiveImageIndex(i)}
                  />
                ))}
              </View>
            )}
          </View>

          {/* 商品信息 */}
          <View className="goods-detail__info">
            <View className="goods-detail__price-row">
              <Text className="goods-detail__price">¥{goods.price}</Text>
              {goods.original_price > goods.price && (
                <Text className="goods-detail__original-price">¥{goods.original_price}</Text>
              )}
            </View>
            <Text className="goods-detail__title">{goods.goods_name}</Text>
            <View className="goods-detail__meta">
              <Text className="caption">库存 {goods.stock}</Text>
              <Text className="caption">已售 {goods.sales}</Text>
            </View>
          </View>

          <View className="divider goods-detail__divider" />

          {/* 规格选择 */}
          <View className="goods-detail__spec">
            <Text className="h4">选择规格</Text>
            <View className="goods-detail__spec-options">
              {goods.specs.map(spec => (
                <View
                  key={spec.spec_id}
                  className={`spec-tag ${selectedSpec?.spec_id === spec.spec_id ? 'spec-tag--active' : ''} ${spec.stock === 0 ? 'spec-tag--disabled' : ''}`}
                  onClick={() => spec.stock > 0 && setSelectedSpec(spec)}
                >
                  {spec.spec_name}
                  {spec.stock === 0 && '（缺货）'}
                </View>
              ))}
            </View>
          </View>

          <View className="divider goods-detail__divider" />

          {/* 商品详情 */}
          <View className="goods-detail__desc">
            <Text className="h4" style="margin-bottom: 12px">商品详情</Text>
            {/* 富文本内容渲染（简化处理） */}
            <View dangerouslySetInnerHTML={{ __html: goods.description || '' }} />
          </View>
        </>
      )}

      {/* 底部操作 */}
      <View className="goods-detail__actions">
        <View className="goods-detail__action-secondary">
          <Text className="caption">收藏</Text>
        </View>
        <Button
          type="primary"
          className="goods-detail__action-primary"
          disabled={!selectedSpec || selectedSpec.stock === 0}
          loading={adding}
          onClick={handleAddToCart}
        >
          {selectedSpec?.stock === 0 ? '暂时缺货' : '加入购物车'}
        </Button>
      </View>
    </View>
  )
}
