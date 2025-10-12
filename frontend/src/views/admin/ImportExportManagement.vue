<template>
  <div class="modern-import-export-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Upload /></el-icon>
            </div>
            <div class="title-text">
      <h1>数据导入导出</h1>
              <p>批量导入导出系统数据</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button @click="$router.push('/admin')" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回控制台</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
    <!-- 导入功能 -->
      <div class="content-card import-card">
        <div class="card-header">
          <div class="header-icon import-header-icon">
            <el-icon><Upload /></el-icon>
        </div>
          <div class="header-text">
            <h2>数据导入</h2>
            <p>批量导入系统数据</p>
          </div>
        </div>
        
        <div class="import-grid">
              <div class="import-item">
            <div class="item-icon user-icon">
              <el-icon><User /></el-icon>
                </div>
            <div class="item-content">
                  <h4>用户导入</h4>
                  <p>批量导入用户数据</p>
              <div class="item-actions">
                <el-button @click="downloadTemplate('users')" class="template-btn">
                      <el-icon><Download /></el-icon>
                  <span>下载模板</span>
                    </el-button>
                <el-button type="primary" @click="showImportDialog('users')" class="import-btn">
                      <el-icon><Upload /></el-icon>
                  <span>导入数据</span>
                    </el-button>
                  </div>
                </div>
              </div>
          
              <div class="import-item">
            <div class="item-icon subject-icon">
              <el-icon><Book /></el-icon>
                </div>
            <div class="item-content">
                  <h4>科目导入</h4>
                  <p>批量导入科目数据</p>
              <div class="item-actions">
                <el-button @click="downloadTemplate('subjects')" class="template-btn">
                      <el-icon><Download /></el-icon>
                  <span>下载模板</span>
                    </el-button>
                <el-button type="primary" @click="showImportDialog('subjects')" class="import-btn">
                      <el-icon><Upload /></el-icon>
                  <span>导入数据</span>
                    </el-button>
                  </div>
                </div>
              </div>
          
              <div class="import-item">
            <div class="item-icon question-icon">
              <el-icon><QuestionFilled /></el-icon>
                </div>
            <div class="item-content">
                  <h4>试题导入</h4>
                  <p>批量导入试题数据</p>
              <div class="item-actions">
                <el-button @click="downloadTemplate('questions')" class="template-btn">
                      <el-icon><Download /></el-icon>
                  <span>下载模板</span>
                    </el-button>
                <el-button type="primary" @click="showImportDialog('questions')" class="import-btn">
                      <el-icon><Upload /></el-icon>
                  <span>导入数据</span>
                    </el-button>
                  </div>
                </div>
              </div>
        </div>
    </div>

    <!-- 导出功能 -->
      <div class="content-card export-card">
        <div class="card-header">
          <div class="header-icon export-header-icon">
            <el-icon><Download /></el-icon>
        </div>
          <div class="header-text">
            <h2>数据导出</h2>
            <p>导出系统数据到Excel文件</p>
          </div>
        </div>
        
        <div class="export-grid">
              <div class="export-item">
            <div class="item-icon user-icon">
              <el-icon><User /></el-icon>
                </div>
            <div class="item-content">
                  <h4>用户数据</h4>
                  <p>导出用户信息</p>
              <el-button type="primary" @click="exportData('users')" class="export-btn">
                    <el-icon><Download /></el-icon>
                <span>导出</span>
                  </el-button>
                </div>
              </div>
          
              <div class="export-item">
            <div class="item-icon subject-icon">
              <el-icon><Book /></el-icon>
                </div>
            <div class="item-content">
                  <h4>科目数据</h4>
                  <p>导出科目信息</p>
              <el-button type="primary" @click="exportData('subjects')" class="export-btn">
                    <el-icon><Download /></el-icon>
                <span>导出</span>
                  </el-button>
                </div>
              </div>
          
              <div class="export-item">
            <div class="item-icon question-icon">
              <el-icon><QuestionFilled /></el-icon>
                </div>
            <div class="item-content">
                  <h4>试题数据</h4>
                  <p>导出试题信息</p>
              <el-button type="primary" @click="exportData('questions')" class="export-btn">
                    <el-icon><Download /></el-icon>
                <span>导出</span>
                  </el-button>
                </div>
              </div>
          
              <div class="export-item">
            <div class="item-icon result-icon">
              <el-icon><Document /></el-icon>
                </div>
            <div class="item-content">
                  <h4>考试结果</h4>
                  <p>导出考试结果</p>
              <el-button type="primary" @click="exportData('exam-results')" class="export-btn">
                    <el-icon><Download /></el-icon>
                <span>导出</span>
                  </el-button>
                </div>
              </div>
        </div>
    </div>

    <!-- 导入记录 -->
      <div class="content-card records-card">
        <div class="card-header">
          <div class="header-icon records-header-icon">
            <el-icon><Document /></el-icon>
          </div>
          <div class="header-text">
            <h2>导入记录</h2>
            <p>查看历史导入记录和结果</p>
          </div>
          <div class="header-actions">
            <el-button @click="loadImportRecords" class="refresh-btn" :loading="loading">
              <el-icon><Refresh /></el-icon>
              <span>刷新</span>
            </el-button>
          </div>
        </div>
        
        <div class="table-container">
        <el-table
          :data="importRecords"
          :loading="loading"
          stripe
            class="modern-table"
        >
            <el-table-column prop="id" label="ID" width="80" align="center" />
            <el-table-column prop="import_type" label="导入类型" width="200" align="center">
            <template #default="{ row }">
                <el-tag :type="getTypeTagType(row.import_type)" size="small" class="type-tag">
                {{ getTypeLabel(row.import_type) }}
              </el-tag>
            </template>
          </el-table-column>
            <el-table-column prop="total_count" label="总数量" width="150" align="center" />
            <el-table-column prop="success_count" label="成功数量" width="150" align="center" />
            <el-table-column prop="error_count" label="错误数量" width="150" align="center" />
            <el-table-column prop="success_rate" label="成功率" width="250" align="center">
            <template #default="{ row }">
                <div class="progress-container">
              <el-progress
                :percentage="row.success_rate"
                :color="getProgressColor(row.success_rate)"
                :show-text="false"
                    class="progress-bar"
              />
              <span class="progress-text">{{ row.success_rate }}%</span>
                </div>
            </template>
          </el-table-column>
            <el-table-column prop="created_at" label="导入时间" width="280" align="center">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
            <el-table-column label="操作" width="220" align="center">
            <template #default="{ row }">
                <el-button size="small" @click="viewImportDetails(row)" v-if="row.error_count > 0" class="detail-btn">
                查看详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        </div>

        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            :current-page="pagination.page"
            :page-size="pagination.size"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
            class="modern-pagination"
          />
        </div>
      </div>
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User, Book, QuestionFilled, Document, Download, Upload, Refresh, UploadFilled, ArrowLeft
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
    UploadFilled,
    ArrowLeft
  },
  setup() {
    const router = useRouter()
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
      router,
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

<style lang="scss" scoped>
.modern-import-export-management {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.modern-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 24px 32px;
  
  .header-content {
    max-width: 1600px;
    margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  }
  
  .header-left {
    .page-title {
      display: flex;
      align-items: center;
      gap: 16px;
      
      .title-icon {
        width: 56px;
        height: 56px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
      }
      
      .title-text {
        h1 {
          font-size: 28px;
          font-weight: 700;
          color: white;
          margin: 0 0 4px 0;
          letter-spacing: -0.5px;
        }
        
        p {
          color: rgba(255, 255, 255, 0.8);
          font-size: 16px;
  margin: 0;
          font-weight: 500;
        }
      }
    }
  }
  
  .header-right {
    .back-btn {
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: white;
      padding: 12px 24px;
      border-radius: 12px;
      font-weight: 600;
      transition: all 0.3s ease;
      
      &:hover {
        background: rgba(255, 255, 255, 0.25);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
      }
    }
  }
}

.main-content {
  padding: 32px;
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.content-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
  }
  
  .card-header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 32px;
    
    .header-icon {
      width: 56px;
      height: 56px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: white;
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
      
      &.import-header-icon {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }
      
      &.export-header-icon {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      }
      
      &.records-header-icon {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
      }
    }
    
    .header-text {
      flex: 1;
      
      h2 {
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
      }
      
      p {
        color: #666;
        font-size: 15px;
  margin: 0;
        font-weight: 500;
      }
    }
    
    .header-actions {
      .refresh-btn {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        color: #667eea;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        
        &:hover {
          background: rgba(102, 126, 234, 0.2);
          border-color: rgba(102, 126, 234, 0.3);
          transform: translateY(-1px);
        }
      }
    }
  }
}

