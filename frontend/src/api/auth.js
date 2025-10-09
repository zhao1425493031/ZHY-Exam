import request from './index'

// 认证相关 API
export const authApi = {
  // 用户登录
  login: (data) => request.post('/auth/login', data),
  
  // 用户注册
  register: (data) => request.post('/auth/register', data),
  
  // 用户登出
  logout: () => request.post('/auth/logout'),
  
  // 获取用户信息
  getProfile: () => request.get('/auth/profile'),
  
  // 更新用户信息
  updateProfile: (data) => request.put('/auth/profile', data),
  
  // 修改密码
  changePassword: (data) => request.put('/auth/change-password', data)
}

// 用户管理 API
export const usersApi = {
  // 获取用户列表
  getUsers: (params) => request.get('/users', { params }),
  
  // 获取用户详情
  getUser: (id) => request.get(`/users/${id}`),
  
  // 创建用户
  createUser: (data) => request.post('/users', data),
  
  // 更新用户
  updateUser: (id, data) => request.put(`/users/${id}`, data),
  
  // 删除用户
  deleteUser: (id) => request.delete(`/users/${id}`),
  
  // 批量删除用户
  batchDeleteUsers: (ids) => request.delete('/users/batch', { data: { ids } })
}

// 科目管理 API
export const subjectsApi = {
  // 获取科目列表
  getSubjects: (params) => request.get('/subjects', { params }),
  
  // 获取科目详情
  getSubject: (id) => request.get(`/subjects/${id}`),
  
  // 创建科目
  createSubject: (data) => request.post('/subjects', data),
  
  // 更新科目
  updateSubject: (id, data) => request.put(`/subjects/${id}`, data),
  
  // 删除科目
  deleteSubject: (id) => request.delete(`/subjects/${id}`)
}

// 试题管理 API
export const questionsApi = {
  // 获取试题列表
  getQuestions: (params) => request.get('/questions', { params }),
  
  // 获取试题详情
  getQuestion: (id) => request.get(`/questions/${id}`),
  
  // 创建试题
  createQuestion: (data) => request.post('/questions', data),
  
  // 更新试题
  updateQuestion: (id, data) => request.put(`/questions/${id}`, data),
  
  // 删除试题
  deleteQuestion: (id) => request.delete(`/questions/${id}`),
  
  // 批量导入试题
  batchImport: (data) => request.post('/questions/batch-import', data),
  
  // 导出试题
  exportQuestions: (params) => request.get('/questions/export', { params, responseType: 'blob' })
}

// 考试管理 API
export const examsApi = {
  // 获取考试列表
  getExams: (params) => request.get('/exams', { params }),
  
  // 获取考试详情
  getExam: (id) => request.get(`/exams/${id}`),
  
  // 创建考试
  createExam: (data) => request.post('/exams', data),
  
  // 更新考试
  updateExam: (id, data) => request.put(`/exams/${id}`, data),
  
  // 删除考试
  deleteExam: (id) => request.delete(`/exams/${id}`),
  
  // 开始考试
  startExam: (id) => request.post(`/exams/${id}/start`),
  
  // 提交考试
  submitExam: (id, data) => request.post(`/exams/${id}/submit`, data)
}

// 考试记录 API
export const examRecordsApi = {
  // 获取考试记录列表
  getExamRecords: (params) => request.get('/exam-records', { params }),
  
  // 获取考试记录详情
  getExamRecord: (id) => request.get(`/exam-records/${id}`),
  
  // 获取考试答案
  getExamAnswers: (id) => request.get(`/exam-records/${id}/answers`)
}

// 导出所有 API
export {
  authApi as login,
  authApi as register,
  authApi as logout,
  authApi as getProfile,
  usersApi as users,
  subjectsApi as subjects,
  questionsApi as questions,
  examsApi as exams,
  examRecordsApi as examRecords
}
