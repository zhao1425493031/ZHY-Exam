import request from '@/utils/request'

// 用户管理API
export const usersApi = {
  // 获取用户列表
  getUsers(params = {}) {
    return request({
      url: '/users',
      method: 'get',
      params
    })
  },

  // 获取用户详情
  getUser(id) {
    return request({
      url: `/users/${id}`,
      method: 'get'
    })
  },

  // 创建用户
  createUser(data) {
    return request({
      url: '/users',
      method: 'post',
      data
    })
  },

  // 更新用户
  updateUser(id, data) {
    return request({
      url: `/users/${id}`,
      method: 'put',
      data
    })
  },

  // 删除用户
  deleteUser(id) {
    return request({
      url: `/users/${id}`,
      method: 'delete'
    })
  },

  // 切换用户状态
  toggleUserStatus(id, status) {
    return request({
      url: `/users/${id}/status`,
      method: 'put',
      data: { status }
    })
  },

  // 批量删除用户
  batchDeleteUsers(ids) {
    return request({
      url: '/users/batch',
      method: 'delete',
      data: { ids }
    })
  },

  // 导出用户数据
  exportUsers(params = {}) {
    return request({
      url: '/import-export/users/export',
      method: 'get',
      params,
      responseType: 'blob'
    })
  },

  // 更新个人资料
  updateProfile(data) {
    return request({
      url: '/auth/profile',
      method: 'put',
      data
    })
  }
}
