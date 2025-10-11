<template>
  <div class="modern-exam-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><DocumentChecked /></el-icon>
            </div>
            <div class="title-text">
              <h1>考试管理</h1>
              <p>管理所有考试和考试配置</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="$router.push('/admin/exam-creation')" class="add-btn">
            <el-icon><Plus /></el-icon>
            <span>创建考试</span>
          </el-button>
          <el-button @click="exportExams" class="back-btn">
            <el-icon><Download /></el-icon>
            <span>导出考试</span>
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
            <p>共 {{ pagination.total }} 场考试</p>
          </div>
          <div class="table-actions" v-if="selectedExams.length > 0">
            <el-button size="small" type="success" @click="batchUpdateStatus('published')" class="action-btn">
              批量发布
            </el-button>
            <el-button size="small" type="warning" @click="batchUpdateStatus('cancelled')" class="action-btn">
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
                  <div class="exam-avatar">{{ row.title.charAt(0) }}</div>
                  <div class="exam-details">
                    <div class="exam-title-text">{{ row.title }}</div>
                    <div class="exam-meta">
                      <el-tag :type="getStatusTagType(row.status)" size="small" class="meta-tag">
                        {{ getStatusLabel(row.status) }}
                      </el-tag>
                      <span class="meta-text">{{ row.question_count }}题 / {{ row.duration }}分钟</span>
                    </div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="subject_id" label="科目" width="150">
              <template #default="{ row }">
                {{ getSubjectName(row.subject_id) }}
              </template>
            </el-table-column>
            <el-table-column prop="total_points" label="总分" width="100" />
            <el-table-column prop="start_time" label="开始时间" width="160">
              <template #default="{ row }">
                {{ formatDate(row.start_time) || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="end_time" label="结束时间" width="160">
              <template #default="{ row }">
                {{ formatDate(row.end_time) || '-' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="220" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" type="primary" @click="viewExam(row)" class="action-btn view-btn">
                    <el-icon><View /></el-icon>
                  </el-button>
                  <el-button size="small" type="success" @click="editExam(row)" class="action-btn edit-btn">
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

    <!-- 查看考试详情对话框 -->
    <el-dialog
      v-model="showViewDialog"
      title="考试详情"
      width="70%"
      class="modern-exam-dialog"
    >
      <div v-if="viewingExam" class="exam-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="考试ID">{{ viewingExam.id }}</el-descriptions-item>
          <el-descriptions-item label="考试标题">{{ viewingExam.title }}</el-descriptions-item>
          <el-descriptions-item label="科目">{{ getSubjectName(viewingExam.subject_id) }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTagType(viewingExam.status)">
              {{ getStatusLabel(viewingExam.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="考试时长">{{ viewingExam.duration }} 分钟</el-descriptions-item>
          <el-descriptions-item label="总分">{{ viewingExam.total_points }} 分</el-descriptions-item>
          <el-descriptions-item label="题目数量">{{ viewingExam.question_count }} 题</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ formatDate(viewingExam.start_time) || '-' }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{ formatDate(viewingExam.end_time) || '-' }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(viewingExam.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="考试描述" :span="2">
            {{ viewingExam.description || '无描述' }}
          </el-descriptions-item>
        </el-descriptions>
        
        <div class="exam-questions" style="margin-top: 20px;">
          <h4>试题列表（{{ viewingExam.question_count }}题）</h4>
          <el-table :data="examQuestions" border style="margin-top: 10px;">
            <el-table-column prop="id" label="题目ID" width="80" />
            <el-table-column prop="title" label="题目" min-width="200" show-overflow-tooltip />
            <el-table-column prop="type" label="题型" width="100">
              <template #default="{ row }">
                {{ getTypeLabel(row.type) }}
              </template>
            </el-table-column>
            <el-table-column prop="points" label="分值" width="80" />
          </el-table>
        </div>
      </div>
    </el-dialog>

    <!-- 编辑考试对话框 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑考试"
      width="70%"
      class="modern-exam-dialog"
    >
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="120px">
        <el-form-item label="考试标题" prop="title">
          <el-input v-model="editForm.title" placeholder="请输入考试标题" />
        </el-form-item>
        <el-form-item label="考试描述" prop="description">
          <el-input v-model="editForm.description" type="textarea" :rows="3" placeholder="请输入考试描述" />
        </el-form-item>
        <el-form-item label="科目" prop="subject_id">
          <el-select v-model="editForm.subject_id" placeholder="请选择科目" style="width: 100%">
            <el-option
              v-for="subject in subjects"
              :key="subject.id"
              :label="subject.name"
              :value="subject.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="考试时长" prop="duration">
          <el-input-number v-model="editForm.duration" :min="1" :max="300" /> 分钟
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
            v-model="editForm.start_time"
            type="datetime"
            placeholder="选择开始时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="editForm.end_time"
            type="datetime"
            placeholder="选择结束时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="考试状态" prop="status">
          <el-select v-model="editForm.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="进行中" value="ongoing" />
            <el-option label="已结束" value="finished" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="handleEditSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, Search, Refresh, Download, DocumentChecked, ArrowLeft,
  Edit, Delete, View, Switch
} from '@element-plus/icons-vue'
import { examApi } from '@/api/exams'
import { subjectsApi } from '@/api/subjects'
import { questionApi } from '@/api/questions'

export default {
  name: 'ExamManagement',
  components: {
    Plus,
    Search,
    Refresh,
    Download,
    DocumentChecked,
    ArrowLeft,
    Edit,
    Delete,
    View,
    Switch
  },
  setup() {
    const loading = ref(false)
    const exams = ref([])
    const subjects = ref([])
    const selectedExams = ref([])
    const showViewDialog = ref(false)
    const showEditDialog = ref(false)
    const viewingExam = ref(null)
    const examQuestions = ref([])
    const editFormRef = ref(null)
    
    const searchForm = reactive({
      keyword: '',
      subject_id: '',
      status: ''
    })
    
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    const editForm = reactive({
      id: null,
      title: '',
      description: '',
      subject_id: '',
      duration: 60,
      start_time: null,
      end_time: null,
      status: 'draft'
    })
    
    const editRules = {
      title: [{ required: true, message: '请输入考试标题', trigger: 'blur' }],
      subject_id: [{ required: true, message: '请选择科目', trigger: 'change' }],
      duration: [{ required: true, message: '请输入考试时长', trigger: 'blur' }]
    }
    
    const loadExams = async () => {
      try {
        loading.value = true
        const params = {
          page: pagination.page,
          size: pagination.size,
          ...searchForm
        }
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        const response = await examApi.getExams(params)
        exams.value = response.data.items || response.data
        pagination.total = response.data.total || exams.value.length
      } catch (error) {
        ElMessage.error('加载考试列表失败')
        console.error('Load exams error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadSubjects = async () => {
      try {
        const response = await subjectsApi.getSubjects()
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
      searchForm.keyword = ''
      searchForm.subject_id = ''
      searchForm.status = ''
      pagination.page = 1
      loadExams()
    }
    
    const handleSelectionChange = (selection) => {
      selectedExams.value = selection
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
    
    const viewExam = async (exam) => {
      try {
        const response = await examApi.getExam(exam.id)
        viewingExam.value = response.data
        
        // 加载考试题目
        if (viewingExam.value.question_ids && viewingExam.value.question_ids.length > 0) {
          const questionIds = viewingExam.value.question_ids.join(',')
          const questionsResponse = await questionApi.getQuestions({ ids: questionIds })
          examQuestions.value = questionsResponse.data.items || questionsResponse.data
        } else {
          examQuestions.value = []
        }
        
        showViewDialog.value = true
      } catch (error) {
        ElMessage.error('获取考试详情失败')
        console.error('View exam error:', error)
      }
    }
    
    const editExam = (exam) => {
      Object.assign(editForm, {
        id: exam.id,
        title: exam.title,
        description: exam.description || '',
        subject_id: exam.subject_id,
        duration: exam.duration,
        start_time: exam.start_time ? new Date(exam.start_time) : null,
        end_time: exam.end_time ? new Date(exam.end_time) : null,
        status: exam.status
      })
      showEditDialog.value = true
    }
    
    const handleEditSubmit = async () => {
      try {
        await editFormRef.value.validate()
        
        const submitData = {
          title: editForm.title,
          description: editForm.description,
          subject_id: editForm.subject_id,
          duration: editForm.duration,
          start_time: editForm.start_time,
          end_time: editForm.end_time,
          status: editForm.status
        }
        
        await examApi.updateExam(editForm.id, submitData)
        ElMessage.success('考试更新成功')
        showEditDialog.value = false
        loadExams()
      } catch (error) {
        ElMessage.error('更新考试失败')
        console.error('Update exam error:', error)
      }
    }
    
    const toggleExamStatus = async (exam) => {
      try {
        const newStatus = exam.status === 'published' ? 'cancelled' : 'published'
        await examApi.updateExamStatus(exam.id, { status: newStatus })
        ElMessage.success(`考试已${newStatus === 'published' ? '发布' : '取消'}`)
        loadExams()
      } catch (error) {
        ElMessage.error('更新考试状态失败')
        console.error('Toggle status error:', error)
      }
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
        
        const statusText = {
          'published': '发布',
          'cancelled': '取消'
        }
        ElMessage.success(`批量${statusText[status] || '更新'}成功`)
        
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
          `确定要删除选中的 ${selectedExams.value.length} 场考试吗？`,
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
    
    const exportExams = async () => {
      try {
        const params = {}
        if (selectedExams.value.length > 0) {
          params.exam_ids = selectedExams.value.map(e => e.id).join(',')
        } else {
          Object.assign(params, searchForm)
        }
        
        const response = await examApi.exportExams(params)
        
        const blob = new Blob([response], { 
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `考试导出_${new Date().toISOString().slice(0, 10)}.xlsx`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        ElMessage.success('导出成功')
      } catch (error) {
        ElMessage.error('导出失败')
        console.error('Export exams error:', error)
      }
    }
    
    const getSubjectName = (subjectId) => {
      const subject = subjects.value.find(s => s.id === subjectId)
      return subject ? subject.name : '未知科目'
    }
    
    const getStatusLabel = (status) => {
      const labels = {
        'draft': '草稿',
        'published': '已发布',
        'ongoing': '进行中',
        'finished': '已结束',
        'cancelled': '已取消'
      }
      return labels[status] || status
    }
    
    const getStatusTagType = (status) => {
      const types = {
        'draft': 'info',
        'published': 'success',
        'ongoing': 'warning',
        'finished': '',
        'cancelled': 'danger'
      }
      return types[status] || ''
    }
    
    const getTypeLabel = (type) => {
      const labels = {
        'single': '单选题',
        'multiple': '多选题',
        'judge': '判断题',
        'fill': '填空题',
        'essay': '简答题'
      }
      return labels[type] || type
    }
    
    const formatDate = (date) => {
      if (!date) return ''
      const d = new Date(date)
      if (isNaN(d.getTime())) return ''
      return d.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    onMounted(() => {
      loadExams()
      loadSubjects()
    })
    
    return {
      loading,
      exams,
      subjects,
      selectedExams,
      searchForm,
      pagination,
      showViewDialog,
      showEditDialog,
      viewingExam,
      examQuestions,
      editForm,
      editRules,
      editFormRef,
      loadExams,
      handleSearch,
      handleReset,
      handleSelectionChange,
      handlePageChange,
      handleSizeChange,
      viewExam,
      editExam,
      handleEditSubmit,
      toggleExamStatus,
      deleteExam,
      batchUpdateStatus,
      batchDelete,
      exportExams,
      getSubjectName,
      getStatusLabel,
      getStatusTagType,
      getTypeLabel,
      formatDate
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
          border-radius: 8px;
          padding: 8px 16px;
          font-weight: 600;
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
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 16px;
          }
          
          .exam-details {
            flex: 1;
            
            .exam-title-text {
              font-weight: 600;
              color: #1a1a1a;
              margin-bottom: 4px;
            }
            
            .exam-meta {
              display: flex;
              gap: 8px;
              align-items: center;
              
              .meta-tag {
                border-radius: 6px;
                padding: 2px 8px;
                font-size: 12px;
              }
              
              .meta-text {
                font-size: 12px;
                color: #909399;
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
            
            &.view-btn {
              background: #e3f2fd;
              border-color: #bbdefb;
              color: #1976d2;
              
              &:hover {
                background: #bbdefb;
                transform: translateY(-1px);
              }
            }
            
            &.edit-btn {
              background: #e8f5e9;
              border-color: #c8e6c9;
              color: #388e3c;
              
              &:hover {
                background: #c8e6c9;
                transform: translateY(-1px);
              }
            }
            
            &.status-btn {
              background: #fff3e0;
              border-color: #ffe0b2;
              color: #f57c00;
              
              &:hover {
                background: #ffe0b2;
                transform: translateY(-1px);
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

.exam-detail {
  .exam-questions {
    h4 {
      font-size: 16px;
      font-weight: 600;
      color: #1a1a1a;
      margin: 0 0 10px 0;
    }
  }
}

.modern-exam-dialog {
  :deep(.el-dialog__header) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    
    .el-dialog__title {
      color: white;
      font-weight: 700;
      font-size: 20px;
    }
    
    .el-dialog__headerbtn .el-dialog__close {
      color: white;
      font-size: 20px;
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
