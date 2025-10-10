import request from '@/utils/request'

// 认证API
export const authApi = {
  // 用户登录
  login(data) {
    return request({
      url: '/api/auth/login',
      method: 'post',
      data
    })
  },

  // 用户注册
  register(data) {
    return request({
      url: '/api/auth/register',
      method: 'post',
      data
    })
  },

  // 用户登出
  logout() {
    return request({
      url: '/api/auth/logout',
      method: 'post'
    })
  },

  // 获取用户信息
  getProfile() {
    return request({
      url: '/api/auth/profile',
      method: 'get'
    })
  },

  // 更新用户信息
  updateProfile(data) {
    return request({
      url: '/api/auth/profile',
      method: 'put',
      data
    })
  },

  // 修改密码
  changePassword(data) {
    return request({
      url: '/api/auth/change-password',
      method: 'put',
      data
    })
  },

  // 刷新token
  refreshToken() {
    return request({
      url: '/api/auth/refresh',
      method: 'post'
    })
  }
}