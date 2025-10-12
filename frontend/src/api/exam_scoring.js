import request from './index'

const examScoringApi = {
  // 提交考试
  submitExam(examRecordId, data) {
    return request.post(`/exam-scoring/submit`, {
      exam_record_id: examRecordId,
      ...data
    })
  },

  // 获取考试结果
  getExamResult(examRecordId) {
    return request.get(`/exam-scoring/result/${examRecordId}`)
  },

  // 获取考试统计信息（管理员）
  getExamStatistics(examId) {
    return request.get(`/exam-scoring/statistics/${examId}`)
  },

  // 获取用户的考试记录
  getExamRecords(params = {}) {
    return request.get('/exam-scoring/records', { params })
  },

  // 获取用户的错题记录
  getWrongAnswers(params = {}) {
    return request.get('/exam-scoring/wrong-answers', { params })
  },

  // 标记错题为已复习
  reviewWrongAnswer(wrongAnswerId) {
    return request.post(`/exam-scoring/wrong-answers/${wrongAnswerId}/review`)
  },

  // 删除错题记录
  deleteWrongAnswer(wrongAnswerId) {
    return request.delete(`/exam-scoring/wrong-answers/${wrongAnswerId}`)
  },

  // 收藏题目
  favoriteQuestion(questionId) {
    return request.post(`/exam-scoring/questions/${questionId}/favorite`)
  },

  // 取消收藏题目
  unfavoriteQuestion(questionId) {
    return request.delete(`/exam-scoring/questions/${questionId}/favorite`)
  },

  // 获取题目收藏状态
  getFavoriteStatus(questionId) {
    return request.get(`/exam-scoring/questions/${questionId}/favorite/status`)
  }
}

export { examScoringApi }
