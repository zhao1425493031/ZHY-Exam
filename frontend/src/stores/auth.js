import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const isLoggedIn = computed(() => !!token.value && !!user.value)

  // 计算属性
  const userRole = computed(() => user.value?.role || '')
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isUser = computed(() => ['admin', 'user'].includes(user.value?.role))

  // 登录
  const loginAction = async (credentials) => {
    try {
      const response = await authApi.login(credentials)
      token.value = response.data.token
      user.value = response.data.user
      
      // 保存到本地存储
      localStorage.setItem('token', token.value)
      
      ElMessage.success('登录成功')
      return response
    } catch (error) {
      ElMessage.error(error.message || '登录失败')
      throw error
    }
  }

  // 注册
  const registerAction = async (userData) => {
    try {
      const response = await authApi.register(userData)
      ElMessage.success('注册成功，请登录')
      return response
    } catch (error) {
      ElMessage.error(error.message || '注册失败')
      throw error
    }
  }

  // 清除认证状态（不调用API）
  const clearAuth = () => {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
  }

  // 登出
  const logoutAction = async () => {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      // 清除状态
      clearAuth()
      ElMessage.success('已退出登录')
    }
  }

  // 获取用户信息
  const fetchProfile = async () => {
    try {
      const response = await authApi.getProfile()
      user.value = response.data
      return response
    } catch (error) {
      console.error('获取用户信息失败:', error)
      // 如果获取用户信息失败，直接清除登录状态（避免循环调用）
      clearAuth()
      throw error
    }
  }

  // 初始化用户信息
  const initUser = async () => {
    if (token.value && !user.value) {
      try {
        await fetchProfile()
      } catch (error) {
        console.error('初始化用户信息失败:', error)
      }
    }
  }

  // 更新用户信息
  const updateUser = (userData) => {
    user.value = { ...user.value, ...userData }
  }

  return {
    // 状态
    user,
    token,
    isLoggedIn,
    
    // 计算属性
    userRole,
    isAdmin,
    isUser,
    
    // 方法
    loginAction,
    registerAction,
    logoutAction,
    clearAuth,
    fetchProfile,
    initUser,
    updateUser
  }
})
