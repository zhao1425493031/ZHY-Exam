<template>
  <div class="import-export-management">
    <div class="page-header">
      <h1>数据导入导出</h1>
      <div class="header-info">
        <el-tag type="info">数据管理工具</el-tag>
      </div>
    </div>

    <!-- 导入功能 -->
    <div class="import-section">
      <el-card>
        <div class="section-header">
          <h3>数据导入</h3>
        </div>
        <div class="import-content">
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="import-item">
                <div class="import-icon">
                  <el-icon color="#409eff"><User /></el-icon>
                </div>
                <div class="import-info">
                  <h4>用户导入</h4>
                  <p>批量导入用户数据</p>
                  <div class="import-actions">
                    <el-button size="small" @click="downloadTemplate('users')">
                      <el-icon><Download /></el-icon>
                      下载模板
                    </el-button>
                    <el-button size="small" type="primary" @click="showImportDialog('users')">
                      <el-icon><Upload /></el-icon>
                      导入数据
                    </el-button>
                  </div>
                </div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="import-item">
                <div class="import-icon">
                  <el-icon color="#67c23a"><Book /></el-icon>
                </div>
                <div class="import-info">
                  <h4>科目导入</h4>
                  <p>批量导入科目数据</p>
                  <div class="import-actions">
                    <el-button size="small" @click="downloadTemplate('subjects')">
                      <el-icon><Download /></el-icon>
                      下载模板
                    </el-button>
                    <el-button size="small" type="primary" @click="showImportDialog('subjects')">
                      <el-icon><Upload /></el-icon>
                      导入数据
                    </el-button>
                  </div>
                </div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="import-item">
                <div class="import-icon">
                  <el-icon color="#e6a23c"><QuestionFilled /></el-icon>
                </div>
                <div class="import-info">
                  <h4>试题导入</h4>
                  <p>批量导入试题数据</p>
                  <div class="import-actions">
                    <el-button size="small" @click="downloadTemplate('questions')">
                      <el-icon><Download /></el-icon>
                      下载模板
                    </el-button>
                    <el-button size="small" type="primary" @click="showImportDialog('questions')">
                      <el-icon><Upload /></el-icon>
                      导入数据
                    </el-button>
                  </div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>

    <!-- 导出功能 -->
    <div class="export-section">
      <el-card>
        <div class="section-header">
          <h3>数据导出</h3>
        </div>
        <div class="export-content">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="export-item">
                <div class="export-icon">
                  <el-icon color="#409eff"><User /></el-icon>
                </div>
                <div class="export-info">
                  <h4>用户数据</h4>
                  <p>导出用户信息</p>
                  <el-button size="small" type="primary" @click="exportData('users')">
                    <el-icon><Download /></el-icon>
                    导出
                  </el-button>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="export-item">
                <div class="export-icon">
                  <el-icon color="#67c23a"><Book /></el-icon>
                </div>
                <div class="export-info">
                  <h4>科目数据</h4>
                  <p>导出科目信息</p>
                  <el-button size="small" type="primary" @click="exportData('subjects')">
                    <el-icon><Download /></el-icon>
                    导出
                  </el-button>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="export-item">
                <div class="export-icon">
                  <el-icon color="#e6a23c"><QuestionFilled /></el-icon>
                </div>
                <div class="export-info">
                  <h4>试题数据</h4>
                  <p>导出试题信息</p>
                  <el-button size="small" type="primary" @click="exportData('questions')">
                    <el-icon><Download /></el-icon>
                    导出
                  </el-button>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="export-item">
                <div class="export-icon">
                  <el-icon color="#f56c6c"><Document /></el-icon>
                </div>
                <div class="export-info">
                  <h4>考试结果</h4>
                  <p>导出考试结果</p>
                  <el-button size="small" type="primary" @click="exportData('exam-results')">
                    <el-icon><Download /></el-icon>
                    导出
                  </el-button>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>

    <!-- 导入记录 -->
    <div class="import-records">
      <el-card>
        <div class="records-header">
          <h3>导入记录</h3>
          <div class="records-actions">
            <el-button size="small" @click="loadImportRecords">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
        
        <el-table
          :data="importRecords"
          :loading="loading"
          stripe
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="import_type" label="导入类型" width="120">
            <template #default="{ row }">
              <el-tag :type="getTypeTagType(row.import_type)" size="small">
                {{ getTypeLabel(row.import_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="total_count" label="总数量" width="100" />
          <el-table-column prop="success_count" label="成功数量" width="100" />
          <el-table-column prop="error_count" label="错误数量" width="100" />
          <el-table-column prop="success_rate" label="成功率" width="100">
            <template #default="{ row }">
              <el-progress
                :percentage="row.success_rate"
                :color="getProgressColor(row.success_rate)"
                :show-text="false"
              />
              <span class="progress-text">{{ row.success_rate }}%</span>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="导入时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button size="small" @click="viewImportDetails(row)" v-if="row.error_count > 0">
                查看详情
              </el-button>
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

    <!-- 导入对话框 -->
    <el-dialog
      v-model="showImportDialogFlag"
      :title="`导入${getTypeLabel(importType)}`"
      width="600px"
    >
      <div class="import-dialog-content">
        <div class="import-steps">
          <el-steps :active="importStep" finish-status="success">
            <el-step title="选择文件" />
            <el-step title="验证数据" />
            <el-step title="导入完成" />
          </el-steps>
        </div>
        
        <div class="import-form" v-if="importStep === 0">
          <el-form :model="importForm" label-width="100px">
            <el-form-item label="选择文件">
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
                  将Excel文件拖到此处，或<em>点击上传</em>
                </div>
                <template #tip>
                  <div class="el-upload__tip">
                    只支持Excel文件（.xlsx, .xls）
                  </div>
                </template>
              </el-upload>
            </el-form-item>
            <el-form-item label="科目选择" v-if="importType === 'questions'">
              <el-select v-model="importForm.subject_id" placeholder="请选择科目" style="width: 100%">
                <el-option
                  v-for="subject in subjects"
                  :key="subject.id"
                  :label="subject.name"
                  :value="subject.id"
                />
              </el-select>
            </el-form-item>
          </el-form>
        </div>
        
        <div class="import-result" v-if="importStep === 2">
          <div class="result-summary">
            <h4>导入结果</h4>
            <div class="result-stats">
              <el-row :gutter="20">
                <el-col :span="8">
                  <div class="stat-item">
                    <div class="stat-value">{{ importResult.total_count }}</div>
                    <div class="stat-label">总数量</div>
                  </div>
                </el-col>
                <el-col :span="8">
                  <div class="stat-item success">
                    <div class="stat-value">{{ importResult.success_count }}</div>
                    <div class="stat-label">成功数量</div>
                  </div>
                </el-col>
                <el-col :span="8">
                  <div class="stat-item error">
                    <div class="stat-value">{{ importResult.error_count }}</div>
                    <div class="stat-label">错误数量</div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>
          
          <div class="error-details" v-if="importResult.errors && importResult.errors.length > 0">
            <h4>错误详情</h4>
            <el-scrollbar height="200px">
              <div class="error-list">
                <div v-for="(error, index) in importResult.errors" :key="index" class="error-item">
                  {{ error }}
                </div>
              </div>
            </el-scrollbar>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="showImportDialogFlag = false">关闭</el-button>
        <el-button type="primary" @click="submitImport" v-if="importStep === 0">
          开始导入
        </el-button>
        <el-button type="primary" @click="showImportDialogFlag = false" v-if="importStep === 2">
          完成
        </el-button>
      </template>
    </el-dialog>

    <!-- 导入详情对话框 -->
    <el-dialog
      v-model="showDetailsDialog"
      title="导入详情"
      width="600px"
    >
      <div v-if="selectedRecord" class="details-content">
        <div class="details-summary">
          <h4>导入摘要</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="导入类型">
              {{ getTypeLabel(selectedRecord.import_type) }}
            </el-descriptions-item>
            <el-descriptions-item label="总数量">
              {{ selectedRecord.total_count }}
            </el-descriptions-item>
            <el-descriptions-item label="成功数量">
              {{ selectedRecord.success_count }}
            </el-descriptions-item>
            <el-descriptions-item label="错误数量">
              {{ selectedRecord.error_count }}
            </el-descriptions-item>
            <el-descriptions-item label="成功率">
              {{ selectedRecord.success_rate }}%
            </el-descriptions-item>
            <el-descriptions-item label="导入时间">
              {{ formatDate(selectedRecord.created_at) }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="details-errors" v-if="selectedRecord.error_details">
          <h4>错误详情</h4>
          <el-scrollbar height="300px">
            <div class="error-list">
              <div v-for="(error, index) in selectedRecord.error_details.split(';')" :key="index" class="error-item">
                {{ error }}
              </div>
            </div>
          </el-scrollbar>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="showDetailsDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User, Book, QuestionFilled, Document, Download, Upload, Refresh, UploadFilled
} from '@element-plus/icons-vue'
import { importExportApi } from '@/api/import_export'
import { subjectApi } from '@/api/subjects'
import { formatDate } from '@/utils/format'

export default {
  name: 'ImportExportManagement',
  components: {
    User,
    Book,
    QuestionFilled,
    Document,
    Download,
    Upload,
    Refresh,
    UploadFilled
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const importRecords = ref([])
    const subjects = ref([])
    const showImportDialogFlag = ref(false)
    const showDetailsDialog = ref(false)
    const importType = ref('')
    const importStep = ref(0)
    const selectedRecord = ref(null)
    const importResult = ref({})
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 导入表单
    const importForm = reactive({
      subject_id: null
    })
    
    // 上传配置
    const uploadUrl = ref('/api/import-export/users/import')
    const uploadHeaders = ref({
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    })
    const uploadData = ref({})
    
    // 方法
    const loadImportRecords = async () => {
      try {
        loading.value = true
        const params = {
          page: pagination.page,
          size: pagination.size
        }
        
        const response = await importExportApi.getImportRecords(params)
        importRecords.value = response.data.items
        pagination.total = response.data.total
      } catch (error) {
        ElMessage.error('加载导入记录失败')
        console.error('Load import records error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadSubjects = async () => {
      try {
        const response = await subjectApi.getSubjects()
        subjects.value = response.data.items
      } catch (error) {
        console.error('Load subjects error:', error)
      }
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadImportRecords()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadImportRecords()
    }
    
    const showImportDialog = (type) => {
      importType.value = type
      importStep.value = 0
      importForm.subject_id = null
      importResult.value = {}
      
      // 设置上传URL
      uploadUrl.value = `/api/import-export/${type}/import`
      
      // 如果是试题导入，加载科目列表
      if (type === 'questions') {
        loadSubjects()
      }
      
      showImportDialogFlag.value = true
    }
    
    const downloadTemplate = async (type) => {
      try {
        const response = await importExportApi.downloadTemplate(type)
        const blob = new Blob([response.data])
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `${type}模板.xlsx`
        link.click()
        window.URL.revokeObjectURL(url)
        ElMessage.success('下载模板成功')
      } catch (error) {
        ElMessage.error('下载模板失败')
        console.error('Download template error:', error)
      }
    }
    
    const exportData = async (type) => {
      try {
        const response = await importExportApi.exportData(type)
        const blob = new Blob([response.data])
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `${type}数据.xlsx`
        link.click()
        window.URL.revokeObjectURL(url)
        ElMessage.success('导出数据成功')
      } catch (error) {
        ElMessage.error('导出数据失败')
        console.error('Export data error:', error)
      }
    }
    
    const beforeUpload = (file) => {
      const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
                    file.type === 'application/vnd.ms-excel'
      
      if (!isExcel) {
        ElMessage.error('只支持Excel文件')
        return false
      }
      
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        ElMessage.error('文件大小不能超过10MB')
        return false
      }
      
      return true
    }
    
    const handleUploadSuccess = (response) => {
      importResult.value = response.data
      importStep.value = 2
      loadImportRecords()
    }
    
    const handleUploadError = (error) => {
      ElMessage.error('上传失败')
      console.error('Upload error:', error)
    }
    
    const submitImport = () => {
      if (importType.value === 'questions' && !importForm.subject_id) {
        ElMessage.error('请选择科目')
        return
      }
      
      // 设置上传数据
      uploadData.value = {}
      if (importType.value === 'questions') {
        uploadData.value.subject_id = importForm.subject_id
      }
      
      // 触发上传
      const uploadRef = document.querySelector('.el-upload__input')
      if (uploadRef) {
        uploadRef.click()
      }
    }
    
    const viewImportDetails = (record) => {
      selectedRecord.value = record
      showDetailsDialog.value = true
    }
    
    // 工具方法
    const getTypeLabel = (type) => {
      const labels = {
        users: '用户',
        subjects: '科目',
        questions: '试题'
      }
      return labels[type] || type
    }
    
    const getTypeTagType = (type) => {
      const types = {
        users: 'primary',
        subjects: 'success',
        questions: 'warning'
      }
      return types[type] || 'default'
    }
    
    const getProgressColor = (percentage) => {
      if (percentage >= 90) return '#67c23a'
      if (percentage >= 70) return '#e6a23c'
      return '#f56c6c'
    }
    
    // 生命周期
    onMounted(() => {
      loadImportRecords()
    })
    
    return {
      loading,
      importRecords,
      subjects,
      showImportDialogFlag,
      showDetailsDialog,
      importType,
      importStep,
      selectedRecord,
      importResult,
      pagination,
      importForm,
      uploadUrl,
      uploadHeaders,
      uploadData,
      loadImportRecords,
      handlePageChange,
      handleSizeChange,
      showImportDialog,
      downloadTemplate,
      exportData,
      beforeUpload,
      handleUploadSuccess,
      handleUploadError,
      submitImport,
      viewImportDetails,
      getTypeLabel,
      getTypeTagType,
      getProgressColor,
      formatDate
    }
  }
}
</script>

<style scoped>
.import-export-management {
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

.import-section,
.export-section,
.import-records {
  margin-bottom: 20px;
}

.section-header,
.records-header {
  margin-bottom: 20px;
}

.section-header h3,
.records-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.records-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.import-content,
.export-content {
  padding: 20px 0;
}

.import-item,
.export-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.import-item:hover,
.export-item:hover {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.import-icon,
.export-icon {
  font-size: 32px;
}

.import-info,
.export-info {
  flex: 1;
}

.import-info h4,
.export-info h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 16px;
}

.import-info p,
.export-info p {
  margin: 0 0 15px 0;
  color: #909399;
  font-size: 14px;
}

.import-actions {
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.progress-text {
  margin-left: 10px;
  font-size: 12px;
  color: #606266;
}

.import-dialog-content {
  padding: 20px 0;
}

.import-steps {
  margin-bottom: 30px;
}

.import-form {
  padding: 20px 0;
}

.import-result {
  padding: 20px 0;
}

.result-summary h4 {
  margin: 0 0 20px 0;
  color: #303133;
}

.result-stats {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.stat-item.success {
  border-color: #67c23a;
  background-color: #f0f9ff;
}

.stat-item.error {
  border-color: #f56c6c;
  background-color: #fef0f0;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.error-details h4 {
  margin: 0 0 15px 0;
  color: #303133;
}

.error-list {
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 6px;
}

.error-item {
  padding: 8px 0;
  border-bottom: 1px solid #e4e7ed;
  color: #f56c6c;
  font-size: 14px;
}

.error-item:last-child {
  border-bottom: none;
}

.details-content {
  padding: 20px 0;
}

.details-summary h4 {
  margin: 0 0 20px 0;
  color: #303133;
}

.details-errors h4 {
  margin: 20px 0 15px 0;
  color: #303133;
}

:deep(.el-table .el-table__row) {
  cursor: pointer;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f7fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .import-export-management {
    padding: 15px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .import-content .el-col,
  .export-content .el-col {
    margin-bottom: 15px;
  }
  
  .import-item,
  .export-item {
    flex-direction: column;
    text-align: center;
  }
  
  .records-header {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
