<template>
  <div class="modern-exam-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="title-text">
              <h1>考试管理</h1>
              <p>创建和管理考试</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="showCreateDialog = true" class="add-btn">
            <el-icon><Plus /></el-icon>
            <span>创建考试</span>
          </el-button>
          <el-button @click="showTemplateDialog = true" class="back-btn">
            <el-icon><Document /></el-icon>
            <span>考试模板</span>
          </el-button>
          <el-button @click="$router.push('/admin')" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回控制台</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-section">
      <div class="search-card">
        <div class="search-header">
          <h3>搜索和筛选</h3>
          <p>快速查找考试信息</p>
        </div>
        <div class="search-form">
          <el-form :model="searchForm" inline>
            <el-form-item>
              <el-input
                v-model="searchForm.keyword"
                placeholder="请输入考试标题"
                prefix-icon="Search"
                class="search-input"
                clearable
                @keyup.enter="handleSearch"
              />
            </el-form-item>
            <el-form-item>
              <el-select
                v-model="searchForm.subject_id"
                placeholder="选择科目"
                clearable
                class="filter-select"
              >
                <el-option
                  v-for="subject in subjects"
                  :key="subject.id"
                  :label="subject.name"
                  :value="subject.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-select
                v-model="searchForm.status"
                placeholder="选择状态"
                clearable
                class="filter-select"
              >
                <el-option label="草稿" value="draft" />
                <el-option label="已发布" value="published" />
                <el-option label="进行中" value="ongoing" />
                <el-option label="已结束" value="finished" />
                <el-option label="已取消" value="cancelled" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch" class="search-btn">
                <el-icon><Search /></el-icon>
                <span>搜索</span>
              </el-button>
              <el-button @click="handleReset" class="reset-btn">
                <el-icon><Refresh /></el-icon>
                <span>重置</span>
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>

    <!-- 考试列表 -->
    <div class="table-section">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>考试列表</h3>
            <p>共 {{ pagination.total }} 个考试</p>
          </div>
          <div class="table-actions" v-if="selectedExams.length > 0">
            <el-button size="small" @click="batchUpdateStatus('published')" class="action-btn">
              批量发布
            </el-button>
            <el-button size="small" @click="batchUpdateStatus('cancelled')" class="action-btn">
              批量取消
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete" class="action-btn">
              批量删除
            </el-button>
          </div>
        </div>

        <div class="table-container">
          <el-table
            :data="exams"
            :loading="loading"
            @selection-change="handleSelectionChange"
            row-key="id"
            stripe
            class="modern-table"
          >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="考试标题" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="exam-info">
                <div class="exam-avatar">{{ row.title.charAt(0).toUpperCase() }}</div>
                <div class="exam-details">
                  <div class="exam-title-text">{{ row.title }}</div>
                  <div class="exam-meta">
                    <el-tag :type="getStatusTagType(row.status)" size="small" class="meta-tag">
                      {{ getStatusLabel(row.status) }}
                    </el-tag>
                    <span class="exam-stats">
                      {{ row.question_count }}题 | {{ row.total_points }}分 | {{ formatDuration(row.duration) }}
                    </span>
                  </div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="subject_id" label="科目" width="120">
            <template #default="{ row }">
              {{ getSubjectName(row.subject_id) }}
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
          <el-table-column label="时间设置" width="200">
            <template #default="{ row }">
              <div class="time-info">
                <div v-if="row.start_time" class="time-item">
                  <span class="time-label">开始：</span>
                  <span class="time-value">{{ formatDate(row.start_time, 'MM-DD HH:mm') }}</span>
                </div>
                <div v-if="row.end_time" class="time-item">
                  <span class="time-label">结束：</span>
                  <span class="time-value">{{ formatDate(row.end_time, 'MM-DD HH:mm') }}</span>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button size="small" type="primary" @click="editExam(row)" class="action-btn edit-btn">
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button size="small" type="warning" @click="toggleExamStatus(row)" class="action-btn status-btn">
                  <el-icon><Switch /></el-icon>
                </el-button>
                <el-button size="small" type="danger" @click="deleteExam(row)" class="action-btn delete-btn">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
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

    <!-- 创建/编辑考试对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingExam ? '编辑考试' : '创建考试'"
      width="80%"
      :close-on-click-modal="false"
    >
      <ExamForm
        v-if="showCreateDialog"
        :exam="editingExam"
        :subjects="subjects"
        @submit="handleSubmit"
        @cancel="showCreateDialog = false"
      />
    </el-dialog>

    <!-- 查看考试对话框 -->
    <el-dialog
      v-model="showViewDialog"
      title="考试详情"
      width="60%"
    >
      <ExamView
        v-if="showViewDialog && viewingExam"
        :exam="viewingExam"
        :subjects="subjects"
      />
    </el-dialog>

    <!-- 考试模板对话框 -->
    <el-dialog
      v-model="showTemplateDialog"
      title="考试模板管理"
      width="70%"
    >
      <ExamTemplate
        v-if="showTemplateDialog"
        :subjects="subjects"
        @success="handleTemplateSuccess"
        @cancel="showTemplateDialog = false"
      />
    </el-dialog>

    <!-- 考试统计对话框 -->
    <el-dialog
      v-model="showStatisticsDialog"
      title="考试统计"
      width="80%"
    >
      <ExamStatistics
        v-if="showStatisticsDialog && statisticsExam"
        :exam="statisticsExam"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Document, Search, Refresh, ArrowLeft, Edit, Switch, Delete } from '@element-plus/icons-vue'
