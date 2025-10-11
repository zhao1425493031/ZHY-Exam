<template>
  <div class="modern-question-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="title-text">
              <h1>试题管理</h1>
              <p>管理题库和试题内容</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="showCreateDialog = true" class="add-btn">
            <el-icon><Plus /></el-icon>
            <span>新增试题</span>
          </el-button>
          <el-button @click="showImportDialog = true" class="back-btn">
            <el-icon><Upload /></el-icon>
            <span>批量导入</span>
          </el-button>
          <el-button @click="exportQuestions" class="back-btn">
            <el-icon><Download /></el-icon>
            <span>导出试题</span>
          </el-button>
          <el-button @click="downloadTemplate" class="back-btn">
            <el-icon><Document /></el-icon>
            <span>下载模板</span>
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
          <p>快速查找试题信息</p>
        </div>
        <div class="search-form">
          <el-form :model="searchForm" inline>
            <el-form-item>
              <el-input
                v-model="searchForm.keyword"
                placeholder="请输入题目内容"
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
                v-model="searchForm.type"
                placeholder="选择题型"
                clearable
                class="filter-select"
              >
                <el-option label="单选题" value="single" />
                <el-option label="多选题" value="multiple" />
                <el-option label="判断题" value="judge" />
                <el-option label="填空题" value="fill" />
                <el-option label="简答题" value="essay" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-select
                v-model="searchForm.difficulty"
                placeholder="选择难度"
                clearable
                class="filter-select"
              >
                <el-option label="简单" value="easy" />
                <el-option label="中等" value="medium" />
                <el-option label="困难" value="hard" />
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
                <el-option label="已归档" value="archived" />
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

    <!-- 试题列表 -->
    <div class="table-section">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>试题列表</h3>
            <p>共 {{ pagination.total }} 个试题</p>
          </div>
          <div class="table-actions" v-if="selectedQuestions.length > 0">
            <el-button size="small" type="info" @click="batchUpdateStatus('draft')" class="action-btn">
              批量草稿
            </el-button>
            <el-button size="small" type="success" @click="batchUpdateStatus('published')" class="action-btn">
              批量发布
            </el-button>
            <el-button size="small" type="warning" @click="batchUpdateStatus('archived')" class="action-btn">
              批量归档
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete" class="action-btn">
              批量删除
            </el-button>
          </div>
        </div>
        
        <div class="table-container">
          <el-table
            :data="questions"
            :loading="loading"
            @selection-change="handleSelectionChange"
            row-key="id"
            stripe
            class="modern-table"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="title" label="题目" min-width="200" show-overflow-tooltip>
              <template #default="{ row }">
                <div class="question-info">
                  <div class="question-avatar">{{ getTypeLabel(row.type).charAt(0) }}</div>
                  <div class="question-details">
                    <div class="question-title-text">{{ row.title }}</div>
                    <div class="question-meta">
                      <el-tag :type="getTypeTagType(row.type)" size="small" class="meta-tag">
                        {{ getTypeLabel(row.type) }}
                      </el-tag>
                      <el-tag :type="getDifficultyTagType(row.difficulty)" size="small" class="meta-tag">
                        {{ getDifficultyLabel(row.difficulty) }}
                      </el-tag>
                      <el-tag :type="getStatusTagType(row.status)" size="small" class="meta-tag">
                        {{ getStatusLabel(row.status) }}
                      </el-tag>
                    </div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="subject_id" label="科目" width="300">
              <template #default="{ row }">
                {{ getSubjectName(row.subject_id) }}
              </template>
            </el-table-column>
            <el-table-column prop="points" label="分值" width="100" />
            <el-table-column prop="created_at" label="创建时间" width="160">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" type="primary" @click="editQuestion(row)" class="action-btn edit-btn">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button size="small" type="warning" @click="toggleQuestionStatus(row)" class="action-btn status-btn">
                    <el-icon><Switch /></el-icon>
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteQuestion(row)" class="action-btn delete-btn">
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

    <!-- 创建/编辑试题对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingQuestion ? '编辑试题' : '新增试题'"
      width="80%"
      :close-on-click-modal="false"
      class="modern-question-dialog"
    >
      <QuestionForm
        v-if="showCreateDialog"
        :question="editingQuestion"
        :subjects="subjects"
        @submit="handleSubmit"
        @cancel="showCreateDialog = false"
      />
    </el-dialog>

    <!-- 查看试题对话框 -->
    <el-dialog
      v-model="showViewDialog"
      title="试题详情"
      width="60%"
      class="modern-question-dialog"
    >
      <QuestionView
        v-if="showViewDialog && viewingQuestion"
        :question="viewingQuestion"
        :subjects="subjects"
      />
    </el-dialog>

    <!-- 批量导入对话框 -->
    <el-dialog
      v-model="showImportDialog"
      title="批量导入试题"
      width="85%"
      class="modern-question-dialog"
    >
      <QuestionImport
        v-if="showImportDialog"
        :subjects="subjects"
        @success="handleImportSuccess"
        @cancel="showImportDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Upload, Download, Document, Search, Refresh, ArrowLeft, Edit, Switch, Delete } from '@element-plus/icons-vue'