@keyframes shimmer {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 200% 0%;
  }
}

.import-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  justify-content: center;
}

.export-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  justify-content: center;
}

.import-item,
.export-item {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
  border-radius: 18px;
  padding: 28px;
  border: 2px solid rgba(102, 126, 234, 0.1);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at top right, rgba(102, 126, 234, 0.05) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.4s ease;
  }
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15);
    border-color: rgba(102, 126, 234, 0.3);
    
    &::before {
      opacity: 1;
    }
    
    .item-icon {
      transform: scale(1.1);
    }
  }
  
  .item-icon {
    width: 64px;
    height: 64px;
    border-radius: 18px;
  display: flex;
  align-items: center;
    justify-content: center;
    font-size: 28px;
    color: white;
    flex-shrink: 0;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 20px;
  }
  
  .user-icon {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  .subject-icon {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  }
  
  .question-icon {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  }
  
  .result-icon {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  }
  
  .item-content {
    h4 {
      font-size: 20px;
      font-weight: 700;
      color: #1a1a1a;
  margin: 0 0 8px 0;
      letter-spacing: -0.3px;
    }
    
    p {
      color: #666;
  font-size: 14px;
      margin: 0 0 20px 0;
      font-weight: 500;
}

    .item-actions {
  display: flex;
      gap: 12px;
      
      .template-btn {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        color: #6c757d;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        
        &:hover {
          background: #e9ecef;
          border-color: #dee2e6;
          transform: translateY(-1px);
        }
      }
      
      .import-btn,
      .export-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        
        &:hover {
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
          transform: translateY(-1px);
        }
      }
    }
  }
}

