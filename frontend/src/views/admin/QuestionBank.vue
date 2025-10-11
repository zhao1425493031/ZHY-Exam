<template>
  <div class="modern-question-bank">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Collection /></el-icon>
            </div>
            <div class="title-text">
              <h1>题库管理</h1>
              <p>试题分类、标签和统计管理</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="$router.push('/admin/questions')" class="add-btn">
            <el-icon><Plus /></el-icon>
            <span>添加试题</span>
          </el-button>
          <el-button @click="showTagDialog = true" class="back-btn">
            <el-icon><PriceTag /></el-icon>
            <span>标签管理</span>
          </el-button>
          <el-button @click="exportByCategory" class="back-btn">
            <el-icon><Download /></el-icon>
            <span>分类导出</span>
          </el-button>
          <el-button @click="$router.push('/admin')" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回控制台</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-section">
      <div class="stats-container">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.total || 0 }}</div>
            <div class="stat-label">试题总数</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <el-icon><Collection /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.subjects || 0 }}</div>
            <div class="stat-label">科目数量</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <el-icon><PriceTag /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.tags || 0 }}</div>
            <div class="stat-label">标签数量</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <el-icon><Select /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.published || 0 }}</div>
            <div class="stat-label">已发布</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-section">
      <div class="search-card">
        <div class="search-header">
          <h3>搜索和筛选</h3>
          <p>按分类、标签、难度筛选试题</p>
        </div>
        <div class="search-form">
          <el-form :model="searchForm" inline>
            <el-form-item>
              <el-input
                v-model="searchForm.keyword"
                placeholder="请输入关键词"
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
                v-model="searchForm.tag"
                placeholder="选择标签"
                clearable
                class="filter-select"
              >
                <el-option
                  v-for="tag in allTags"
                  :key="tag"
                  :label="tag"
                  :value="tag"
                />
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

    <!-- 分类视图区域 -->
    <div class="category-section">
      <div class="category-card">
        <div class="category-header">
          <h3>按科目分类</h3>
          <p>查看各科目试题分布</p>
        </div>
        <div class="category-grid">
          <div
            v-for="subject in subjects"
            :key="subject.id"
            class="category-item"
            @click="filterBySubject(subject.id)"
          >
            <div class="category-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="category-name">{{ subject.name }}</div>
            <div class="category-count">{{ getSubjectQuestionCount(subject.id) }} 题</div>
          </div>
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
            <el-button size="small" type="primary" @click="showBatchTagDialog = true" class="action-btn">
              批量打标签
            </el-button>
            <el-button size="small" type="warning" @click="batchExport" class="action-btn">
              批量导出
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
            <el-table-column prop="tags" label="标签" width="200">
              <template #default="{ row }">
                <el-tag
                  v-for="(tag, index) in row.tags"
                  :key="index"
                  size="small"
                  style="margin-right: 4px;"
                >
                  {{ tag }}
                </el-tag>
                <span v-if="!row.tags || row.tags.length === 0" style="color: #909399;">无标签</span>
              </template>
            </el-table-column>
            <el-table-column prop="points" label="分值" width="80" />
            <el-table-column prop="usage_count" label="使用次数" width="100">
              <template #default="{ row }">
                {{ row.usage_count || 0 }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" type="primary" @click="editQuestionTags(row)" class="action-btn edit-btn">
                    <el-icon><Edit /></el-icon>
                    标签
                  </el-button>
                  <el-button size="small" type="success" @click="viewQuestion(row)" class="action-btn view-btn">
                    <el-icon><View /></el-icon>
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

    <!-- 标签管理对话框 -->
    <el-dialog
      v-model="showTagDialog"
      title="标签管理"
      width="60%"
      class="modern-dialog"
    >
      <div class="tag-management">
        <div class="tag-input-section">
          <el-input
            v-model="newTag"
            placeholder="输入新标签名称"
            @keyup.enter="addTag"
          >
            <template #append>
              <el-button type="primary" @click="addTag">添加</el-button>
            </template>
          </el-input>
        </div>
        <div class="tag-list">
          <el-tag
            v-for="(tag, index) in allTags"
            :key="index"
            closable
            @close="removeTag(tag)"
            size="large"
            style="margin: 8px;"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </el-dialog>

    <!-- 编辑试题标签对话框 -->
    <el-dialog
      v-model="showEditTagDialog"
      title="编辑试题标签"
      width="50%"
      class="modern-dialog"
    >
      <div v-if="editingQuestion">
        <p style="margin-bottom: 16px; color: #606266;">
          <strong>题目：</strong>{{ editingQuestion.title }}
        </p>
        <el-select
          v-model="editingQuestion.tags"
          multiple
          filterable
          allow-create
          placeholder="选择或输入标签"
          style="width: 100%"
        >
          <el-option
            v-for="tag in allTags"
            :key="tag"
            :label="tag"
            :value="tag"
          />
        </el-select>
      </div>
      <template #footer>
        <el-button @click="showEditTagDialog = false">取消</el-button>
        <el-button type="primary" @click="saveQuestionTags">保存</el-button>
      </template>
    </el-dialog>

    <!-- 批量打标签对话框 -->
    <el-dialog
      v-model="showBatchTagDialog"
      title="批量打标签"
      width="50%"
      class="modern-dialog"
    >
      <p style="margin-bottom: 16px; color: #606266;">
        已选择 <strong>{{ selectedQuestions.length }}</strong> 个试题
      </p>
      <el-select
        v-model="batchTags"
        multiple
        filterable
        allow-create
        placeholder="选择或输入标签"
        style="width: 100%"
      >
        <el-option
          v-for="tag in allTags"
          :key="tag"
          :label="tag"
          :value="tag"
        />
      </el-select>
      <template #footer>
        <el-button @click="showBatchTagDialog = false">取消</el-button>
        <el-button type="primary" @click="saveBatchTags">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, Search, Refresh, Download, Collection, ArrowLeft,
  Edit, View, Document, PriceTag, Select
} from '@element-plus/icons-vue'
import { questionApi } from '@/api/questions'
import { subjectsApi } from '@/api/subjects'

