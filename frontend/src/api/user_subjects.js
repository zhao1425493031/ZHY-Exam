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
  }
}