@keyframes shimmer {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 200% 0%;
  }
}

.table-container {
  background: rgba(248, 250, 252, 0.6);
  border-radius: 16px;
  padding: 24px;
  margin-top: 24px;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.modern-table {
  background: transparent;
  border-radius: 16px;
  overflow: hidden;
  
  :deep(.el-table) {
    background: transparent;
    border-radius: 12px;
    overflow: hidden;
    
    .el-table__header-wrapper {
      border-radius: 12px 12px 0 0;
      overflow: hidden;
    }
    
    .el-table__header th {
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      color: #495057;
      font-weight: 700;
      border-bottom: 2px solid rgba(102, 126, 234, 0.1);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-size: 13px;
      padding: 16px 12px;
      border: none;
    }
    
    .el-table__body-wrapper {
      border-radius: 0 0 12px 12px;
      overflow: hidden;
    }
    
    .el-table__body tr {
      transition: all 0.3s ease;
      border: none;
      
      &:hover {
        background: rgba(102, 126, 234, 0.08);
        transform: scale(1.005);
      }
      
      td {
        border: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
        padding: 16px 12px;
        font-weight: 500;
      }
    }
    
    .el-table__empty-block {
      background: transparent;
    }
  }
}

.type-tag {
  font-weight: 600;
  border-radius: 6px;
  padding: 4px 8px;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 12px;
  
  .progress-bar {
    flex: 1;
    height: 8px;
    
    :deep(.el-progress-bar__outer) {
      background: rgba(0, 0, 0, 0.08);
      border-radius: 4px;
    }
    
    :deep(.el-progress-bar__inner) {
      border-radius: 4px;
    }
}

.progress-text {
    font-weight: 600;
    color: #666;
    min-width: 40px;
    text-align: right;
  }
}

.modern-pagination {
  margin-top: 32px;
  display: flex;
  justify-content: center;
  
  :deep(.el-pagination) {
    .el-pager li {
      background: rgba(248, 250, 252, 0.8);
      border: 1px solid rgba(102, 126, 234, 0.1);
      border-radius: 8px;
      margin: 0 4px;
      transition: all 0.3s ease;
      
      &:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
      }
      
      &.is-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: transparent;
        color: white;
      }
    }
    
    .btn-prev,
    .btn-next {
      background: rgba(248, 250, 252, 0.8);
      border: 1px solid rgba(102, 126, 234, 0.1);
      border-radius: 8px;
      transition: all 0.3s ease;
      
      &:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
      }
    }
  }
}

