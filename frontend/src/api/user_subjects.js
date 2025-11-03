import request from './index'

export const userSubjectsApi = {
  // 获取用户订阅的科目列表
  getUserSubjects(params = {}) {
    return request({
      url: '/user-subjects',
      method: 'get',
      params
    })
  },

  // 订阅科目
  subscribeSubject(data) {
    return request({
      url: '/user-subjects/subscribe',
      method: 'post',
      data
    })
  },

  // 取消订阅科目
  unsubscribeSubject(data) {
    return request({
      url: '/user-subjects/unsubscribe',
      method: 'post',
      data
    })
  },

  // 检查用户是否已订阅指定科目
  checkSubscription(subjectId) {
    return request({
      url: `/user-subjects/check/${subjectId}`,
      method: 'get'
    })
  },

  // ==================== 管理员接口 ====================
  
  // 管理员获取所有用户课程关联列表
  adminGetUserSubjects(params = {}) {
    return request({
      url: '/user-subjects/admin',
      method: 'get',
      params
    })
  },

  // 管理员创建用户课程关联
  adminCreateUserSubject(data) {
    return request({
      url: '/user-subjects/admin',
      method: 'post',
      data
    })
  },

  // 管理员删除用户课程关联
  adminDeleteUserSubject(userSubjectId) {
    return request({
      url: `/user-subjects/admin/${userSubjectId}`,
      method: 'delete'
    })
  },

  // 管理员更新用户课程关联状态
  adminUpdateUserSubjectStatus(userSubjectId, status) {
    return request({
      url: `/user-subjects/admin/${userSubjectId}/status`,
      method: 'put',
      data: { status }
    })
  }
}
