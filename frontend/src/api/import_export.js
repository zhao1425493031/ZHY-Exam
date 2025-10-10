import request from './index'

// 导入导出API
export const importExportApi = {
  // 导入用户数据
  importUsers(file) {
    const formData = new FormData()
    formData.append('file', file)
    
    return request.post('/import-export/users/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 导入科目数据
  importSubjects(file) {
    const formData = new FormData()
    formData.append('file', file)
    
    return request.post('/import-export/subjects/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 导入试题数据
  importQuestions(file, subjectId) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('subject_id', subjectId)
    
    return request.post('/import-export/questions/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 导出用户数据
  exportUsers(params = {}) {
    return request.get('/import-export/users/export', {
      params,
      responseType: 'blob'
    })
  },

  // 导出科目数据
  exportSubjects(params = {}) {
    return request.get('/import-export/subjects/export', {
      params,
      responseType: 'blob'
    })
  },

  // 导出试题数据
  exportQuestions(params = {}) {
    return request.get('/import-export/questions/export', {
      params,
      responseType: 'blob'
    })
  },

  // 导出考试结果数据
  exportExamResults(params = {}) {
    return request.get('/import-export/exam-results/export', {
      params,
      responseType: 'blob'
    })
  },

  // 导出统计数据
  exportStatistics(params = {}) {
    return request.get('/import-export/statistics/export', {
      params,
      responseType: 'blob'
    })
  },

  // 下载用户导入模板
  downloadUserTemplate() {
    return request.get('/import-export/templates/users', {
      responseType: 'blob'
    })
  },

  // 下载科目导入模板
  downloadSubjectTemplate() {
    return request.get('/import-export/templates/subjects', {
      responseType: 'blob'
    })
  },

  // 下载试题导入模板
  downloadQuestionTemplate() {
    return request.get('/import-export/templates/questions', {
      responseType: 'blob'
    })
  },

  // 获取导入记录
  getImportRecords(params = {}) {
    return request.get('/import-export/records', { params })
  },

  // 通用下载模板方法
  downloadTemplate(type) {
    const templateMap = {
      users: this.downloadUserTemplate,
      subjects: this.downloadSubjectTemplate,
      questions: this.downloadQuestionTemplate
    }
    
    const downloadFn = templateMap[type]
    if (downloadFn) {
      return downloadFn()
    } else {
      throw new Error(`不支持的模板类型: ${type}`)
    }
  },

  // 通用导出数据方法
  exportData(type, params = {}) {
    const exportMap = {
      users: this.exportUsers,
      subjects: this.exportSubjects,
      questions: this.exportQuestions,
      'exam-results': this.exportExamResults,
      statistics: this.exportStatistics
    }
    
    const exportFn = exportMap[type]
    if (exportFn) {
      return exportFn(params)
    } else {
      throw new Error(`不支持的导出类型: ${type}`)
    }
  }
}
