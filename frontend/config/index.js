const config = {
  projectName: 'intimoi-miniprogram',
  date: '2026-04-24',
  designWidth: 375,
  deviceRatio: { 640: 2.34 / 1, 750: 1, 828: 1 / 1.81, 375: 2 },
  sourceRoot: 'src',
  outputRoot: 'dist',
  framework: 'react',
  mini: { compile: { include: [] } },
  h5: {
    publicPath: '/',
    staticDirectory: 'static',
    postcss: { autoprefixer: { enable: true, config: {} } }
  }
}
module.exports = config
