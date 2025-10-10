import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

// 创建 axios 实例
const request = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 添加认证 token
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    // 统一处理响应数据
    const { data } = response
    
    // 如果返回的数据结构是 { code, message, data }
    if (data && typeof data === 'object' && 'code' in data) {
      if (data.code === 200) {
        return data
      } else {
        ElMessage.error(data.message || '请求失败')
        return Promise.reject(new Error(data.message || '请求失败'))
      }
    }
    
    return data
  },
  error => {
    console.error('响应错误:', error)
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // 未授权，清除登录状态
          const authStore = useAuthStore()
          authStore.logoutAction()
          ElMessage.error('登录已过期，请重新登录')
          break
        case 403:
          ElMessage.error('权限不足')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 422:
          ElMessage.error(data.message || '数据验证失败')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(data.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络连接失败')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

// 导出所有API模块
export { questionApi } from './questions'
export { subjectsApi } from './subjects'
export { authApi } from './auth'
export { examApi } from './exams'
export { examScoringApi } from './exam_scoring'
export { examMonitoringApi } from './exam_monitoring'
export { learningProgressApi } from './learning_progress'
export { notificationApi } from './notifications'
export { fileApi } from './files'
export { announcementApi } from './announcements'
export { permissionApi } from './permissions'
export { importExportApi } from './import_export'
export { statisticsApi } from './statistics'

export default request
