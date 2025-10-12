/**
 * 考试记录 API
 */
import request from '@/utils/request'

export const examRecordsApi = {
  // 获取考试记录列表
  getExamRecords(params = {}) {
    return request({
      url: '/exam-records',
      method: 'get',
      params
    })
  },

  // 获取单个考试记录
  getExamRecord(id) {
    return request({
      url: `/exam-records/${id}`,
      method: 'get'
    })
  },

  // 获取用户的考试记录
  getUserExamRecords(userId, params = {}) {
    return request({
      url: `/exam-records/user/${userId}`,
      method: 'get',
      params
    })
  },

  // 获取考试的记录列表
  getExamRecordsByExam(examId, params = {}) {
    return request({
      url: `/exam-records/exam/${examId}`,
      method: 'get',
      params
    })
  },

  // 删除考试记录
  deleteExamRecord(id) {
    return request({
      url: `/exam-records/${id}`,
      method: 'delete'
    })
  }
}
