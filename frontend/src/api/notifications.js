import request from './index'

// 通知API
export const notificationApi = {
  // 获取通知列表
  getNotifications(params = {}) {
    return request.get('/notifications', { params })
  },

  // 获取单个通知详情
  getNotification(notificationId) {
    return request.get(`/notifications/${notificationId}`)
  },

  // 标记通知为已读
  markAsRead(notificationId) {
    return request.put(`/notifications/${notificationId}/read`)
  },

  // 批量标记通知为已读
  batchMarkAsRead(data) {
    return request.put('/notifications/batch-read', data)
  },

  // 删除通知
  deleteNotification(notificationId) {
    return request.delete(`/notifications/${notificationId}`)
  },

  // 批量删除通知
  batchDelete(data) {
    return request.delete('/notifications/batch-delete', data)
  },

  // 获取未读通知数量
  getUnreadCount() {
    return request.get('/notifications/unread-count')
  },

  // 发送通知（管理员）
  sendNotification(data) {
    return request.post('/notifications/send', data)
  },

  // 发送通知给指定用户（管理员）
  sendNotificationToUser(data) {
    return request.post('/notifications/send-to-user', data)
  },

  // 发送通知给所有用户（管理员）
  sendNotificationToAll(data) {
    return request.post('/notifications/send-to-all', data)
  },

  // 获取用户通知设置
  getNotificationSettings() {
    return request.get('/notifications/settings')
  },

  // 更新用户通知设置
  updateNotificationSettings(settings) {
    return request.put('/notifications/settings', settings)
  }
}
