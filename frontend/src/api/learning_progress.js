import request from './index'

// 学习进度API
export const learningProgressApi = {
  // 获取学习概览
  getOverview() {
    return request.get('/learning-progress/overview')
  },

  // 获取学习进度
  getProgress(params = {}) {
    return request.get('/learning-progress/progress', { params })
  },

  // 获取学习统计
  getStatistics(params = {}) {
    return request.get('/learning-progress/statistics', { params })
  },

  // 获取学习成就
  getAchievements() {
    return request.get('/learning-progress/achievements')
  },

  // 生成学习报告
  generateReport(params = {}) {
    return request.get('/learning-progress/report', { params })
  },

  // 获取学习建议
  getRecommendations() {
    return request.get('/learning-progress/recommendations')
  },

  // 获取学习目标
  getGoals() {
    return request.get('/learning-progress/goals')
  },

  // 创建学习目标
  createGoal(data) {
    return request.post('/learning-progress/goals', data)
  },

  // 更新学习目标
  updateGoal(goalId, data) {
    return request.put(`/learning-progress/goals/${goalId}`, data)
  },

  // 删除学习目标
  deleteGoal(goalId) {
    return request.delete(`/learning-progress/goals/${goalId}`)
  }
}
