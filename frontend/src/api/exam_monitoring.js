import request from './index'

const examMonitoringApi = {
  // 记录考试监控事件
  recordEvent(data) {
    return request.post('/exam-monitoring/events', data)
  },

  // 获取考试监控事件
  getExamEvents(examRecordId) {
    return request.get(`/exam-monitoring/${examRecordId}/events`)
  },

  // 获取可疑行为记录（管理员）
  getSuspiciousBehavior(params = {}) {
    return request.get('/exam-monitoring/suspicious-behavior', { params })
  },

  // 获取监控统计信息（管理员）
  getMonitoringStatistics(params = {}) {
    return request.get('/exam-monitoring/statistics', { params })
  },

  // 获取实时监控数据（管理员）
  getRealTimeMonitoring(examId) {
    return request.get(`/exam-monitoring/real-time/${examId}`)
  },

  // 获取监控告警（管理员）
  getMonitoringAlerts(params = {}) {
    return request.get('/exam-monitoring/alerts', { params })
  },

  // 处理监控告警（管理员）
  resolveAlert(alertId, data) {
    return request.put(`/exam-monitoring/alerts/${alertId}/resolve`, data)
  }
}

export { examMonitoringApi }
