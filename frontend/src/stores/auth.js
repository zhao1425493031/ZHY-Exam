import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const token = ref(localStorage.getItem('token') || '')
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const showLoginDialog = ref(false) // 登录弹窗显示状态

  // 计算属性
  const userRole = computed(() => user.value?.role || '')
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isUser = computed(() => ['admin', 'user'].includes(user.value?.role))

  // 登录
  const loginAction = async (credentials, skipRedirect = false) => {
    try {
      const response = await authApi.login(credentials)
      token.value = response.data.token
      user.value = response.data.user
      
      // 保存到本地存储
      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      
      ElMessage.success('登录成功')
      
      // 关闭登录弹窗
      closeLoginDialog()
      
      // 根据角色进行跳转（除非明确跳过）
      if (!skipRedirect) {
        // 如果在首页，根据角色跳转到对应的仪表盘
        if (router.currentRoute.value.path === '/' || router.currentRoute.value.path === '/courses') {
          if (user.value.role === 'admin') {
            router.push('/admin')
          } else {
            router.push('/user/dashboard')
          }
        } else {
          // 如果在其他页面，不刷新页面，让用户手动刷新或重新请求
          console.log('登录成功，当前页面:', router.currentRoute.value.path)
          ElMessage.info('登录成功，请重新操作')
        }
      }
      
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
    localStorage.removeItem('user')
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
      // 更新本地存储的用户信息
      localStorage.setItem('user', JSON.stringify(user.value))
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
    // 如果localStorage中已经有用户信息，直接使用
    if (token.value && user.value) {
      console.log('从localStorage恢复用户状态:', user.value)
      return
    }
    
    // 如果有token但没有用户信息，尝试从服务器获取
    if (token.value && !user.value) {
      try {
        console.log('正在从服务器恢复用户状态...')
        await fetchProfile()
        console.log('用户状态恢复成功:', user.value)
      } catch (error) {
        console.error('初始化用户信息失败:', error)
        // 如果token无效，清除认证状态
        clearAuth()
      }
    }
  }

  // 更新用户信息
  const updateUser = (userData) => {
    user.value = { ...user.value, ...userData }
  }

  // 显示登录弹窗
  const openLoginDialog = () => {
    showLoginDialog.value = true
  }

  // 关闭登录弹窗
  const closeLoginDialog = () => {
    showLoginDialog.value = false
  }

  return {
    // 状态
    user,
    token,
    isLoggedIn,
    showLoginDialog,
    
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
    updateUser,
    openLoginDialog,
    closeLoginDialog
  }
})
