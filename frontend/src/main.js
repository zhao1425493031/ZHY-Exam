import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

import App from './App.vue'
import router from './router'
import './styles/index.scss'
import './styles/theme.css'
import { initTheme } from './composables/useTheme'
import { useAuthStore } from './stores/auth'

// 完全抑制 ResizeObserver 错误
window.addEventListener('error', (e) => {
  if (e.message && e.message.includes('ResizeObserver')) {
    e.preventDefault()
    e.stopImmediatePropagation()
    return false
  }
})

// 抑制未捕获的Promise错误
window.addEventListener('unhandledrejection', (e) => {
  if (e.reason && e.reason.message && e.reason.message.includes('ResizeObserver')) {
    e.preventDefault()
    return false
  }
})

// 抑制console错误
const originalError = console.error
console.error = (...args) => {
  if (args[0] && typeof args[0] === 'string' && args[0].includes('ResizeObserver')) {
    return
  }
  originalError.apply(console, args)
}

const app = createApp(App)
const pinia = createPinia()

// 注册 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(pinia)
app.use(router)
app.use(ElementPlus, {
  locale: zhCn,
})

// 初始化主题
initTheme()

// 检查并清理过期的认证状态
const authStore = useAuthStore()
// 清除所有可能的过期状态，避免401循环
authStore.clearAuth()

app.mount('#app')
