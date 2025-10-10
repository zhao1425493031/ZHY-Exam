import request from './index'

// 公告API
export const announcementApi = {
  // 获取公告列表
  getAnnouncements(params = {}) {
    return request.get('/announcements', { params })
  },

  // 获取公开公告列表
  getPublicAnnouncements(params = {}) {
    return request.get('/announcements/public', { params })
  },

  // 获取单个公告详情
  getAnnouncement(announcementId) {
    return request.get(`/announcements/${announcementId}`)
  },

  // 获取公开公告详情
  getPublicAnnouncement(announcementId) {
    return request.get(`/announcements/${announcementId}/public`)
  },

  // 创建公告（管理员）
  createAnnouncement(data) {
    return request.post('/announcements', data)
  },

  // 更新公告（管理员）
  updateAnnouncement(announcementId, data) {
    return request.put(`/announcements/${announcementId}`, data)
  },

  // 删除公告（管理员）
  deleteAnnouncement(announcementId) {
    return request.delete(`/announcements/${announcementId}`)
  },

  // 发布公告（管理员）
  publishAnnouncement(announcementId) {
    return request.put(`/announcements/${announcementId}/publish`)
  },

  // 取消发布公告（管理员）
  unpublishAnnouncement(announcementId) {
    return request.put(`/announcements/${announcementId}/unpublish`)
  },

  // 批量发布公告（管理员）
  batchPublish(data) {
    return request.put('/announcements/batch-publish', data)
  },

  // 批量删除公告（管理员）
  batchDelete(data) {
    return request.delete('/announcements/batch-delete', data)
  },

  // 获取公告统计（管理员）
  getStatistics() {
    return request.get('/announcements/statistics')
  }
}
