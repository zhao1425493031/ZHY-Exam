import request from '@/utils/request'

// 考试管理API
export const examApi = {
  // 获取考试列表
  getExams(params) {
    return request({
      url: '/exams',
      method: 'get',
      params
    })
  },

  // 创建考试
  createExam(data) {
    return request({
      url: '/exams',
      method: 'post',
      data
    })
  },

  // 获取考试详情
  getExam(id) {
    return request({
      url: `/exams/${id}`,
      method: 'get'
    })
  },

  // 更新考试
  updateExam(id, data) {
    return request({
      url: `/exams/${id}`,
      method: 'put',
      data
    })
  },

  // 删除考试
  deleteExam(id) {
    return request({
      url: `/exams/${id}`,
      method: 'delete'
    })
  },

  // 更新考试状态
  updateExamStatus(id, data) {
    return request({
      url: `/exams/${id}/status`,
      method: 'put',
      data
    })
  },

  // 获取考试统计信息
  getExamStats(id) {
    return request({
      url: `/exams/${id}/stats`,
      method: 'get'
    })
  },

  // 批量更新考试状态
  batchUpdateStatus(data) {
    return request({
      url: '/exams/batch-update-status',
      method: 'put',
      data
    })
  },

  // 批量删除考试
  batchDelete(data) {
    return request({
      url: '/exams/batch-delete',
      method: 'delete',
      data
    })
  },

  // 创建随机考试
  createRandomExam(data) {
    return request({
      url: '/exams/random',
      method: 'post',
      data
    })
  },

  // 从模板创建考试
  createExamFromTemplate(templateId, data) {
    return request({
      url: `/exams/template/${templateId}`,
      method: 'post',
      data
    })
  },

  // 验证考试配置
  validateExamConfig(data) {
    return request({
      url: '/exams/validate-config',
      method: 'post',
      data
    })
  },

  // 计算考试时长
  calculateExamDuration(data) {
    return request({
      url: '/exams/calculate-duration',
      method: 'post',
      data
    })
  },

  // 开始考试
  startExam(examId) {
    return request({
      url: `/exams/${examId}/start`,
      method: 'post'
    })
  },

  // 提交考试
  submitExam(examId, data) {
    return request({
      url: `/exams/${examId}/submit`,
      method: 'post',
      data
    })
  },

  // 检查考试是否可以参加
  checkExamAvailability(id) {
    return request({
      url: `/exams/${id}/check-availability`,
      method: 'get'
    })
  },

  // 导出考试
  exportExams(params) {
    return request({
      url: '/import-export/exams/export',
      method: 'get',
      params,
      responseType: 'blob'
    })
  },

  // 获取考试分析数据
  getExamAnalysis(params) {
    return request({
      url: '/exams/analysis',
      method: 'get',
      params
    })
  },

  // 获取考试结果
  getExamResult(examId) {
    return request({
      url: `/exams/${examId}/result`,
      method: 'get'
    })
  }
}
