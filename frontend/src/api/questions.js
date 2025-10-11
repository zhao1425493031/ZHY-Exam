import request from '@/utils/request'

// 试题管理API
export const questionApi = {
  // 获取试题列表
  getQuestions(params) {
    return request({
      url: '/questions',
      method: 'get',
      params
    })
  },

  // 创建试题
  createQuestion(data) {
    return request({
      url: '/questions',
      method: 'post',
      data
    })
  },

  // 获取试题详情
  getQuestion(id) {
    return request({
      url: `/questions/${id}`,
      method: 'get'
    })
  },

  // 更新试题
  updateQuestion(id, data) {
    return request({
      url: `/questions/${id}`,
      method: 'put',
      data
    })
  },

  // 删除试题
  deleteQuestion(id) {
    return request({
      url: `/questions/${id}`,
      method: 'delete'
    })
  },

  // 更新试题状态
  updateQuestionStatus(id, data) {
    return request({
      url: `/questions/${id}/status`,
      method: 'put',
      data
    })
  },

  // 获取试题类型列表
  getQuestionTypes() {
    return request({
      url: '/questions/types',
      method: 'get'
    })
  },

  // 获取试题难度列表
  getQuestionDifficulties() {
    return request({
      url: '/questions/difficulties',
      method: 'get'
    })
  },

  // 获取试题统计信息
  getQuestionStats() {
    return request({
      url: '/questions/stats',
      method: 'get'
    })
  },

  // 批量导入试题
  importQuestions(formData) {
    return request({
      url: '/import-export/questions/import',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 导出试题
  exportQuestions(params) {
    return request({
      url: '/questions/export',
      method: 'get',
      params,
      responseType: 'blob'
    })
  },

  // 获取导入模板
  getImportTemplate() {
    return request({
      url: '/questions/import-template',
      method: 'get',
      responseType: 'blob'
    })
  },

  // 批量删除试题
  batchDelete(data) {
    return request({
      url: '/questions/batch-delete',
      method: 'delete',
      data
    })
  },

  // 批量更新试题状态
  batchUpdateStatus(data) {
    return request({
      url: '/questions/batch-update-status',
      method: 'put',
      data
    })
  }
}
