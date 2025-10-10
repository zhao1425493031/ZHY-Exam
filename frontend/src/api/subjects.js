import request from '@/utils/request'

// 科目管理API
export const subjectsApi = {
  // 获取科目列表
  getSubjects(params) {
    return request({
      url: '/subjects',
      method: 'get',
      params
    })
  },

  // 创建科目
  createSubject(data) {
    return request({
      url: '/subjects',
      method: 'post',
      data
    })
  },

  // 获取科目详情
  getSubject(id) {
    return request({
      url: `/subjects/${id}`,
      method: 'get'
    })
  },

  // 更新科目
  updateSubject(id, data) {
    return request({
      url: `/subjects/${id}`,
      method: 'put',
      data
    })
  },

  // 删除科目
  deleteSubject(id) {
    return request({
      url: `/subjects/${id}`,
      method: 'delete'
    })
  },

  // 更新科目状态
  updateSubjectStatus(id, data) {
    return request({
      url: `/subjects/${id}/status`,
      method: 'put',
      data
    })
  },

  // 获取科目统计信息
  getSubjectStats() {
    return request({
      url: '/subjects/stats',
      method: 'get'
    })
  }
}
