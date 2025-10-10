import request from './index'

// 权限API
export const permissionApi = {
  // 获取权限列表
  getPermissions(params = {}) {
    return request.get('/permissions', { params })
  },

  // 获取权限树
  getPermissionTree() {
    return request.get('/permissions/tree')
  },

  // 获取单个权限详情
  getPermission(permissionId) {
    return request.get(`/permissions/${permissionId}`)
  },

  // 创建权限
  createPermission(data) {
    return request.post('/permissions', data)
  },

  // 更新权限
  updatePermission(permissionId, data) {
    return request.put(`/permissions/${permissionId}`, data)
  },

  // 删除权限
  deletePermission(permissionId) {
    return request.delete(`/permissions/${permissionId}`)
  },

  // 获取角色权限
  getRolePermissions(role) {
    return request.get(`/permissions/role/${role}`)
  },

  // 设置角色权限
  setRolePermissions(role, data) {
    return request.post(`/permissions/role/${role}`, data)
  },

  // 移除角色权限
  removeRolePermission(role, permissionId) {
    return request.delete(`/permissions/role/${role}/${permissionId}`)
  },

  // 获取用户权限
  getUserPermissions(userId) {
    return request.get(`/permissions/user/${userId}`)
  },

  // 检查用户权限
  checkPermission(data) {
    return request.post('/permissions/check', data)
  },

  // 获取用户菜单权限
  getUserMenu() {
    return request.get('/permissions/menu')
  },

  // 初始化权限数据
  initPermissions() {
    return request.post('/permissions/init')
  }
}
