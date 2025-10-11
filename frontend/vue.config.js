const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,

  // 开发服务器配置
  devServer: {
    port: 8081,
    open: true,
    hot: true,
    client: {
      overlay: {
        warnings: false,
        errors: true
      },
      webSocketURL: {
        hostname: 'localhost',
        pathname: '/ws',
        port: 8081,
        protocol: 'ws'
      },
      // 解决 WebSocket 连接问题
      logging: 'warn'
    },
    // 解决跨域问题（可选，因为后端已配置CORS）
    proxy: {
      '/api': {
        target: 'http://localhost:9999',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  },

  // 生产环境配置
  publicPath: process.env.NODE_ENV === 'production' ? '/examsphere/' : '/',
  outputDir: 'dist',
  assetsDir: 'static',
  productionSourceMap: false,

  // Webpack 配置
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          },
          elementPlus: {
            name: 'chunk-element-plus',
            test: /[\\/]node_modules[\\/]element-plus[\\/]/,
            priority: 20,
            chunks: 'all'
          }
        }
      }
    },
    // 抑制 ResizeObserver 错误
    plugins: [
      new (require('webpack')).DefinePlugin({
        'process.env': {
          NODE_ENV: JSON.stringify(process.env.NODE_ENV || 'development')
        }
      })
    ]
  },
  
  // CSS 配置
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  }
})
