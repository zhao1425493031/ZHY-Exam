import request from './index'

export const favoritesApi = {
  // 获取收藏的题目列表
  getFavoriteQuestions(params = {}) {
    return request.get('/exam-scoring/favorites', { params })
  },

  // 收藏题目
  addFavorite(questionId) {
    return request.post(`/exam-scoring/questions/${questionId}/favorite`)
  },

  // 取消收藏
  removeFavorite(questionId) {
    return request.delete(`/exam-scoring/questions/${questionId}/favorite`)
  },

  // 检查收藏状态
  checkFavoriteStatus(questionId) {
    return request.get(`/exam-scoring/questions/${questionId}/favorite/status`)
  },

  // 批量取消收藏
  batchRemoveFavorites(questionIds) {
    return request.delete('/exam-scoring/favorites/batch', {
      data: { question_ids: questionIds }
    })
  },

  // 获取收藏统计
  getFavoriteStatistics() {
    return request.get('/exam-scoring/favorites/statistics')
  }
}