export default {
  name: 'QuestionBank',
  components: {
    Plus,
    Search,
    Refresh,
    Download,
    Collection,
    ArrowLeft,
    Edit,
    View,
    Document,
    PriceTag,
    Select
  },
  setup() {
    const loading = ref(false)
    const questions = ref([])
    const subjects = ref([])
    const allTags = ref([])
    const selectedQuestions = ref([])
    const showTagDialog = ref(false)
    const showEditTagDialog = ref(false)
    const showBatchTagDialog = ref(false)
    const editingQuestion = ref(null)
    const newTag = ref('')
    const batchTags = ref([])
    
    const stats = reactive({
      total: 0,
      subjects: 0,
      tags: 0,
      published: 0
    })
    
    const searchForm = reactive({
      keyword: '',
      subject_id: '',
      type: '',
      difficulty: '',
      tag: ''
    })
    
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    const loadQuestions = async () => {
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
        const response = await questionApi.getQuestions(params)
        questions.value = response.data.items || response.data
        pagination.total = response.data.total || questions.value.length
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
        stats.subjects = subjects.value.length
      } catch (error) {
        console.error('Load subjects error:', error)
      }
    }
    
    const loadStats = async () => {
      try {
        const response = await questionApi.getQuestionStats()
        Object.assign(stats, response.data)
      } catch (error) {
        console.error('Load stats error:', error)
      }
    }
    
    const loadAllTags = () => {
      const tagsSet = new Set()
      questions.value.forEach(q => {
        if (q.tags && Array.isArray(q.tags)) {
          q.tags.forEach(tag => tagsSet.add(tag))
        }
      })
      allTags.value = Array.from(tagsSet).sort()
      stats.tags = allTags.value.length
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadQuestions()
    }
    
    const handleReset = () => {
      searchForm.keyword = ''
      searchForm.subject_id = ''
      searchForm.type = ''
      searchForm.difficulty = ''
      searchForm.tag = ''
      pagination.page = 1
      loadQuestions()
    }
    
    const handleSelectionChange = (selection) => {
      selectedQuestions.value = selection
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
    
    const filterBySubject = (subjectId) => {
      searchForm.subject_id = subjectId
      handleSearch()
    }
    
    const getSubjectQuestionCount = (subjectId) => {
      return questions.value.filter(q => q.subject_id === subjectId).length
    }
    
    const addTag = () => {
      if (!newTag.value.trim()) {
        ElMessage.warning('请输入标签名称')
        return
      }
      if (allTags.value.includes(newTag.value.trim())) {
        ElMessage.warning('标签已存在')
        return
      }
      allTags.value.push(newTag.value.trim())
      allTags.value.sort()
      stats.tags = allTags.value.length
      newTag.value = ''
      ElMessage.success('标签添加成功')
    }
    
    const removeTag = (tag) => {
      ElMessageBox.confirm(
        `确定要删除标签"${tag}"吗？`,
        '确认删除',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        allTags.value = allTags.value.filter(t => t !== tag)
        stats.tags = allTags.value.length
        ElMessage.success('标签删除成功')
      }).catch(() => {})
    }
    
    const editQuestionTags = (question) => {
      editingQuestion.value = { ...question, tags: question.tags || [] }
      showEditTagDialog.value = true
    }
    
    const saveQuestionTags = async () => {
      try {
        const submitData = {
          subject_id: editingQuestion.value.subject_id,
          type: editingQuestion.value.type,
          title: editingQuestion.value.title,
          answer: editingQuestion.value.answer,
          tags: editingQuestion.value.tags
        }
        
        await questionApi.updateQuestion(editingQuestion.value.id, submitData)
        ElMessage.success('标签保存成功')
        showEditTagDialog.value = false
        loadQuestions()
        loadAllTags()
      } catch (error) {
        ElMessage.error('保存标签失败')
        console.error('Save tags error:', error)
      }
    }
    
    const saveBatchTags = async () => {
      try {
        const promises = selectedQuestions.value.map(q => {
          const currentTags = q.tags || []
          const newTags = [...new Set([...currentTags, ...batchTags.value])]
          return questionApi.updateQuestion(q.id, {
            subject_id: q.subject_id,
            type: q.type,
            title: q.title,
            answer: q.answer,
            tags: newTags
          })
        })
        
        await Promise.all(promises)
        ElMessage.success('批量打标签成功')
        showBatchTagDialog.value = false
        batchTags.value = []
        selectedQuestions.value = []
        loadQuestions()
        loadAllTags()
      } catch (error) {
        ElMessage.error('批量打标签失败')
        console.error('Batch tag error:', error)
      }
    }
    
    const viewQuestion = (question) => {
      // 跳转到试题管理页面查看详情
      window.open(`/admin/questions?id=${question.id}`, '_blank')
    }
    
    const batchExport = async () => {
      try {
        const ids = selectedQuestions.value.map(q => q.id).join(',')
        const response = await questionApi.exportQuestions({ question_ids: ids })
        
        const blob = new Blob([response], { 
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `题库导出_${new Date().toISOString().slice(0, 10)}.xlsx`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        ElMessage.success('导出成功')
      } catch (error) {
        ElMessage.error('导出失败')
        console.error('Export error:', error)
      }
    }
    
    const exportByCategory = async () => {
      try {
        const params = { ...searchForm }
        const response = await questionApi.exportQuestions(params)
        
        const blob = new Blob([response], { 
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `分类导出_${new Date().toISOString().slice(0, 10)}.xlsx`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        ElMessage.success('导出成功')
      } catch (error) {
        ElMessage.error('导出失败')
        console.error('Export error:', error)
      }
    }
    
    const getSubjectName = (subjectId) => {
      const subject = subjects.value.find(s => s.id === subjectId)
      return subject ? subject.name : '未知科目'
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
    
    const getTypeTagType = (type) => {
      const types = {
        'single': 'primary',
        'multiple': 'success',
        'judge': 'warning',
        'fill': 'info',
        'essay': 'danger'
      }
      return types[type] || ''
    }
    
    const getDifficultyLabel = (difficulty) => {
      const labels = {
        'easy': '简单',
        'medium': '中等',
        'hard': '困难'
      }
      return labels[difficulty] || difficulty
    }
    
    const getDifficultyTagType = (difficulty) => {
      const types = {
        'easy': 'success',
        'medium': 'warning',
        'hard': 'danger'
      }
      return types[difficulty] || ''
    }
    
    onMounted(async () => {
      await loadSubjects()
      await loadQuestions()
      await loadStats()
      loadAllTags()
    })
    
    return {
      loading,
      questions,
      subjects,
      allTags,
      selectedQuestions,
      showTagDialog,
      showEditTagDialog,
      showBatchTagDialog,
      editingQuestion,
      newTag,
      batchTags,
      stats,
      searchForm,
      pagination,
      loadQuestions,
      handleSearch,
      handleReset,
      handleSelectionChange,
      handlePageChange,
      handleSizeChange,
      filterBySubject,
      getSubjectQuestionCount,
      addTag,
      removeTag,
      editQuestionTags,
      saveQuestionTags,
      saveBatchTags,
      viewQuestion,
      batchExport,
      exportByCategory,
      getSubjectName,
      getTypeLabel,
      getTypeTagType,
      getDifficultyLabel,
      getDifficultyTagType
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-question-bank {
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

.stats-section {
  padding: 32px;
  
  .stats-container {
    max-width: 1800px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
    
    .stat-card {
      background: rgba(255, 255, 255, 0.95);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      align-items: center;
      gap: 20px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
      }
      
      .stat-icon {
        width: 60px;
        height: 60px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        
        .el-icon {
          font-size: 28px;
          color: white;
        }
      }
      
      .stat-content {
        flex: 1;
        
        .stat-value {
          font-size: 32px;
          font-weight: 700;
          color: #1a1a1a;
          line-height: 1;
          margin-bottom: 8px;
        }
        
        .stat-label {
          font-size: 14px;
          color: #666;
          font-weight: 500;
        }
      }
    }
  }
}

.search-section {
  padding: 0 32px 32px;
  
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

.category-section {
  padding: 0 32px 32px;
  
  .category-card {
    max-width: 1800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    
    .category-header {
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
    
    .category-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 16px;
      
      .category-item {
        background: white;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #e9ecef;
        
        &:hover {
          transform: translateY(-4px);
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
          border-color: #667eea;
        }
        
        .category-icon {
          width: 48px;
          height: 48px;
          border-radius: 10px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          
          .el-icon {
            font-size: 24px;
            color: white;
          }
        }
        
        .category-name {
          font-size: 16px;
          font-weight: 600;
          color: #1a1a1a;
          text-align: center;
        }
        
        .category-count {
          font-size: 14px;
          color: #909399;
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
        
        .question-info {
          display: flex;
          align-items: center;
          gap: 12px;
          
          .question-avatar {
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
          
          .question-details {
            flex: 1;
            
            .question-title-text {
              font-weight: 600;
              color: #1a1a1a;
              margin-bottom: 4px;
            }
            
            .question-meta {
              display: flex;
              gap: 8px;
              align-items: center;
              
              .meta-tag {
                border-radius: 6px;
                padding: 2px 8px;
                font-size: 12px;
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
            
            &.view-btn {
              background: #e8f5e9;
              border-color: #c8e6c9;
              color: #388e3c;
              
              &:hover {
                background: #c8e6c9;
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

.tag-management {
  .tag-input-section {
    margin-bottom: 24px;
  }
  
  .tag-list {
    min-height: 200px;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
  }
}

.modern-dialog {
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
  
  .stats-section {
    padding: 16px;
    
    .stats-container {
      grid-template-columns: 1fr;
    }
  }
  
  .search-section {
    padding: 0 16px 16px;
    
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
  
  .category-section {
    padding: 0 16px 16px;
    
    .category-card {
      padding: 20px;
      
      .category-grid {
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
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