.detail-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    transform: translateY(-1px);
  }
}

// 响应式设计
@media (max-width: 1400px) {
  .import-grid,
  .export-grid {
    max-width: 1000px;
  }
  
  .table-container {
    max-width: 1200px;
  }
}

@media (max-width: 1200px) {
  .import-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .export-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .import-section,
  .export-section,
  .import-records {
    padding: 24px;
  }
}

@media (max-width: 900px) {
  .export-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .table-container {
    max-width: 100%;
    padding: 16px;
  }
}

@media (max-width: 768px) {
  .modern-header {
    padding: 20px 16px;
    
    .header-content {
      flex-direction: column;
      gap: 16px;
      text-align: center;
    }
    
    .page-title {
      .title-text h1 {
        font-size: 24px;
      }
    }
  }
  
  .import-grid {
    grid-template-columns: 1fr;
    gap: 16px;
    max-width: 100%;
  }
  
  .export-grid {
    grid-template-columns: 1fr;
    gap: 16px;
    max-width: 100%;
  }
  
  .import-item,
  .export-item {
    padding: 20px;
    
    .import-actions,
    .export-actions {
      flex-direction: column;
      gap: 8px;
      
      .template-btn,
      .import-btn,
      .export-btn {
        width: 100%;
      }
    }
  }
  
  .import-section,
  .export-section,
  .import-records {
    padding: 16px;
    
    .import-card,
    .export-card,
    .records-card {
      padding: 24px;
    }
  }
}

// 响应式设计
@media (max-width: 1400px) {
  .main-content {
    padding: 24px;
    gap: 24px;
  }
  
  .content-card {
    padding: 24px;
  }
}

@media (max-width: 1200px) {
  .import-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .export-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .modern-header {
    padding: 20px 24px;
    
    .header-content {
      max-width: 100%;
    }
  }
}

@media (max-width: 900px) {
  .export-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .table-container {
    padding: 16px;
  }
}

@media (max-width: 768px) {
  .modern-header {
    padding: 20px 16px;
    
    .header-content {
      flex-direction: column;
      gap: 16px;
      text-align: center;
    }
    
    .page-title {
      .title-text h1 {
        font-size: 24px;
      }
    }
  }
  
  .main-content {
    padding: 16px;
    gap: 20px;
  }
  
  .content-card {
    padding: 20px;
    
    .card-header {
      flex-direction: column;
      gap: 16px;
      text-align: center;
    }
  }
  
  .import-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .import-item,
  .export-item {
    padding: 20px;
    
    .item-actions {
      flex-direction: column;
      gap: 8px;
      
      .template-btn,
      .import-btn,
      .export-btn {
        width: 100%;
      }
    }
  }
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
