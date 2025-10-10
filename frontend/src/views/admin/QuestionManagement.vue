<template>
  <div class="question-management">
    <div class="page-header">
      <h1>试题管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新增试题
        </el-button>
        <el-button @click="showImportDialog = true">
          <el-icon><Upload /></el-icon>
          批量导入
        </el-button>
        <el-button @click="exportQuestions">
          <el-icon><Download /></el-icon>
          导出试题
        </el-button>
        <el-button @click="downloadTemplate">
          <el-icon><Document /></el-icon>
          下载模板
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
              placeholder="搜索题目内容"
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
          <el-form-item label="题型">
            <el-select
              v-model="searchForm.type"
              placeholder="选择题型"
              clearable
              style="width: 120px"
            >
              <el-option label="单选题" value="single" />
              <el-option label="多选题" value="multiple" />
              <el-option label="判断题" value="judge" />
              <el-option label="填空题" value="fill" />
              <el-option label="简答题" value="essay" />
            </el-select>
          </el-form-item>
          <el-form-item label="难度">
            <el-select
              v-model="searchForm.difficulty"
              placeholder="选择难度"
              clearable
              style="width: 100px"
            >
              <el-option label="简单" value="easy" />
              <el-option label="中等" value="medium" />
              <el-option label="困难" value="hard" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select
              v-model="searchForm.status"
              placeholder="选择状态"
              clearable
              style="width: 100px"
            >
              <el-option label="草稿" value="draft" />
              <el-option label="已发布" value="published" />
              <el-option label="已归档" value="archived" />
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

    <!-- 试题列表 -->
    <div class="table-section">
      <el-card>
        <div class="table-header">
          <div class="table-title">
            <span>试题列表</span>
            <el-tag v-if="selectedQuestions.length > 0" type="info">
              已选择 {{ selectedQuestions.length }} 题
            </el-tag>
          </div>
          <div class="table-actions" v-if="selectedQuestions.length > 0">
            <el-button size="small" @click="batchUpdateStatus('published')">
              批量发布
            </el-button>
            <el-button size="small" @click="batchUpdateStatus('archived')">
              批量归档
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete">
              批量删除
            </el-button>
          </div>
        </div>

        <el-table
          :data="questions"
          :loading="loading"
          @selection-change="handleSelectionChange"
          row-key="id"
          stripe
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="题目" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="question-title">
                <span v-html="formatQuestionTitle(row.title)"></span>
                <div class="question-meta">
                  <el-tag :type="getTypeTagType(row.type)" size="small">
                    {{ getTypeLabel(row.type) }}
                  </el-tag>
                  <el-tag :type="getDifficultyTagType(row.difficulty)" size="small">
                    {{ getDifficultyLabel(row.difficulty) }}
                  </el-tag>
                  <el-tag :type="getStatusTagType(row.status)" size="small">
                    {{ getStatusLabel(row.status) }}
                  </el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="subject_id" label="科目" width="120">
            <template #default="{ row }">
              {{ getSubjectName(row.subject_id) }}
            </template>
          </el-table-column>
          <el-table-column prop="points" label="分值" width="80" />
          <el-table-column prop="created_at" label="创建时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewQuestion(row)">
                查看
              </el-button>
              <el-button size="small" type="primary" @click="editQuestion(row)">
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

    <!-- 创建/编辑试题对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingQuestion ? '编辑试题' : '新增试题'"
      width="80%"
      :close-on-click-modal="false"
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
      width="50%"
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
import { Plus, Upload, Download, Document, Search, Refresh, ArrowDown } from '@element-plus/icons-vue'
import QuestionForm from '@/components/question/QuestionForm.vue'
import QuestionView from '@/components/question/QuestionView.vue'
import QuestionImport from '@/components/question/QuestionImport.vue'
import { questionApi } from '@/api/questions'
import { subjectApi } from '@/api/subjects'
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
    ArrowDown
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
        const response = await subjectApi.getSubjects()
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
    
    const editQuestion = (question) => {
      editingQuestion.value = question
      showCreateDialog.value = true
    }
    
    const handleSubmit = async (questionData) => {
      try {
        if (editingQuestion.value) {
          await questionApi.updateQuestion(editingQuestion.value.id, questionData)
          ElMessage.success('试题更新成功')
        } else {
          await questionApi.createQuestion(questionData)
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
    
    const duplicateQuestion = async (question) => {
      try {
        const duplicateData = { ...question }
        delete duplicateData.id
        delete duplicateData.created_at
        delete duplicateData.updated_at
        duplicateData.title = duplicateData.title + ' (副本)'
        duplicateData.status = 'draft'
        
        await questionApi.createQuestion(duplicateData)
        ElMessage.success('试题复制成功')
        loadQuestions()
      } catch (error) {
        ElMessage.error('复制试题失败')
        console.error('Duplicate question error:', error)
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
        ElMessage.success(`批量${status === 'published' ? '发布' : '归档'}成功`)
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
        
        await questionApi.exportQuestions(params)
        ElMessage.success('导出成功')
      } catch (error) {
        ElMessage.error('导出失败')
        console.error('Export questions error:', error)
      }
    }
    
    const downloadTemplate = async () => {
      try {
        await questionApi.getImportTemplate()
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
      handleSubmit,
      handleAction,
      batchUpdateStatus,
      batchDelete,
      exportQuestions,
      downloadTemplate,
      handleImportSuccess,
      formatQuestionTitle,
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

<style scoped>
.question-management {
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

.question-title {
  line-height: 1.5;
}

.question-meta {
  margin-top: 8px;
  display: flex;
  gap: 5px;
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
