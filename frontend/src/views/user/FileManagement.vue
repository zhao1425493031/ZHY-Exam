<template>
  <div class="file-management">
    <div class="page-header">
      <h1>文件管理</h1>
      <div class="header-info">
        <el-tag type="info">总文件数: {{ storageInfo.total_count || 0 }}</el-tag>
        <el-tag type="warning">已用空间: {{ storageInfo.total_size_formatted || '0 B' }}</el-tag>
      </div>
    </div>

    <!-- 存储信息 -->
    <div class="storage-info">
      <el-card>
        <div class="storage-header">
          <h3>存储信息</h3>
          <div class="storage-usage">
            <el-progress
              :percentage="storageUsagePercentage"
              :color="getStorageColor(storageUsagePercentage)"
              :show-text="false"
            />
            <span class="usage-text">
              {{ storageInfo.total_size_formatted || '0 B' }} / {{ storageInfo.max_size_formatted || '100 MB' }}
            </span>
          </div>
        </div>
        <div class="storage-stats">
          <el-row :gutter="20">
            <el-col :span="6" v-for="(stats, type) in storageInfo.type_stats" :key="type">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon :color="getTypeColor(type)">
                    <component :is="getTypeIcon(type)" />
                  </el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.count }}</div>
                  <div class="stat-label">{{ getTypeLabel(type) }}</div>
                  <div class="stat-size">{{ formatFileSize(stats.size) }}</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>

    <!-- 文件上传 -->
    <div class="upload-section">
      <el-card>
        <div class="upload-header">
          <h3>文件上传</h3>
          <div class="upload-controls">
            <el-button type="primary" @click="showUploadDialog = true">
              <el-icon><Upload /></el-icon>
              上传文件
            </el-button>
            <el-button @click="showBatchUploadDialog = true">
              <el-icon><UploadFilled /></el-icon>
              批量上传
            </el-button>
          </div>
        </div>
        <div class="upload-info">
          <p>支持的文件类型: 图片、文档、视频、音频、压缩包</p>
          <p>单个文件最大: {{ allowedTypes.max_file_size_formatted }}</p>
        </div>
      </el-card>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-card>
        <el-form :model="searchForm" inline>
          <el-form-item label="关键词">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索文件名"
              clearable
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item label="文件类型">
            <el-select
              v-model="searchForm.file_type"
              placeholder="选择类型"
              clearable
              style="width: 120px"
            >
              <el-option label="图片" value="image" />
              <el-option label="文档" value="application" />
              <el-option label="视频" value="video" />
              <el-option label="音频" value="audio" />
            </el-select>
          </el-form-item>
          <el-form-item label="关联类型">
            <el-select
              v-model="searchForm.related_type"
              placeholder="选择关联类型"
              clearable
              style="width: 120px"
            >
              <el-option label="通用" value="general" />
              <el-option label="题目" value="question" />
              <el-option label="考试" value="exam" />
              <el-option label="用户" value="user" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="handleReset">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 文件列表 -->
    <div class="files-list">
      <el-card>
        <div class="list-header">
          <div class="list-title">
            <span>文件列表</span>
            <el-tag v-if="selectedFiles.length > 0" type="info">
              已选择 {{ selectedFiles.length }} 个文件
            </el-tag>
          </div>
          <div class="list-actions" v-if="selectedFiles.length > 0">
            <el-button size="small" @click="batchDownload">
              <el-icon><Download /></el-icon>
              批量下载
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete">
              <el-icon><Delete /></el-icon>
              批量删除
            </el-button>
          </div>
        </div>

        <!-- 文件网格视图 -->
        <div class="files-grid" v-if="viewMode === 'grid'">
          <div
            v-for="file in files"
            :key="file.id"
            class="file-item"
            @click="selectFile(file)"
            :class="{ 'file-selected': isFileSelected(file) }"
          >
            <div class="file-preview">
              <div v-if="file.file_type?.startsWith('image/')" class="image-preview">
                <img :src="getFilePreviewUrl(file)" :alt="file.original_name" />
              </div>
              <div v-else class="file-icon">
                <el-icon :size="48" :color="getFileIconColor(file)">
                  <component :is="getFileIcon(file)" />
                </el-icon>
              </div>
            </div>
            <div class="file-info">
              <div class="file-name" :title="file.original_name">
                {{ file.original_name }}
              </div>
              <div class="file-meta">
                <span class="file-size">{{ file.file_size_formatted }}</span>
                <span class="file-date">{{ formatDate(file.created_at) }}</span>
              </div>
              <div class="file-actions">
                <el-button size="small" @click.stop="downloadFile(file)">
                  <el-icon><Download /></el-icon>
                </el-button>
                <el-button size="small" @click.stop="previewFile(file)" v-if="canPreview(file)">
                  <el-icon><View /></el-icon>
                </el-button>
                <el-button size="small" type="danger" @click.stop="deleteFile(file)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 文件列表视图 -->
        <el-table
          v-else
          :data="files"
          :loading="loading"
          @selection-change="handleSelectionChange"
          row-key="id"
          stripe
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="original_name" label="文件名" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="file-name-cell">
                <el-icon :color="getFileIconColor(row)">
                  <component :is="getFileIcon(row)" />
                </el-icon>
                <span>{{ row.original_name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="file_size_formatted" label="大小" width="100" />
          <el-table-column prop="file_type" label="类型" width="120" />
          <el-table-column prop="related_type" label="关联类型" width="100" />
          <el-table-column prop="download_count" label="下载次数" width="100" />
          <el-table-column prop="created_at" label="上传时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="downloadFile(row)">
                下载
              </el-button>
              <el-button size="small" type="primary" @click="previewFile(row)" v-if="canPreview(row)">
                预览
              </el-button>
              <el-dropdown @command="(command) => handleAction(command, row)">
                <el-button size="small">
                  更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">编辑信息</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除文件</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            :current-page="pagination.page"
            :page-size="pagination.size"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 文件上传对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传文件"
      width="500px"
    >
      <el-upload
        ref="uploadRef"
        :action="uploadUrl"
        :headers="uploadHeaders"
        :data="uploadData"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
        :show-file-list="false"
        drag
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持的文件类型: 图片、文档、视频、音频、压缩包
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" @click="submitUpload">确定</el-button>
      </template>
    </el-dialog>

    <!-- 批量上传对话框 -->
    <el-dialog
      v-model="showBatchUploadDialog"
      title="批量上传文件"
      width="600px"
    >
      <el-upload
        ref="batchUploadRef"
        :action="uploadUrl"
        :headers="uploadHeaders"
        :data="uploadData"
        :on-success="handleBatchUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
        multiple
        :file-list="batchFileList"
      >
        <el-button type="primary">
          <el-icon><Upload /></el-icon>
          选择文件
        </el-button>
        <template #tip>
          <div class="el-upload__tip">
            支持批量上传多个文件
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="showBatchUploadDialog = false">取消</el-button>
        <el-button type="primary" @click="submitBatchUpload">确定</el-button>
      </template>
    </el-dialog>

    <!-- 文件预览对话框 -->
    <el-dialog
      v-model="showPreviewDialog"
      title="文件预览"
      width="80%"
    >
      <div v-if="previewingFile" class="file-preview-content">
        <div v-if="previewingFile.file_type?.startsWith('image/')" class="image-preview">
          <img :src="getFilePreviewUrl(previewingFile)" :alt="previewingFile.original_name" />
        </div>
        <div v-else class="file-info-preview">
          <div class="preview-icon">
            <el-icon :size="64" :color="getFileIconColor(previewingFile)">
              <component :is="getFileIcon(previewingFile)" />
            </el-icon>
          </div>
          <div class="preview-details">
            <h3>{{ previewingFile.original_name }}</h3>
            <p>文件大小: {{ previewingFile.file_size_formatted }}</p>
            <p>文件类型: {{ previewingFile.file_type }}</p>
            <p>上传时间: {{ formatDate(previewingFile.created_at) }}</p>
            <p>下载次数: {{ previewingFile.download_count }}</p>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="showPreviewDialog = false">关闭</el-button>
        <el-button type="primary" @click="downloadFile(previewingFile)">下载</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Upload, UploadFilled, Search, Refresh, Download, Delete, View, ArrowDown,
  Document, Picture, VideoPlay, Headphones, FolderZip
} from '@element-plus/icons-vue'
import { fileApi } from '@/api/files'
import { formatDate } from '@/utils/format'

export default {
  name: 'FileManagement',
  components: {
    Upload,
    UploadFilled,
    Search,
    Refresh,
    Download,
    Delete,
    View,
    ArrowDown,
    Document,
    Picture,
    VideoPlay,
    Headphones,
    FolderZip
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const files = ref([])
    const selectedFiles = ref([])
    const storageInfo = ref({})
    const allowedTypes = ref({})
    const viewMode = ref('grid') // grid 或 table
    const showUploadDialog = ref(false)
    const showBatchUploadDialog = ref(false)
    const showPreviewDialog = ref(false)
    const previewingFile = ref(null)
    const batchFileList = ref([])
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      file_type: '',
      related_type: ''
    })
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 上传配置
    const uploadUrl = ref('/api/files/upload')
    const uploadHeaders = ref({
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    })
    const uploadData = ref({
      related_type: 'general'
    })
    
    // 计算属性
    const storageUsagePercentage = computed(() => {
      if (!storageInfo.value.total_size || !storageInfo.value.max_size) return 0
      return Math.round((storageInfo.value.total_size / storageInfo.value.max_size) * 100)
    })
    
    // 方法
    const loadFiles = async () => {
      try {
        loading.value = true
        const params = {
          page: pagination.page,
          size: pagination.size,
          ...searchForm
        }
        
        // 过滤空值
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await fileApi.getFiles(params)
        files.value = response.data.items
        pagination.total = response.data.total
      } catch (error) {
        ElMessage.error('加载文件列表失败')
        console.error('Load files error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadStorageInfo = async () => {
      try {
        const response = await fileApi.getStorageInfo()
        storageInfo.value = response.data
      } catch (error) {
        console.error('Load storage info error:', error)
      }
    }
    
    const loadAllowedTypes = async () => {
      try {
        const response = await fileApi.getAllowedTypes()
        allowedTypes.value = response.data
      } catch (error) {
        console.error('Load allowed types error:', error)
      }
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadFiles()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadFiles()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadFiles()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadFiles()
    }
    
    const handleSelectionChange = (selection) => {
      selectedFiles.value = selection
    }
    
    const selectFile = (file) => {
      const index = selectedFiles.value.findIndex(f => f.id === file.id)
      if (index > -1) {
        selectedFiles.value.splice(index, 1)
      } else {
        selectedFiles.value.push(file)
      }
    }
    
    const isFileSelected = (file) => {
      return selectedFiles.value.some(f => f.id === file.id)
    }
    
    const downloadFile = async (file) => {
      try {
        const response = await fileApi.downloadFile(file.id)
        const blob = new Blob([response.data])
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = file.original_name
        link.click()
        window.URL.revokeObjectURL(url)
        ElMessage.success('下载成功')
      } catch (error) {
        ElMessage.error('下载失败')
        console.error('Download file error:', error)
      }
    }
    
    const previewFile = (file) => {
      previewingFile.value = file
      showPreviewDialog.value = true
    }
    
    const canPreview = (file) => {
      return file.file_type?.startsWith('image/') || file.file_type?.startsWith('text/')
    }
    
    const getFilePreviewUrl = (file) => {
      return `/api/files/${file.id}/preview`
    }
    
    const deleteFile = async (file) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除文件"${file.original_name}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await fileApi.deleteFile(file.id)
        ElMessage.success('删除文件成功')
        loadFiles()
        loadStorageInfo()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除文件失败')
          console.error('Delete file error:', error)
        }
      }
    }
    
    const handleAction = async (command, file) => {
      switch (command) {
        case 'edit':
          // TODO: 实现编辑功能
          ElMessage.info('编辑功能开发中')
          break
        case 'delete':
          await deleteFile(file)
          break
      }
    }
    
    const batchDownload = async () => {
      try {
        for (const file of selectedFiles.value) {
          await downloadFile(file)
        }
        ElMessage.success('批量下载完成')
      } catch (error) {
        ElMessage.error('批量下载失败')
        console.error('Batch download error:', error)
      }
    }
    
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedFiles.value.length} 个文件吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const fileIds = selectedFiles.value.map(f => f.id)
        await fileApi.batchDelete({ file_ids: fileIds })
        
        ElMessage.success('批量删除成功')
        selectedFiles.value = []
        loadFiles()
        loadStorageInfo()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    const beforeUpload = (file) => {
      const isValidType = Object.values(allowedTypes.value.allowed_extensions || {})
        .flat()
        .includes('.' + file.name.split('.').pop().toLowerCase())
      
      if (!isValidType) {
        ElMessage.error('不支持的文件类型')
        return false
      }
      
      const isValidSize = file.size <= (allowedTypes.value.max_file_size || 100 * 1024 * 1024)
      if (!isValidSize) {
        ElMessage.error('文件大小超过限制')
        return false
      }
      
      return true
    }
    
    const handleUploadSuccess = (response) => {
      ElMessage.success('上传成功')
      showUploadDialog.value = false
      loadFiles()
      loadStorageInfo()
    }
    
    const handleBatchUploadSuccess = (response) => {
      ElMessage.success('批量上传成功')
      showBatchUploadDialog.value = false
      batchFileList.value = []
      loadFiles()
      loadStorageInfo()
    }
    
    const handleUploadError = (error) => {
      ElMessage.error('上传失败')
      console.error('Upload error:', error)
    }
    
    const submitUpload = () => {
      // 触发上传
      const uploadRef = document.querySelector('.el-upload__input')
      if (uploadRef) {
        uploadRef.click()
      }
    }
    
    const submitBatchUpload = () => {
      // 触发批量上传
      const batchUploadRef = document.querySelector('.el-upload__input')
      if (batchUploadRef) {
        batchUploadRef.click()
      }
    }
    
    // 工具方法
    const getFileIcon = (file) => {
      if (file.file_type?.startsWith('image/')) return 'Picture'
      if (file.file_type?.startsWith('video/')) return 'VideoPlay'
      if (file.file_type?.startsWith('audio/')) return 'Headphones'
      if (file.file_type?.includes('zip') || file.file_type?.includes('rar')) return 'FolderZip'
      return 'Document'
    }
    
    const getFileIconColor = (file) => {
      if (file.file_type?.startsWith('image/')) return '#67c23a'
      if (file.file_type?.startsWith('video/')) return '#409eff'
      if (file.file_type?.startsWith('audio/')) return '#e6a23c'
      if (file.file_type?.includes('zip') || file.file_type?.includes('rar')) return '#f56c6c'
      return '#909399'
    }
    
    const getTypeIcon = (type) => {
      const icons = {
        image: 'Picture',
        application: 'Document',
        video: 'VideoPlay',
        audio: 'Headphones'
      }
      return icons[type] || 'Document'
    }
    
    const getTypeColor = (type) => {
      const colors = {
        image: '#67c23a',
        application: '#409eff',
        video: '#e6a23c',
        audio: '#f56c6c'
      }
      return colors[type] || '#909399'
    }
    
    const getTypeLabel = (type) => {
      const labels = {
        image: '图片',
        application: '文档',
        video: '视频',
        audio: '音频'
      }
      return labels[type] || type
    }
    
    const getStorageColor = (percentage) => {
      if (percentage >= 90) return '#f56c6c'
      if (percentage >= 70) return '#e6a23c'
      return '#67c23a'
    }
    
    const formatFileSize = (size) => {
      if (size < 1024) return `${size} B`
      if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
      if (size < 1024 * 1024 * 1024) return `${(size / (1024 * 1024)).toFixed(1)} MB`
      return `${(size / (1024 * 1024 * 1024)).toFixed(1)} GB`
    }
    
    // 生命周期
    onMounted(() => {
      loadFiles()
      loadStorageInfo()
      loadAllowedTypes()
    })
    
    return {
      loading,
      files,
      selectedFiles,
      storageInfo,
      allowedTypes,
      viewMode,
      showUploadDialog,
      showBatchUploadDialog,
      showPreviewDialog,
      previewingFile,
      batchFileList,
      searchForm,
      pagination,
      uploadUrl,
      uploadHeaders,
      uploadData,
      storageUsagePercentage,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      selectFile,
      isFileSelected,
      downloadFile,
      previewFile,
      canPreview,
      getFilePreviewUrl,
      deleteFile,
      handleAction,
      batchDownload,
      batchDelete,
      beforeUpload,
      handleUploadSuccess,
      handleBatchUploadSuccess,
      handleUploadError,
      submitUpload,
      submitBatchUpload,
      getFileIcon,
      getFileIconColor,
      getTypeIcon,
      getTypeColor,
      getTypeLabel,
      getStorageColor,
      formatFileSize,
      formatDate
    }
  }
}
</script>

