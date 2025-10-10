// 主题管理
import { ref, computed } from 'vue'

// 主题配置
const themes = {
  light: {
    name: '浅色主题',
    primary: '#667eea',
    secondary: '#764ba2',
    background: '#ffffff',
    surface: '#f8f9fa',
    text: '#333333',
    textSecondary: '#666666',
    border: '#e0e0e0',
    shadow: 'rgba(0, 0, 0, 0.1)',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  dark: {
    name: '深色主题',
    primary: '#8b5cf6',
    secondary: '#a855f7',
    background: '#1a1a1a',
    surface: '#2d2d2d',
    text: '#ffffff',
    textSecondary: '#b3b3b3',
    border: '#404040',
    shadow: 'rgba(0, 0, 0, 0.3)',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)'
  },
  ocean: {
    name: '海洋主题',
    primary: '#06b6d4',
    secondary: '#0891b2',
    background: '#f0f9ff',
    surface: '#e0f2fe',
    text: '#0c4a6e',
    textSecondary: '#0369a1',
    border: '#bae6fd',
    shadow: 'rgba(6, 182, 212, 0.1)',
    gradient: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)'
  },
  forest: {
    name: '森林主题',
    primary: '#10b981',
    secondary: '#059669',
    background: '#f0fdf4',
    surface: '#dcfce7',
    text: '#064e3b',
    textSecondary: '#047857',
    border: '#bbf7d0',
    shadow: 'rgba(16, 185, 129, 0.1)',
    gradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
  }
}

// 当前主题
const currentTheme = ref('light')

// 获取当前主题配置
const getCurrentTheme = computed(() => themes[currentTheme.value])

// 切换主题
const setTheme = (themeName) => {
  if (themes[themeName]) {
    currentTheme.value = themeName
    localStorage.setItem('theme', themeName)
    applyTheme(themes[themeName])
  }
}

// 应用主题到CSS变量
const applyTheme = (theme) => {
  const root = document.documentElement
  // 设置data-theme属性
  root.setAttribute('data-theme', currentTheme.value)
  
  // 应用CSS变量
  Object.keys(theme).forEach(key => {
    if (key !== 'name') {
      root.style.setProperty(`--theme-${key}`, theme[key])
    }
  })
}

// 初始化主题
const initTheme = () => {
  const savedTheme = localStorage.getItem('theme') || 'light'
  if (themes[savedTheme]) {
    currentTheme.value = savedTheme
    applyTheme(themes[savedTheme])
  }
}

// 获取所有主题
const getAllThemes = () => Object.keys(themes).map(key => ({
  key,
  ...themes[key]
}))

// useTheme composable
const useTheme = () => {
  return {
    themes,
    currentTheme,
    getCurrentTheme,
    setTheme,
    initTheme,
    getAllThemes
  }
}

export {
  useTheme,
  themes,
  currentTheme,
  getCurrentTheme,
  setTheme,
  initTheme,
  getAllThemes
}