import ExamForm from '@/components/exam/ExamForm.vue'
import ExamView from '@/components/exam/ExamView.vue'
import ExamTemplate from '@/components/exam/ExamTemplate.vue'
import ExamStatistics from '@/components/exam/ExamStatistics.vue'
import { examApi } from '@/api/exams'
import { subjectApi } from '@/api/subjects'
import { formatDate, formatDuration } from '@/utils/format'

export default {
  name: 'ExamManagement',
  components: {
    ExamForm,
    ExamView,
    ExamTemplate,
    ExamStatistics,
    Plus,
    Document,
    Search,
    Refresh,
    ArrowLeft,
    Edit,
    Switch,
    Delete
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const exams = ref([])
    const subjects = ref([])
    const selectedExams = ref([])
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      subject_id: '',
      status: '',
      date_range: []
    })
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 对话框状态
    const showCreateDialog = ref(false)
    const showViewDialog = ref(false)
    const showTemplateDialog = ref(false)
    const showStatisticsDialog = ref(false)
    const editingExam = ref(null)
    const viewingExam = ref(null)
    const statisticsExam = ref(null)
    
    // 计算属性
    const getSubjectName = computed(() => {
      return (subjectId) => {
        const subject = subjects.value.find(s => s.id === subjectId)
        return subject ? subject.name : '未知科目'
      }
    })
    
    // 方法
    const loadExams = async () => {
      try {
        loading.value = true
        const params = {
          page: pagination.page,
          size: pagination.size,
          ...searchForm
        }
        
        // 处理日期范围
        if (searchForm.date_range && searchForm.date_range.length === 2) {
          params.start_date = searchForm.date_range[0]
          params.end_date = searchForm.date_range[1]
          delete params.date_range
        }
        
        // 过滤空值
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await examApi.getExams(params)
        exams.value = response.data.items
        pagination.total = response.data.total
      } catch (error) {
        ElMessage.error('加载考试列表失败')
        console.error('Load exams error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadSubjects = async () => {
      try {
        const response = await subjectApi.getSubjects()
        subjects.value = response.data.items || response.data
      } catch (error) {
        console.error('Load subjects error:', error)
      }
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadExams()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadExams()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadExams()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadExams()
    }
    
    const handleSelectionChange = (selection) => {
      selectedExams.value = selection
    }
    
    const viewExam = (exam) => {
      viewingExam.value = exam
      showViewDialog.value = true
    }
    
    const editExam = (exam) => {
      editingExam.value = exam
      showCreateDialog.value = true
    }
    
    const handleSubmit = async (examData) => {
      try {
        if (editingExam.value) {
          await examApi.updateExam(editingExam.value.id, examData)
          ElMessage.success('考试更新成功')
        } else {
          await examApi.createExam(examData)
          ElMessage.success('考试创建成功')
        }
        
        showCreateDialog.value = false
        editingExam.value = null
        loadExams()
      } catch (error) {
        ElMessage.error('保存考试失败')
        console.error('Submit exam error:', error)
      }
    }
    
    const handleAction = async (command, exam) => {
      switch (command) {
        case 'toggle-status':
          await toggleExamStatus(exam)
          break
        case 'duplicate':
          await duplicateExam(exam)
          break
        case 'preview':
          await previewExam(exam)
          break
        case 'statistics':
          await showExamStatistics(exam)
          break
        case 'delete':
          await deleteExam(exam)
          break
      }
    }
    
    const toggleExamStatus = async (exam) => {
      try {
        const newStatus = exam.status === 'published' ? 'draft' : 'published'
        await examApi.updateExamStatus(exam.id, { status: newStatus })
        ElMessage.success(`考试已${newStatus === 'published' ? '发布' : '取消发布'}`)
        loadExams()
      } catch (error) {
        ElMessage.error('更新考试状态失败')
        console.error('Toggle status error:', error)
      }
    }
    
    const duplicateExam = async (exam) => {
      try {
        const duplicateData = { ...exam }
        delete duplicateData.id
        delete duplicateData.created_at
        delete duplicateData.updated_at
        duplicateData.title = duplicateData.title + ' (副本)'
        duplicateData.status = 'draft'
        
        await examApi.createExam(duplicateData)
        ElMessage.success('考试复制成功')
        loadExams()
      } catch (error) {
        ElMessage.error('复制考试失败')
        console.error('Duplicate exam error:', error)
      }
    }
    
    const previewExam = async (exam) => {
      // TODO: 实现考试预览功能
      ElMessage.info('考试预览功能开发中')
    }
    
    const showExamStatistics = (exam) => {
      statisticsExam.value = exam
      showStatisticsDialog.value = true
    }
    
    const deleteExam = async (exam) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除考试"${exam.title}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await examApi.deleteExam(exam.id)
        ElMessage.success('考试删除成功')
        loadExams()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除考试失败')
          console.error('Delete exam error:', error)
        }
      }
    }
    
    const batchUpdateStatus = async (status) => {
      try {
        const ids = selectedExams.value.map(e => e.id)
        await examApi.batchUpdateStatus({ ids, status })
        ElMessage.success(`批量${status === 'published' ? '发布' : '取消'}成功`)
        selectedExams.value = []
        loadExams()
      } catch (error) {
        ElMessage.error('批量更新状态失败')
        console.error('Batch update status error:', error)
      }
    }
    
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedExams.value.length} 个考试吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const ids = selectedExams.value.map(e => e.id)
        await examApi.batchDelete({ ids })
        ElMessage.success('批量删除成功')
        selectedExams.value = []
        loadExams()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    const handleTemplateSuccess = () => {
      showTemplateDialog.value = false
      loadExams()
    }
    
    // 工具方法
    const getStatusLabel = (status) => {
      const labels = {
        draft: '草稿',
        published: '已发布',
        ongoing: '进行中',
        finished: '已结束',
        cancelled: '已取消'
      }
      return labels[status] || status
    }
    
    const getStatusTagType = (status) => {
      const types = {
        draft: 'info',
        published: 'success',
        ongoing: 'primary',
        finished: 'warning',
        cancelled: 'danger'
      }
      return types[status] || 'default'
    }
    
    // 生命周期
    onMounted(() => {
      loadSubjects()
      loadExams()
    })
    
    return {
      loading,
      exams,
      subjects,
      selectedExams,
      searchForm,
      pagination,
      showCreateDialog,
      showViewDialog,
      showTemplateDialog,
      showStatisticsDialog,
      editingExam,
      viewingExam,
      statisticsExam,
      getSubjectName,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewExam,
      editExam,
      toggleExamStatus,
      deleteExam,
      handleSubmit,
      handleAction,
      batchUpdateStatus,
      batchDelete,
      handleTemplateSuccess,
      getStatusLabel,
      getStatusTagType,
      formatDate,
      formatDuration
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-exam-management {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.modern-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 24px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  
  .header-content {
    max-width: 1800px;
    margin: 0 auto;
    padding: 0 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .header-left {
      .page-title {
        display: flex;
        align-items: center;
        gap: 20px;
        
        .title-icon {
          width: 64px;
          height: 64px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.3);
          
          .el-icon {
            font-size: 32px;
            color: white;
          }
        }
        
        .title-text {
          h1 {
            font-size: 32px;
            font-weight: 700;
            color: white;
            margin: 0 0 8px 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
      display: flex;
      gap: 12px;
      
      .add-btn, .back-btn {
        padding: 12px 20px;
        font-weight: 600;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        
        &.el-button--primary {
          background: rgba(255, 255, 255, 0.2);
          border-color: rgba(255, 255, 255, 0.3);
          color: white;
          
          &:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
          }
        }
        
        &:not(.el-button--primary) {
          background: rgba(255, 255, 255, 0.1);
          border-color: rgba(255, 255, 255, 0.2);
          color: white;
          
          &:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
          }
        }
      }
    }
  }
}

.search-section {
  padding: 32px;
  
  .search-card {
    max-width: 1800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    
    .search-header {
      margin-bottom: 24px;
      
      h3 {
        font-size: 20px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0 0 8px 0;
      }
      
      p {
        color: #666;
        font-size: 14px;
        margin: 0;
      }
    }
    
    .search-form {
      .el-form {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        align-items: end;
        
        .el-form-item {
          margin-bottom: 0;
          
          .search-input {
            width: 240px;
            
            :deep(.el-input__wrapper) {
              border-radius: 12px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
          }
          
          .filter-select {
            width: 160px;
            
            :deep(.el-select__wrapper) {
              border-radius: 12px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
          }
          
          .search-btn, .reset-btn {
            padding: 10px 20px;
            border-radius: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            
            &.el-button--primary {
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              border: none;
              
              &:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
              }
            }
            
            &:not(.el-button--primary) {
              background: #f8f9fa;
              border-color: #e9ecef;
              color: #6c757d;
              
              &:hover {
                background: #e9ecef;
                transform: translateY(-2px);
              }
            }
          }
        }
      }
    }
  }
}

.table-section {
  padding: 0 32px 32px;
  
  .table-card {
    max-width: 1800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    
    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      
      .table-title {
        h3 {
          font-size: 20px;
          font-weight: 700;
          color: #1a1a1a;
          margin: 0 0 4px 0;
        }
        
        p {
          color: #666;
          font-size: 14px;
          margin: 0;
        }
      }
      
      .table-actions {
        display: flex;
        gap: 8px;
        
        .action-btn {
          padding: 8px 16px;
          border-radius: 8px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 4px;
          
          &:not(.el-button--danger) {
            background: #f8f9fa;
            border-color: #e9ecef;
            color: #6c757d;
            
            &:hover {
              background: #e9ecef;
              transform: translateY(-1px);
            }
          }
        }
      }
    }
    
    .table-container {
      .modern-table {
        :deep(.el-table__header) {
          th {
            background: #f8f9fa;
            color: #495057;
            font-weight: 600;
            border-bottom: 2px solid #e9ecef;
          }
        }
        
        :deep(.el-table__body) {
          tr {
            &:hover {
              background: rgba(102, 126, 234, 0.05);
            }
          }
        }
        
        .exam-info {
          display: flex;
          align-items: center;
          gap: 12px;
          
          .exam-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
          }
          
          .exam-details {
            flex: 1;
            
            .exam-title-text {
              font-weight: 600;
              color: #1a1a1a;
              margin-bottom: 8px;
              line-height: 1.4;
            }
            
            .exam-meta {
              display: flex;
              gap: 8px;
              align-items: center;
              flex-wrap: wrap;
              
              .meta-tag {
                border-radius: 6px;
                font-size: 12px;
                padding: 2px 8px;
              }
              
              .exam-stats {
                font-size: 12px;
                color: #666;
                font-weight: 500;
              }
            }
          }
        }
        
        .action-buttons {
          display: flex;
          gap: 8px;
          
          .el-button {
            border-radius: 8px;
            padding: 6px 12px;
            
            &.edit-btn {
              background: #e3f2fd;
              border-color: #bbdefb;
              color: #1976d2;
              
              &:hover {
                background: #bbdefb;
                transform: translateY(-1px);
              }
            }
            
            &.status-btn {
              &.el-button--warning {
                background: #fff3e0;
                border-color: #ffcc02;
                color: #f57c00;
                
                &:hover {
                  background: #ffcc02;
                  transform: translateY(-1px);
                }
              }
              
              &.el-button--success {
                background: #e8f5e8;
                border-color: #4caf50;
                color: #2e7d32;
                
                &:hover {
                  background: #4caf50;
                  transform: translateY(-1px);
                }
              }
            }
            
            &.delete-btn {
              background: #ffebee;
              border-color: #ffcdd2;
              color: #d32f2f;
              
              &:hover {
                background: #ffcdd2;
                transform: translateY(-1px);
              }
            }
          }
        }
      }
    }
    
    .pagination-wrapper {
      margin-top: 24px;
      display: flex;
      justify-content: center;
      
      .modern-pagination {
        :deep(.el-pagination) {
          .el-pager li {
            border-radius: 8px;
            margin: 0 4px;
            
            &.is-active {
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              color: white;
            }
          }
          
          .btn-prev, .btn-next {
            border-radius: 8px;
            margin: 0 4px;
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .modern-header .header-content {
    flex-direction: column;
    gap: 24px;
    text-align: center;
    padding: 0 16px;
    
    .header-right {
      width: 100%;
      justify-content: center;
      flex-wrap: wrap;
    }
  }
  
  .search-section {
    padding: 16px;
    
    .search-card {
      padding: 20px;
      
      .search-form .el-form {
        flex-direction: column;
        align-items: stretch;
        
        .el-form-item {
          width: 100%;
          
          .search-input, .filter-select {
            width: 100%;
          }
        }
      }
    }
  }
  
  .table-section {
    padding: 0 16px 16px;
    
    .table-card {
      padding: 20px;
      
      .table-header {
        flex-direction: column;
        gap: 16px;
        align-items: stretch;
      }
    }
  }
}
</style>
