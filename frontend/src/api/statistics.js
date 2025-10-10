import request from './index'

// 统计分析API
export const statisticsApi = {
  // 获取仪表盘统计数据
  getDashboardStatistics() {
    return request.get('/statistics/dashboard')
  },

  // 获取考试数据统计（管理员）
  getExamStatistics(params = {}) {
    return request.get('/statistics/exam-data', { params })
  },

  // 获取用户行为统计（管理员）
  getUserBehaviorStatistics(params = {}) {
    return request.get('/statistics/user-behavior', { params })
  },

  // 获取试题分析统计（管理员）
  getQuestionAnalysis(params = {}) {
    return request.get('/statistics/question-analysis', { params })
  },

  // 获取成绩分布统计（管理员）
  getScoreDistribution(params = {}) {
    return request.get('/statistics/score-distribution', { params })
  },

  // 获取学习进度统计
  getLearningProgressStatistics(params = {}) {
    return request.get('/statistics/learning-progress', { params })
  },

  // 获取成绩趋势统计
  getPerformanceTrends(params = {}) {
    return request.get('/statistics/performance-trends', { params })
  },

  // 获取科目表现统计
  getSubjectPerformance() {
    return request.get('/statistics/subject-performance')
  },

  // 获取薄弱环节分析
  getWeakAreas(params = {}) {
    return request.get('/statistics/weak-areas', { params })
  },

  // 获取成绩对比统计
  getPerformanceComparison(params = {}) {
    return request.get('/statistics/comparison', { params })
  },

  // 导出统计数据（管理员）
  exportStatistics(params = {}) {
    return request.get('/statistics/export', { params })
  }
}
