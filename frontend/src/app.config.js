export default {
  pages: [
    'pages/index/index',
    'pages/goods_list/index',
    'pages/goods_detail/index',
    'pages/cart/index',
    'pages/order/index',
    'pages/profile/index'
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: 'rgba(255,255,255,0.5)',
    navigationBarTitleText: 'intimoi',
    navigationStyle: 'custom',
    backgroundColor: '#F5F1FA'
  },
  tabBar: {
    custom: true,
    color: '#8E8A96',
    selectedColor: '#6B5B8E',
    backgroundColor: 'rgba(255,255,255,0.5)',
    borderStyle: 'black',
    list: [
      { pagePath: 'pages/index/index', text: '首页' },
      { pagePath: 'pages/goods_list/index', text: '精选' },
      { pagePath: 'pages/cart/index', text: '购物车' },
      { pagePath: 'pages/profile/index', text: '我的' }
    ]
  }
}
