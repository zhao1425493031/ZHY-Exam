<template>
  <div class="wrong-answers">
    <div class="page-header">
      <h1>错题管理</h1>
      <div class="header-info">
        <el-tag type="info">共 {{ wrongAnswers.length }} 道错题</el-tag>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="statistics-overview">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon color="#f56c6c"><Warning /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ statistics.total_wrong }}</div>
                <div class="stat-label">总错题数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon color="#67c23a"><Check /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ statistics.reviewed_count }}</div>
                <div class="stat-label">已复习</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon color="#e6a23c"><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ statistics.pending_count }}</div>
              <div class="stat-label">待复习</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon color="#409eff"><TrendCharts /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ statistics.review_rate }}%</div>
                <div class="stat-label">复习率</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
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
              v-model="searchForm.question_type"
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
          <el-form-item label="复习状态">
            <el-select
              v-model="searchForm.is_reviewed"
              placeholder="选择状态"
              clearable
              style="width: 120px"
            >
              <el-option label="已复习" :value="true" />
              <el-option label="待复习" :value="false" />
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

    <!-- 错题列表 -->
    <div class="wrong-answers-list">
      <el-card>
        <div class="list-header">
          <div class="list-title">
            <span>错题列表</span>
            <el-tag v-if="selectedAnswers.length > 0" type="info">
              已选择 {{ selectedAnswers.length }} 道错题
            </el-tag>
          </div>
          <div class="list-actions" v-if="selectedAnswers.length > 0">
            <el-button size="small" type="success" @click="batchReview">
              <el-icon><Check /></el-icon>
              批量标记复习
            </el-button>
            <el-button size="small" @click="batchExport">
              <el-icon><Download /></el-icon>
              批量导出
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete">
              <el-icon><Delete /></el-icon>
              批量删除
            </el-button>
          </div>
        </div>

        <el-table
          :data="wrongAnswers"
          :loading="loading"
          @selection-change="handleSelectionChange"
          row-key="id"
          stripe
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="question_title" label="题目" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="question-title">
                <span>{{ row.question_title }}</span>
                <div class="question-meta">
                  <el-tag :type="getTypeTagType(row.question_type)" size="small">
                    {{ getTypeLabel(row.question_type) }}
                  </el-tag>
                  <el-tag :type="getSubjectTagType(row.subject_id)" size="small">
                    {{ getSubjectName(row.subject_id) }}
                  </el-tag>
                  <el-tag :type="row.is_reviewed ? 'success' : 'warning'" size="small">
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
          <el-table-column prop="correct_answer" label="正确答案" width="500" show-overflow-tooltip>
            <template #default="{ row }">
              <span class="correct-answer">{{ row.correct_answer }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="exam_title" label="来源考试" width="250" show-overflow-tooltip />
          <el-table-column prop="created_at" label="错题时间" width="200">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewQuestion(row)">
                查看
              </el-button>
              <el-button size="small" type="primary" @click="reviewQuestion(row)" v-if="!row.is_reviewed">
                复习
              </el-button>
              <el-dropdown @command="(command) => handleAction(command, row)">
                <el-button size="small">
                  更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="retake" v-if="row.exam_id">重新考试</el-dropdown-item>
                    <el-dropdown-item command="favorite">收藏题目</el-dropdown-item>
                    <el-dropdown-item command="export">导出错题</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除错题</el-dropdown-item>
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

    <!-- 题目详情对话框 -->
    <el-dialog
      v-model="showQuestionDialog"
      title="题目详情"
      width="60%"
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Warning, Check, Clock, TrendCharts, Search, Refresh, Download, Delete, ArrowDown
} from '@element-plus/icons-vue'
import QuestionDetail from '@/components/question/QuestionDetail.vue'
import ReviewMode from '@/components/question/ReviewMode.vue'
import { examScoringApi } from '@/api/exam_scoring'
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
    ArrowDown
  },
  setup() {
    const router = useRouter()
    
    // 响应式数据
    const loading = ref(false)
    const wrongAnswers = ref([])
    const subjects = ref([])
    const selectedAnswers = ref([])
    const showQuestionDialog = ref(false)
    const showReviewDialog = ref(false)
    const viewingQuestion = ref(null)
    const reviewingQuestions = ref([])
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      subject_id: '',
      question_type: '',
      is_reviewed: ''
    })
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 统计数据
    const statistics = reactive({
      total_wrong: 0,
      reviewed_count: 0,
      pending_count: 0,
      review_rate: 0
    })
    
    // 计算属性
    const getSubjectName = computed(() => {
      return (subjectId) => {
        const subject = subjects.value.find(s => s.id === subjectId)
        return subject ? subject.name : '未知科目'
      }
    })
    
    // 方法
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
        pagination.total = response.data.total
        
        // 计算统计数据
        calculateStatistics()
      } catch (error) {
        ElMessage.error('加载错题记录失败')
        console.error('Load wrong answers error:', error)
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
    
    const calculateStatistics = () => {
      statistics.total_wrong = wrongAnswers.value.length
      statistics.reviewed_count = wrongAnswers.value.filter(wa => wa.is_reviewed).length
      statistics.pending_count = statistics.total_wrong - statistics.reviewed_count
      statistics.review_rate = statistics.total_wrong > 0 ? 
        Math.round(statistics.reviewed_count / statistics.total_wrong * 100) : 0
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadWrongAnswers()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadWrongAnswers()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadWrongAnswers()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadWrongAnswers()
    }
    
    const handleSelectionChange = (selection) => {
      selectedAnswers.value = selection
    }
    
    const viewQuestion = (wrongAnswer) => {
      viewingQuestion.value = wrongAnswer
      showQuestionDialog.value = true
    }
    
    const reviewQuestion = async (wrongAnswer) => {
      try {
        await examScoringApi.reviewWrongAnswer(wrongAnswer.id)
        ElMessage.success('标记复习成功')
        loadWrongAnswers()
      } catch (error) {
        ElMessage.error('标记复习失败')
        console.error('Review question error:', error)
      }
    }
    
    const handleAction = async (command, wrongAnswer) => {
      switch (command) {
        case 'retake':
          await retakeExam(wrongAnswer)
          break
        case 'favorite':
          await favoriteQuestion(wrongAnswer)
          break
        case 'export':
          await exportQuestion(wrongAnswer)
          break
        case 'delete':
          await deleteQuestion(wrongAnswer)
          break
      }
    }
    
    const retakeExam = async (wrongAnswer) => {
      if (wrongAnswer.exam_id) {
        router.push(`/exam/detail/${wrongAnswer.exam_id}`)
      } else {
        ElMessage.warning('无法找到来源考试')
      }
    }
    
    const favoriteQuestion = async (wrongAnswer) => {
      try {
        // TODO: 实现收藏功能
        ElMessage.success('收藏功能开发中')
      } catch (error) {
        ElMessage.error('收藏失败')
        console.error('Favorite question error:', error)
      }
    }
    
    const exportQuestion = async (wrongAnswer) => {
      try {
        // TODO: 实现导出功能
        ElMessage.success('导出功能开发中')
      } catch (error) {
        ElMessage.error('导出失败')
        console.error('Export question error:', error)
      }
    }
    
    const deleteQuestion = async (wrongAnswer) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除这道错题吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // TODO: 实现删除功能
        ElMessage.success('删除功能开发中')
        loadWrongAnswers()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
          console.error('Delete question error:', error)
        }
      }
    }
    
    const batchReview = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要标记选中的 ${selectedAnswers.value.length} 道错题为已复习吗？`,
          '确认批量标记',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // TODO: 实现批量标记功能
        ElMessage.success('批量标记功能开发中')
        selectedAnswers.value = []
        loadWrongAnswers()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量标记失败')
          console.error('Batch review error:', error)
        }
      }
    }
    
    const batchExport = async () => {
      try {
        // TODO: 实现批量导出功能
        ElMessage.success('批量导出功能开发中')
      } catch (error) {
        ElMessage.error('批量导出失败')
        console.error('Batch export error:', error)
      }
    }
    
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedAnswers.value.length} 道错题吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // TODO: 实现批量删除功能
        ElMessage.success('批量删除功能开发中')
        selectedAnswers.value = []
        loadWrongAnswers()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    const handleReviewComplete = () => {
      showReviewDialog.value = false
      reviewingQuestions.value = []
      loadWrongAnswers()
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
      const subject = subjects.value.find(s => s.id === subjectId)
      return subject && !subject.is_free ? 'warning' : 'primary'
    }
    
    // 生命周期
    onMounted(() => {
      loadSubjects()
      loadWrongAnswers()
    })
    
    return {
      loading,
      wrongAnswers,
      subjects,
      selectedAnswers,
      showQuestionDialog,
      showReviewDialog,
      viewingQuestion,
      reviewingQuestions,
      searchForm,
      pagination,
      statistics,
      getSubjectName,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewQuestion,
      reviewQuestion,
      handleAction,
      batchReview,
      batchExport,
      batchDelete,
      handleReviewComplete,
      getTypeLabel,
      getTypeTagType,
      getSubjectTagType,
      formatDate
    }
  }
}
</script>

<style scoped>
.wrong-answers {
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

.statistics-overview {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  font-size: 32px;
}

.stat-info {
  flex: 1;
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

.search-section {
  margin-bottom: 20px;
}

.wrong-answers-list {
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

.question-title {
  line-height: 1.5;
}

.question-meta {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-answer {
  color: #f56c6c;
  font-weight: 500;
}

.correct-answer {
  color: #67c23a;
  font-weight: 500;
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

/* 响应式设计 */
@media (max-width: 768px) {
  .wrong-answers {
    padding: 15px;
  }
  
  .statistics-overview .el-col {
    margin-bottom: 15px;
  }
  
  .list-header {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
