<template>
  <div class="exam-management">
    <div class="page-header">
      <h1>考试管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          创建考试
        </el-button>
        <el-button @click="showTemplateDialog = true">
          <el-icon><Document /></el-icon>
          考试模板
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-card>
        <el-form :model="searchForm" inline>
          <el-form-item label="关键词">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索考试标题"
              clearable
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item label="科目">
            <el-select
              v-model="searchForm.subject_id"
              placeholder="选择科目"
              clearable
              style="width: 200px"
            >
              <el-option
                v-for="subject in subjects"
                :key="subject.id"
                :label="subject.name"
                :value="subject.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select
              v-model="searchForm.status"
              placeholder="选择状态"
              clearable
              style="width: 120px"
            >
              <el-option label="草稿" value="draft" />
              <el-option label="已发布" value="published" />
              <el-option label="进行中" value="ongoing" />
              <el-option label="已结束" value="finished" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item label="创建时间">
            <el-date-picker
              v-model="searchForm.date_range"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
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

    <!-- 考试列表 -->
    <div class="table-section">
      <el-card>
        <div class="table-header">
          <div class="table-title">
            <span>考试列表</span>
            <el-tag v-if="selectedExams.length > 0" type="info">
              已选择 {{ selectedExams.length }} 个考试
            </el-tag>
          </div>
          <div class="table-actions" v-if="selectedExams.length > 0">
            <el-button size="small" @click="batchUpdateStatus('published')">
              批量发布
            </el-button>
            <el-button size="small" @click="batchUpdateStatus('cancelled')">
              批量取消
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete">
              批量删除
            </el-button>
          </div>
        </div>

        <el-table
          :data="exams"
          :loading="loading"
          @selection-change="handleSelectionChange"
          row-key="id"
          stripe
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="考试标题" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="exam-title">
                <span>{{ row.title }}</span>
                <div class="exam-meta">
                  <el-tag :type="getStatusTagType(row.status)" size="small">
                    {{ getStatusLabel(row.status) }}
                  </el-tag>
                  <span class="exam-info">
                    {{ row.question_count }}题 | {{ row.total_points }}分 | {{ formatDuration(row.duration) }}
                  </span>
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
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewExam(row)">
                查看
              </el-button>
              <el-button size="small" type="primary" @click="editExam(row)">
                编辑
              </el-button>
              <el-dropdown @command="(command) => handleAction(command, row)">
                <el-button size="small">
                  更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="toggle-status">
                      {{ row.status === 'published' ? '取消发布' : '发布' }}
                    </el-dropdown-item>
                    <el-dropdown-item command="duplicate">复制</el-dropdown-item>
                    <el-dropdown-item command="preview">预览</el-dropdown-item>
                    <el-dropdown-item command="statistics">统计</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
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
import { Plus, Document, Search, Refresh, ArrowDown } from '@element-plus/icons-vue'
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
    ArrowDown
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

<style scoped>
.exam-management {
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

.header-actions {
  display: flex;
  gap: 10px;
}

.search-section {
  margin-bottom: 20px;
}

.table-section {
  margin-bottom: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 500;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.exam-title {
  line-height: 1.5;
}

.exam-meta {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.exam-info {
  color: #909399;
  font-size: 12px;
}

.time-info {
  font-size: 12px;
}

.time-item {
  margin-bottom: 4px;
}

.time-item:last-child {
  margin-bottom: 0;
}

.time-label {
  color: #909399;
}

.time-value {
  color: #606266;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

:deep(.el-table .el-table__row) {
  cursor: pointer;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f7fa;
}
</style>
