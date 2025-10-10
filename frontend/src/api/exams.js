import request from '@/utils/request'

// 考试管理API
export const examApi = {
  // 获取考试列表
  getExams(params) {
    return request({
      url: '/api/exams',
      method: 'get',
      params
    })
  },

  // 创建考试
  createExam(data) {
    return request({
      url: '/api/exams',
      method: 'post',
      data
    })
  },

  // 获取考试详情
  getExam(id) {
    return request({
      url: `/api/exams/${id}`,
      method: 'get'
    })
  },

  // 更新考试
  updateExam(id, data) {
    return request({
      url: `/api/exams/${id}`,
      method: 'put',
      data
    })
  },

  // 删除考试
  deleteExam(id) {
    return request({
      url: `/api/exams/${id}`,
      method: 'delete'
    })
  },

  // 更新考试状态
  updateExamStatus(id, data) {
    return request({
      url: `/api/exams/${id}/status`,
      method: 'put',
      data
    })
  },

  // 获取考试统计信息
  getExamStats(id) {
    return request({
      url: `/api/exams/${id}/stats`,
      method: 'get'
    })
  },

  // 批量更新考试状态
  batchUpdateStatus(data) {
    return request({
      url: '/api/exams/batch-update-status',
      method: 'put',
      data
    })
  },

  // 批量删除考试
  batchDelete(data) {
    return request({
      url: '/api/exams/batch-delete',
      method: 'delete',
      data
    })
  },

  // 创建随机考试
  createRandomExam(data) {
    return request({
      url: '/api/exams/random',
      method: 'post',
      data
    })
  },

  // 从模板创建考试
  createExamFromTemplate(templateId, data) {
    return request({
      url: `/api/exams/template/${templateId}`,
      method: 'post',
      data
    })
  },

  // 验证考试配置
  validateExamConfig(data) {
    return request({
      url: '/api/exams/validate-config',
      method: 'post',
      data
    })
  },

  // 计算考试时长
  calculateExamDuration(data) {
    return request({
      url: '/api/exams/calculate-duration',
      method: 'post',
      data
    })
  },

  // 检查考试可用性
  checkExamAvailability(id) {
    return request({
      url: `/api/exams/${id}/availability`,
      method: 'get'
    })
  }
}
