<template>
  <div class="modern-wrong-answers-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="title-text">
              <h1>错题管理</h1>
              <p>复习错题，提升学习效果</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button @click="goBackToPersonalCenter" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回个人中心</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 统计概览区域 -->
    <div class="search-section">
      <div class="search-card">
        <div class="search-header">
          <h3>错题统计</h3>
          <p>查看您的错题复习情况</p>
        </div>
        <div class="statistics-content">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon color="#f56c6c"><Warning /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.total_wrong }}</div>
                  <div class="stat-label">总错题数</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon color="#67c23a"><Check /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.reviewed_count }}</div>
                  <div class="stat-label">已复习</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon color="#e6a23c"><Clock /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.pending_count }}</div>
                  <div class="stat-label">待复习</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon color="#409eff"><TrendCharts /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.review_rate }}%</div>
                  <div class="stat-label">复习率</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-section">
      <div class="search-card">
        <div class="search-header">
          <h3>搜索和筛选</h3>
          <p>快速查找错题记录</p>
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
              />
            </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.subject_id" placeholder="选择科目" class="filter-select" clearable>
                <el-option
                  v-for="subject in subjects"
                  :key="subject.id"
                  :label="subject.name"
                  :value="subject.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.type" placeholder="选择题型" class="filter-select" clearable>
                <el-option label="单选题" value="single" />
                <el-option label="多选题" value="multiple" />
                <el-option label="判断题" value="judge" />
                <el-option label="填空题" value="fill" />
                <el-option label="简答题" value="essay" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.status" placeholder="选择状态" class="filter-select" clearable>
                <el-option label="已复习" value="reviewed" />
                <el-option label="待复习" value="pending" />
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

    <!-- 错题列表 -->
    <div class="table-section">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>错题列表</h3>
            <p>共 {{ pagination.total }} 道错题</p>
          </div>
          <div class="table-actions">
            <el-button 
              type="success" 
              @click="batchReview" 
              :disabled="selectedAnswers.length === 0"
              class="action-btn"
            >
              <el-icon><Check /></el-icon>
              <span>批量复习</span>
            </el-button>
            <el-button 
              type="primary" 
              @click="batchExport" 
              :disabled="selectedAnswers.length === 0"
              class="action-btn"
            >
              <el-icon><Download /></el-icon>
              <span>批量导出</span>
            </el-button>
            <el-button 
              type="danger" 
              @click="batchDelete" 
              :disabled="selectedAnswers.length === 0"
              class="action-btn"
            >
              <el-icon><Delete /></el-icon>
              <span>批量删除</span>
            </el-button>
          </div>
        </div>
        
        <div class="table-container">
          <el-table 
            :data="wrongAnswers" 
            stripe 
            class="modern-table"
            :loading="loading"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="question_title" label="题目" min-width="250">
              <template #default="{ row }">
                <div class="question-info">
                  <div class="question-title-wrapper">
                    <span class="question-title">{{ row.question_title }}</span>
                  </div>
                  <div class="question-tags">
                    <el-tag :type="getTypeTagType(row.question_type)" size="small" class="type-tag">
                      {{ getTypeLabel(row.question_type) }}
                    </el-tag>
                    <el-tag :type="getSubjectTagType(row.subject_id)" size="small" class="subject-tag">
                      {{ getSubjectName(row.subject_id) }}
                    </el-tag>
                    <el-tag :type="row.is_reviewed ? 'success' : 'warning'" size="small" class="status-tag">
                      {{ row.is_reviewed ? '已复习' : '待复习' }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="user_answer" label="我的答案" width="150" show-overflow-tooltip>
              <template #default="{ row }">
                <span class="user-answer">{{ row.user_answer || '未作答' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="correct_answer" label="正确答案" width="150" show-overflow-tooltip>
              <template #default="{ row }">
                <span class="correct-answer">{{ row.correct_answer }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="exam_title" label="来源考试" width="200" show-overflow-tooltip />
            <el-table-column prop="created_at" label="错题时间" width="160">
              <template #default="{ row }">
                <span class="date-text">{{ formatDate(row.created_at) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="240" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" @click="viewQuestion(row)" class="view-btn">
                    <el-icon><View /></el-icon>
                  </el-button>
                  <el-button 
                    size="small" 
                    type="primary" 
                    @click="reviewQuestion(row)" 
                    v-if="!row.is_reviewed"
                    class="review-btn"
                  >
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button 
                    size="small" 
                    :type="row.is_favorited ? 'warning' : 'primary'"
                    @click="toggleFavorite(row)"
                    class="favorite-btn"
                  >
                    <el-icon>
                      <StarFilled v-if="row.is_favorited" />
                      <Star v-else />
                    </el-icon>
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteWrongAnswer(row)" class="delete-btn">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      
        <!-- 分页 -->
        <div class="pagination-container">
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

    <!-- 题目详情对话框 -->
    <el-dialog
      v-model="showQuestionDialog"
      title="题目详情"
      width="720px"
      :close-on-click-modal="false"
      class="modern-question-dialog"
    >
      <QuestionDetail
        v-if="showQuestionDialog && viewingQuestion"
        :question="viewingQuestion"
        :user-answer="viewingQuestion.user_answer"
        :correct-answer="viewingQuestion.correct_answer"
        :explanation="viewingQuestion.explanation"
        @close="showQuestionDialog = false"
      />
    </el-dialog>

    <!-- 复习模式对话框 -->
    <el-dialog
      v-model="showReviewDialog"
      title="错题复习"
      width="80%"
      :close-on-click-modal="false"
      class="modern-review-dialog"
    >
      <ReviewMode
        v-if="showReviewDialog && reviewingQuestions.length > 0"
        :questions="reviewingQuestions"
        @complete="handleReviewComplete"
        @close="showReviewDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Warning, Check, Clock, TrendCharts, Search, Refresh, Download, Delete, ArrowLeft, View, Edit, Star, StarFilled
} from '@element-plus/icons-vue'
import QuestionDetail from '@/components/question/QuestionDetail.vue'
import ReviewMode from '@/components/question/ReviewMode.vue'
import { examScoringApi } from '@/api/exam_scoring'
import { learningProgressApi } from '@/api/learning_progress'
import { subjectsApi } from '@/api/subjects'
import { formatDate } from '@/utils/format'

export default {
  name: 'WrongAnswers',
  components: {
    QuestionDetail,
    ReviewMode,
    Warning,
    Check,
    Clock,
    TrendCharts,
    Search,
    Refresh,
    Download,
    Delete,
    View,
    Edit,
    Star,
    StarFilled
  },
  setup() {
    const router = useRouter()
    
    // 响应式数据
    const loading = ref(false)
    const wrongAnswers = ref([])
    const selectedAnswers = ref([])
    const subjects = ref([])
    const statistics = ref({
      total_wrong: 0,
      reviewed_count: 0,
      pending_count: 0,
      review_rate: 0
    })
    const showQuestionDialog = ref(false)
    const showReviewDialog = ref(false)
    const viewingQuestion = ref(null)
    const reviewingQuestions = ref([])
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      subject_id: '',
      type: '',
      status: ''
    })
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 返回个人中心
    const goBackToPersonalCenter = () => {
      router.push('/user/dashboard')
    }
    
    // 加载错题列表
    const loadWrongAnswers = async () => {
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
        
        const response = await examScoringApi.getWrongAnswers(params)
        wrongAnswers.value = response.data.items
        
        // 为每个错题检查收藏状态
        for (const wrongAnswer of wrongAnswers.value) {
          await checkFavoriteStatus(wrongAnswer)
        }
        
        pagination.total = response.data.total
      } catch (error) {
        ElMessage.error('加载错题列表失败')
        console.error('Load wrong answers error:', error)
      } finally {
        loading.value = false
      }
    }
    
    // 加载统计信息
    const loadStatistics = async () => {
      try {
        const response = await learningProgressApi.getOverview()
        const overview = response.data
        
        // 映射数据格式 - 使用正确的字段名 learning_stats
        const totalWrong = overview.learning_stats?.total_wrong_answers || 0
        const reviewRate = overview.learning_stats?.review_rate || 0
        
        statistics.value = {
          total_wrong: totalWrong,
          reviewed_count: Math.round(totalWrong * reviewRate / 100),
          pending_count: totalWrong - Math.round(totalWrong * reviewRate / 100),
          review_rate: reviewRate
        }
      } catch (error) {
        console.error('Load statistics error:', error)
        // 如果API失败，尝试从错题列表计算统计
        try {
          const response = await examScoringApi.getWrongAnswers({ page: 1, size: 1000 })
          const wrongAnswers = response.data.items || []
          const reviewedCount = wrongAnswers.filter(wa => wa.is_reviewed).length
          
          statistics.value = {
            total_wrong: wrongAnswers.length,
            reviewed_count: reviewedCount,
            pending_count: wrongAnswers.length - reviewedCount,
            review_rate: wrongAnswers.length > 0 ? Math.round(reviewedCount / wrongAnswers.length * 100) : 0
          }
        } catch (fallbackError) {
          console.error('Fallback statistics calculation error:', fallbackError)
        }
      }
    }
    
    // 加载科目列表
    const loadSubjects = async () => {
      try {
        const response = await subjectsApi.getSubjects()
        // 确保subjects是数组
        subjects.value = Array.isArray(response.data) ? response.data : (response.data.items || [])
      } catch (error) {
        console.error('Load subjects error:', error)
        subjects.value = []
      }
    }
    
    // 搜索
    const handleSearch = () => {
      pagination.page = 1
      loadWrongAnswers()
    }
    
    // 重置
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadWrongAnswers()
    }
    
    // 分页变化
    const handlePageChange = (page) => {
      pagination.page = page
      loadWrongAnswers()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadWrongAnswers()
    }
    
    // 选择变化
    const handleSelectionChange = (selection) => {
      selectedAnswers.value = selection
    }
    
    // 查看题目
    const viewQuestion = (wrongAnswer) => {
      viewingQuestion.value = wrongAnswer
      showQuestionDialog.value = true
    }
    
    // 复习题目
    const reviewQuestion = (wrongAnswer) => {
      reviewingQuestions.value = [wrongAnswer]
      showReviewDialog.value = true
    }
    
    // 批量复习
    const batchReview = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要复习选中的 ${selectedAnswers.value.length} 道错题吗？`,
          '确认批量复习',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        reviewingQuestions.value = selectedAnswers.value
        selectedAnswers.value = []
        showReviewDialog.value = true
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量复习失败')
          console.error('Batch review error:', error)
        }
      }
    }
    
    // 批量导出
    const batchExport = async () => {
      try {
        ElMessage.info('错题导出功能开发中...')
      } catch (error) {
        ElMessage.error('错题导出失败')
        console.error('Export wrong answers error:', error)
      }
    }
    
    // 删除错题
    const deleteWrongAnswer = async (wrongAnswer) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除这道错题吗？此操作不可恢复！`,
          '确认删除',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await examScoringApi.deleteWrongAnswer(wrongAnswer.id)
        ElMessage.success('删除错题成功')
        loadWrongAnswers()
        loadStatistics()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除错题失败')
          console.error('Delete wrong answer error:', error)
        }
      }
    }
    
    // 批量删除
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedAnswers.value.length} 道错题吗？此操作不可恢复！`,
          '确认批量删除',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // 逐个删除
        for (const wrongAnswer of selectedAnswers.value) {
          await examScoringApi.deleteWrongAnswer(wrongAnswer.id)
        }
        
        ElMessage.success('批量删除成功')
        selectedAnswers.value = []
        loadWrongAnswers()
        loadStatistics()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    // 切换收藏
    const toggleFavorite = async (wrongAnswer) => {
      try {
        if (wrongAnswer.is_favorited) {
          await examScoringApi.unfavoriteQuestion(wrongAnswer.question_id)
          wrongAnswer.is_favorited = false
          ElMessage.success('取消收藏成功')
        } else {
          await examScoringApi.favoriteQuestion(wrongAnswer.question_id)
          wrongAnswer.is_favorited = true
          ElMessage.success('收藏成功')
        }
      } catch (error) {
        ElMessage.error(wrongAnswer.is_favorited ? '取消收藏失败' : '收藏失败')
        console.error('Toggle favorite error:', error)
      }
    }

    // 检查收藏状态
    const checkFavoriteStatus = async (wrongAnswer) => {
      try {
        const response = await examScoringApi.getFavoriteStatus(wrongAnswer.question_id)
        wrongAnswer.is_favorited = response.data.is_favorited
      } catch (error) {
        console.error('Check favorite status error:', error)
      }
    }
    
    // 复习完成
    const handleReviewComplete = (results) => {
      ElMessage.success('复习完成')
      showReviewDialog.value = false
      loadWrongAnswers()
      loadStatistics()
    }
    
    // 工具方法
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
    
    const getSubjectTagType = (subjectId) => {
      const colors = ['primary', 'success', 'warning', 'danger', 'info']
      return colors[subjectId % colors.length]
    }
    
    const getSubjectName = (subjectId) => {
      if (!Array.isArray(subjects.value)) {
        return '未知科目'
      }
      const subject = subjects.value.find(s => s.id === subjectId)
      return subject ? subject.name : '未知科目'
    }
    
    // 生命周期
    onMounted(() => {
      loadWrongAnswers()
      loadStatistics()
      loadSubjects()
    })
    
    return {
      loading,
      wrongAnswers,
      selectedAnswers,
      subjects,
      statistics,
      showQuestionDialog,
      showReviewDialog,
      viewingQuestion,
      reviewingQuestions,
      searchForm,
      pagination,
      goBackToPersonalCenter,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewQuestion,
      reviewQuestion,
      batchReview,
      batchExport,
      deleteWrongAnswer,
      batchDelete,
      toggleFavorite,
      handleReviewComplete,
      getTypeLabel,
      getTypeTagType,
      getSubjectTagType,
      getSubjectName,
      formatDate,
      ArrowLeft
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-wrong-answers-management {
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
        gap: 16px;
        
        .title-icon {
          width: 56px;
          height: 56px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;
          color: white;
          backdrop-filter: blur(10px);
        }
        
        .title-text {
          h1 {
            color: white;
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 4px 0;
            letter-spacing: -0.5px;
          }
          
          p {
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
            margin: 0;
            font-weight: 500;
          }
        }
      }
    }
    
    .header-right {
      display: flex;
      gap: 12px;
      
      .back-btn {
        padding: 12px 20px;
        font-weight: 600;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
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

.search-section {
  padding: 32px;
  
  .search-card {
    max-width: 1800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    margin-bottom: 32px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
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
    
    .statistics-content {
      .stat-item {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: all 0.3s ease;
        
        &:hover {
          background: #e9ecef;
          transform: translateY(-2px);
        }
        
        .stat-icon {
          width: 40px;
          height: 40px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: white;
          font-size: 20px;
        }
        
        .stat-info {
          flex: 1;
          
          .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: #1a1a1a;
            line-height: 1;
            margin-bottom: 4px;
          }
          
          .stat-label {
            font-size: 14px;
            color: #666;
            font-weight: 500;
          }
        }
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
        gap: 12px;
        
        .action-btn {
          padding: 10px 20px;
          border-radius: 12px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 6px;
          
          &.el-button--success {
            background: #e8f5e9;
            border-color: #c8e6c9;
            color: #2e7d32;
            
            &:hover:not(:disabled) {
              background: #c8e6c9;
              transform: translateY(-2px);
            }
          }
          
          &.el-button--primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            
            &:hover:not(:disabled) {
              transform: translateY(-2px);
              box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            }
          }
          
          &.el-button--danger {
            background: #ffebee;
            border-color: #ffcdd2;
            color: #d32f2f;
            
            &:hover:not(:disabled) {
              background: #ffcdd2;
              transform: translateY(-2px);
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
          .question-title-wrapper {
            margin-bottom: 8px;
            
            .question-title {
              font-weight: 600;
              color: #1a1a1a;
            }
          }
          
          .question-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            
            .type-tag, .subject-tag, .status-tag {
              border-radius: 8px;
              font-weight: 600;
              padding: 4px 12px;
            }
          }
        }
        
        .user-answer, .correct-answer {
          font-weight: 500;
          color: #1a1a1a;
        }
        
        .date-text {
          color: #6c757d;
          font-size: 13px;
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
            
            &.review-btn {
              background: #e8f5e9;
              border-color: #c8e6c9;
              color: #4caf50;
              
              &:hover {
                background: #c8e6c9;
                transform: translateY(-1px);
              }
            }
            
            &.favorite-btn {
              &.el-button--warning {
                background: #fff3e0;
                border-color: #ff9800;
                color: #f57c00;
                
                &:hover {
                  background: #ffcc02;
                  transform: translateY(-1px);
                }
              }
              
              &.el-button--primary {
                background: #e3f2fd;
                border-color: #bbdefb;
                color: #1976d2;
                
                &:hover {
                  background: #bbdefb;
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
    
    .pagination-container {
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

/* 对话框样式 */
.modern-question-dialog,
.modern-review-dialog {
  :deep(.el-dialog) {
    border-radius: 20px;
    overflow: visible;
    box-shadow: 
      0 25px 50px -12px rgba(0, 0, 0, 0.25),
      0 0 0 1px rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
  
  :deep(.el-dialog__header) {
    background: transparent;
    color: #1f2937;
    padding: 32px 40px 0 40px;
    margin: 0;
    border-bottom: none;
  }
  
  :deep(.el-dialog__title) {
    font-size: 24px;
    font-weight: 700;
    color: #1f2937;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  :deep(.el-dialog__body) {
    padding: 40px;
    background: rgba(255, 255, 255, 0.5);
  }
  
  :deep(.el-dialog__footer) {
    background: rgba(248, 250, 252, 0.8);
    padding: 32px 40px;
    border-top: 1px solid rgba(229, 231, 235, 0.5);
    backdrop-filter: blur(10px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .modern-header .header-content {
    flex-direction: column;
    gap: 24px;
    text-align: center;
    
    .header-right {
      width: 100%;
      justify-content: center;
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
      
      .statistics-content {
        .el-col {
          margin-bottom: 16px;
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