import QuestionForm from '@/components/question/QuestionForm.vue'
import QuestionView from '@/components/question/QuestionView.vue'
import QuestionImport from '@/components/question/QuestionImport.vue'
import { questionApi } from '@/api/questions'
import { subjectsApi } from '@/api/subjects'
import { formatDate } from '@/utils/format'

export default {
  name: 'QuestionManagement',
  components: {
    QuestionForm,
    QuestionView,
    QuestionImport,
    Plus,
    Upload,
    Download,
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
    const questions = ref([])
    const subjects = ref([])
    const selectedQuestions = ref([])
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      subject_id: '',
      type: '',
      difficulty: '',
      status: ''
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
    const showImportDialog = ref(false)
    const editingQuestion = ref(null)
    const viewingQuestion = ref(null)
    
    // 计算属性
    const getSubjectName = computed(() => {
      return (subjectId) => {
        const subject = subjects.value.find(s => s.id === subjectId)
        return subject ? subject.name : '未知科目'
      }
    })
    
    // 方法
    const loadQuestions = async () => {
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
        
        const response = await questionApi.getQuestions(params)
        questions.value = response.data.items
        pagination.total = response.data.total
      } catch (error) {
        ElMessage.error('加载试题列表失败')
        console.error('Load questions error:', error)
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
      loadQuestions()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadQuestions()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadQuestions()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadQuestions()
    }
    
    const handleSelectionChange = (selection) => {
      selectedQuestions.value = selection
    }
    
    const viewQuestion = (question) => {
      viewingQuestion.value = question
      showViewDialog.value = true
    }
    
    const toggleQuestionStatus = async (question) => {
      try {
        const newStatus = question.status === 'published' ? 'draft' : 'published'
        await questionApi.updateQuestionStatus(question.id, { status: newStatus })
        ElMessage.success(`试题已${newStatus === 'published' ? '发布' : '取消发布'}`)
        loadQuestions()
      } catch (error) {
        ElMessage.error('更新试题状态失败')
        console.error('Toggle status error:', error)
      }
    }
    
    const editQuestion = (question) => {
      editingQuestion.value = question
      showCreateDialog.value = true
    }
    
    const handleSubmit = async (questionData) => {
      try {
        // 过滤掉不应该发送的字段
        const submitData = { ...questionData }
        delete submitData.id
        delete submitData.created_at
        delete submitData.updated_at
        delete submitData.created_by
        
        // 转换选项格式：从对象数组转换为字符串数组
        if (submitData.options && Array.isArray(submitData.options)) {
          if (submitData.options.length > 0 && typeof submitData.options[0] === 'object') {
            // 如果是对象数组，转换为字符串数组
            submitData.options = submitData.options.map(opt => opt.text || opt)
          }
        } else if (submitData.options === null || submitData.options === undefined) {
          // 对于essay和judge类型，如果options为null，删除该字段
          delete submitData.options
        }
        
        if (editingQuestion.value) {
          await questionApi.updateQuestion(editingQuestion.value.id, submitData)
          ElMessage.success('试题更新成功')
        } else {
          await questionApi.createQuestion(submitData)
          ElMessage.success('试题创建成功')
        }
        
        showCreateDialog.value = false
        editingQuestion.value = null
        loadQuestions()
      } catch (error) {
        ElMessage.error('保存试题失败')
        console.error('Submit question error:', error)
      }
    }
    
    const handleAction = async (command, question) => {
      switch (command) {
        case 'toggle-status':
          await toggleQuestionStatus(question)
          break
        case 'duplicate':
          await duplicateQuestion(question)
          break
        case 'delete':
          await deleteQuestion(question)
          break
      }
    }
    
    const deleteQuestion = async (question) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除试题"${question.title}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await questionApi.deleteQuestion(question.id)
        ElMessage.success('试题删除成功')
        loadQuestions()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除试题失败')
          console.error('Delete question error:', error)
        }
      }
    }
    
    const batchUpdateStatus = async (status) => {
      try {
        const ids = selectedQuestions.value.map(q => q.id)
        await questionApi.batchUpdateStatus({ ids, status })
        
        // 根据状态显示不同的提示信息
        const statusText = {
          'draft': '设为草稿',
          'published': '发布',
          'archived': '归档'
        }
        ElMessage.success(`批量${statusText[status] || '更新'}成功`)
        
        selectedQuestions.value = []
        loadQuestions()
      } catch (error) {
        ElMessage.error('批量更新状态失败')
        console.error('Batch update status error:', error)
      }
    }
    
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedQuestions.value.length} 个试题吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const ids = selectedQuestions.value.map(q => q.id)
        await questionApi.batchDelete({ ids })
        ElMessage.success('批量删除成功')
        selectedQuestions.value = []
        loadQuestions()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    const exportQuestions = async () => {
      try {
        const params = {}
        if (selectedQuestions.value.length > 0) {
          params.question_ids = selectedQuestions.value.map(q => q.id).join(',')
        } else {
          Object.assign(params, searchForm)
        }
        
        const response = await questionApi.exportQuestions(params)
        
        // 创建Blob并下载文件
        const blob = new Blob([response], { 
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `试题导出_${new Date().toISOString().slice(0, 10)}.xlsx`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        ElMessage.success('导出成功')
      } catch (error) {
        ElMessage.error('导出失败')
        console.error('Export questions error:', error)
      }
    }
    
    const downloadTemplate = async () => {
      try {
        const response = await questionApi.getImportTemplate()
        const blob = new Blob([response], { 
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `试题导入模板_${new Date().toISOString().slice(0, 10)}.xlsx`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        ElMessage.success('模板下载成功')
      } catch (error) {
        ElMessage.error('下载模板失败')
        console.error('Download template error:', error)
      }
    }
    
    const handleImportSuccess = () => {
      showImportDialog.value = false
      loadQuestions()
    }
    
    // 工具方法
    const formatQuestionTitle = (title) => {
      if (!title) return ''
      return title.replace(/\n/g, '<br>')
    }
    
    const getTypeLabel = (type) => {
      const labels = {
        single: '单选题',
        multiple: '多选题',
        judge: '判断题',
        fill: '填空题',
        essay: '简答题'
      }
      return labels[type] || type
    }
    
    const getTypeTagType = (type) => {
      const types = {
        single: 'primary',
        multiple: 'success',
        judge: 'warning',
        fill: 'info',
        essay: 'danger'
      }
      return types[type] || 'default'
    }
    
    const getDifficultyLabel = (difficulty) => {
      const labels = {
        easy: '简单',
        medium: '中等',
        hard: '困难'
      }
      return labels[difficulty] || difficulty
    }
    
    const getDifficultyTagType = (difficulty) => {
      const types = {
        easy: 'success',
        medium: 'warning',
        hard: 'danger'
      }
      return types[difficulty] || 'default'
    }
    
    const getStatusLabel = (status) => {
      const labels = {
        draft: '草稿',
        published: '已发布',
        archived: '已归档'
      }
      return labels[status] || status
    }
    
    const getStatusTagType = (status) => {
      const types = {
        draft: 'info',
        published: 'success',
        archived: 'warning'
      }
      return types[status] || 'default'
    }
    
    // 生命周期
    onMounted(() => {
      loadSubjects()
      loadQuestions()
    })
    
    return {
      loading,
      questions,
      subjects,
      selectedQuestions,
      searchForm,
      pagination,
      showCreateDialog,
      showViewDialog,
      showImportDialog,
      editingQuestion,
      viewingQuestion,
      getSubjectName,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewQuestion,
      editQuestion,
      toggleQuestionStatus,
      deleteQuestion,
      handleSubmit,
      handleAction,
      batchUpdateStatus,
      batchDelete,
      exportQuestions,
      downloadTemplate,
      handleImportSuccess,
      getTypeLabel,
      getTypeTagType,
      getDifficultyLabel,
      getDifficultyTagType,
      getStatusLabel,
      getStatusTagType,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-question-management {
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
        
        .question-info {
          display: flex;
          align-items: center;
          gap: 12px;
          
          .question-avatar {
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
          
          .question-details {
            flex: 1;
            
            .question-title-text {
              font-weight: 600;
              color: #1a1a1a;
              margin-bottom: 8px;
              line-height: 1.4;
            }
            
            .question-meta {
              display: flex;
              gap: 6px;
              flex-wrap: wrap;
              
              .meta-tag {
                border-radius: 6px;
                font-size: 12px;
                padding: 2px 8px;
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
