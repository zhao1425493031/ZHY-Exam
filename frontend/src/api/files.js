import request from './index'

// 文件API
export const fileApi = {
  // 上传文件
  uploadFile(file, relatedType = 'general', relatedId = null) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('related_type', relatedType)
    if (relatedId) {
      formData.append('related_id', relatedId)
    }
    
    return request.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 批量上传文件
  batchUploadFiles(files, relatedType = 'general', relatedId = null) {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })
    formData.append('related_type', relatedType)
    if (relatedId) {
      formData.append('related_id', relatedId)
    }
    
    return request.post('/files/batch-upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 获取文件信息
  getFile(fileId) {
    return request.get(`/files/${fileId}`)
  },

  // 下载文件
  downloadFile(fileId) {
    return request.get(`/files/${fileId}/download`, {
      responseType: 'blob'
    })
  },

  // 预览文件
  previewFile(fileId) {
    return request.get(`/files/${fileId}/preview`)
  },

  // 获取文件列表
  getFiles(params = {}) {
    return request.get('/files', { params })
  },

  // 更新文件信息
  updateFile(fileId, data) {
    return request.put(`/files/${fileId}`, data)
  },

  // 删除文件
  deleteFile(fileId) {
    return request.delete(`/files/${fileId}`)
  },

  // 批量删除文件
  batchDelete(data) {
    return request.delete('/files/batch-delete', data)
  },

  // 获取存储信息
  getStorageInfo() {
    return request.get('/files/storage-info')
  },

  // 清理无用文件（管理员）
  cleanupFiles() {
    return request.post('/files/cleanup')
  },

  // 获取允许的文件类型
  getAllowedTypes() {
    return request.get('/files/allowed-types')
  }
}