<style scoped>
.file-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
}

.header-info {
  display: flex;
  gap: 10px;
}

.storage-info {
  margin-bottom: 20px;
}

.storage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.storage-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.storage-usage {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 300px;
}

.usage-text {
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
}

.storage-stats {
  padding: 20px 0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-item:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.stat-icon {
  font-size: 24px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 3px;
}

.stat-size {
  font-size: 12px;
  color: #606266;
}

.upload-section {
  margin-bottom: 20px;
}

.upload-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.upload-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.upload-controls {
  display: flex;
  gap: 10px;
}

.upload-info {
  color: #606266;
  font-size: 14px;
}

.upload-info p {
  margin: 5px 0;
}

.search-section {
  margin-bottom: 20px;
}

.files-list {
  margin-bottom: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.list-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 500;
}

.list-actions {
  display: flex;
  gap: 10px;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.file-item {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.file-item:hover {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.file-selected {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.file-preview {
  text-align: center;
  margin-bottom: 15px;
}

.image-preview {
  width: 100%;
  height: 120px;
  overflow: hidden;
  border-radius: 6px;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 120px;
  background-color: #f5f7fa;
  border-radius: 6px;
}

.file-info {
  text-align: center;
}

.file-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
  margin-bottom: 10px;
}

.file-actions {
  display: flex;
  justify-content: center;
  gap: 5px;
}

.file-name-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.file-preview-content {
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  max-height: 500px;
  border-radius: 8px;
}

.file-info-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.preview-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 120px;
  height: 120px;
  background-color: #f5f7fa;
  border-radius: 50%;
}

.preview-details h3 {
  margin: 0 0 15px 0;
  color: #303133;
}

.preview-details p {
  margin: 8px 0;
  color: #606266;
}

:deep(.el-table .el-table__row) {
  cursor: pointer;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f7fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .file-management {
    padding: 15px;
  }
  
  .storage-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .storage-usage {
    width: 100%;
  }
  
  .storage-stats .el-col {
    margin-bottom: 15px;
  }
  
  .list-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .files-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }
}
</style>
