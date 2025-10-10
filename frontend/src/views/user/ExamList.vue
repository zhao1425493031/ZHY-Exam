<template>
  <div class="exam-list">
    <div class="page-header">
      <h1>考试列表</h1>
      <div class="header-info">
        <el-tag type="info">共 {{ exams.length }} 场考试</el-tag>
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
              <el-option label="可参加" value="available" />
              <el-option label="进行中" value="ongoing" />
              <el-option label="已结束" value="finished" />
            </el-select>
          </el-form-item>
          <el-form-item label="收费类型">
            <el-select
              v-model="searchForm.is_free"
              placeholder="选择收费类型"
              clearable
              style="width: 120px"
            >
              <el-option label="免费" :value="true" />
              <el-option label="收费" :value="false" />
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

    <!-- 考试列表 -->
    <div class="exam-grid">
      <div
        v-for="exam in exams"
        :key="exam.id"
        class="exam-card"
        :class="{ 'exam-disabled': !canTakeExam(exam) }"
      >
        <div class="card-header">
          <div class="exam-title">
            <h3>{{ exam.title }}</h3>
            <div class="exam-meta">
              <el-tag :type="getStatusTagType(exam)" size="small">
                {{ getStatusLabel(exam) }}
              </el-tag>
              <el-tag :type="getSubjectTagType(exam)" size="small">
                {{ getSubjectName(exam.subject_id) }}
              </el-tag>
            </div>
          </div>
          <div class="exam-price" v-if="!isFreeExam(exam)">
            <div class="price-current">¥{{ getExamPrice(exam) }}</div>
            <div v-if="getOriginalPrice(exam) > getExamPrice(exam)" class="price-original">
              ¥{{ getOriginalPrice(exam) }}
            </div>
          </div>
        </div>

        <div class="card-content">
          <div v-if="exam.description" class="exam-description">
            <p>{{ exam.description }}</p>
          </div>

          <div class="exam-info">
            <div class="info-item">
              <el-icon><QuestionFilled /></el-icon>
              <span>{{ exam.question_count }}题</span>
            </div>
            <div class="info-item">
              <el-icon><Medal /></el-icon>
              <span>{{ exam.total_points }}分</span>
            </div>
            <div class="info-item">
              <el-icon><Timer /></el-icon>
              <span>{{ formatDuration(exam.duration) }}</span>
            </div>
          </div>

          <div v-if="exam.start_time || exam.end_time" class="exam-time">
            <div v-if="exam.start_time" class="time-item">
              <span class="time-label">开始时间：</span>
              <span class="time-value">{{ formatDate(exam.start_time) }}</span>
            </div>
            <div v-if="exam.end_time" class="time-item">
              <span class="time-label">结束时间：</span>
              <span class="time-value">{{ formatDate(exam.end_time) }}</span>
            </div>
          </div>

          <div v-if="!isFreeExam(exam)" class="exam-purchase">
            <div class="purchase-info">
              <span class="purchase-label">需要购买</span>
              <span class="purchase-price">¥{{ getExamPrice(exam) }}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <div class="exam-actions">
            <el-button
              v-if="canTakeExam(exam)"
              type="primary"
              @click="startExam(exam)"
              :loading="startingExam === exam.id"
            >
              <el-icon><PlayArrow /></el-icon>
              开始考试
            </el-button>
            <el-button
              v-else-if="!isFreeExam(exam) && !hasPurchased(exam)"
              type="warning"
              @click="purchaseExam(exam)"
            >
              <el-icon><ShoppingCart /></el-icon>
              购买考试
            </el-button>
            <el-button
              v-else-if="hasTakenExam(exam)"
              type="success"
              @click="viewResult(exam)"
            >
              <el-icon><View /></el-icon>
              查看结果
            </el-button>
            <el-button
              v-else
              disabled
            >
              {{ getDisabledReason(exam) }}
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        :current-page="pagination.page"
        :page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="[12, 24, 48]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 购买考试对话框 -->
    <el-dialog
      v-model="showPurchaseDialog"
      title="购买考试"
      width="50%"
    >
      <ExamPurchase
        v-if="showPurchaseDialog && purchasingExam"
        :exam="purchasingExam"
        @success="handlePurchaseSuccess"
        @cancel="showPurchaseDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Refresh, QuestionFilled, Medal, Timer, PlayArrow, ShoppingCart, View } from '@element-plus/icons-vue'
import ExamPurchase from '@/components/exam/ExamPurchase.vue'
import { examApi } from '@/api/exams'
import { subjectApi } from '@/api/subjects'
import { formatDate, formatDuration } from '@/utils/format'

export default {
  name: 'ExamList',
  components: {
    ExamPurchase,
    Search,
    Refresh,
    QuestionFilled,
    Medal,
    Timer,
    PlayArrow,
    ShoppingCart,
    View
  },
  setup() {
    const router = useRouter()
    
    // 响应式数据
    const loading = ref(false)
    const exams = ref([])
    const subjects = ref([])
    const startingExam = ref(null)
    const showPurchaseDialog = ref(false)
    const purchasingExam = ref(null)
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      subject_id: '',
      status: '',
      is_free: ''
    })
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 12,
      total: 0
    })
    
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
          status: 'published',
          ...searchForm
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
    
    const canTakeExam = (exam) => {
      // 检查考试是否可参加
      if (exam.status !== 'published') return false
      
      // 检查时间
      const now = new Date()
      if (exam.start_time && new Date(exam.start_time) > now) return false
      if (exam.end_time && new Date(exam.end_time) < now) return false
      
      // 检查是否已购买（收费考试）
      if (!isFreeExam(exam) && !hasPurchased(exam)) return false
      
      // 检查是否已参加过
      if (hasTakenExam(exam)) return false
      
      return true
    }
    
    const isFreeExam = (exam) => {
      const subject = subjects.value.find(s => s.id === exam.subject_id)
      return subject ? subject.is_free : true
    }
    
    const hasPurchased = (exam) => {
      // TODO: 检查用户是否已购买此考试
      return false
    }
    
    const hasTakenExam = (exam) => {
      // TODO: 检查用户是否已参加过此考试
      return false
    }
    
    const getExamPrice = (exam) => {
      const subject = subjects.value.find(s => s.id === exam.subject_id)
      return subject ? subject.price : 0
    }
    
    const getOriginalPrice = (exam) => {
      const subject = subjects.value.find(s => s.id === exam.subject_id)
      return subject ? subject.original_price : 0
    }
    
    const getDisabledReason = (exam) => {
      if (exam.status !== 'published') return '考试未发布'
      if (exam.start_time && new Date(exam.start_time) > new Date()) return '考试未开始'
      if (exam.end_time && new Date(exam.end_time) < new Date()) return '考试已结束'
      if (!isFreeExam(exam) && !hasPurchased(exam)) return '需要购买'
      if (hasTakenExam(exam)) return '已参加'
      return '不可参加'
    }
    
    const startExam = async (exam) => {
      try {
        startingExam.value = exam.id
        
        // 检查考试可用性
        const response = await examApi.checkExamAvailability(exam.id)
        if (!response.data.available) {
          ElMessage.error(response.data.message)
          return
        }
        
        // 跳转到考试页面
        router.push(`/user/exam-taking/${exam.id}`)
      } catch (error) {
        ElMessage.error('开始考试失败')
        console.error('Start exam error:', error)
      } finally {
        startingExam.value = null
      }
    }
    
    const purchaseExam = (exam) => {
      purchasingExam.value = exam
      showPurchaseDialog.value = true
    }
    
    const viewResult = (exam) => {
      router.push(`/user/exam-result/${exam.id}`)
    }
    
    const handlePurchaseSuccess = () => {
      showPurchaseDialog.value = false
      purchasingExam.value = null
      loadExams()
    }
    
    // 工具方法
    const getStatusLabel = (exam) => {
      const now = new Date()
      if (exam.status !== 'published') return '未发布'
      if (exam.start_time && new Date(exam.start_time) > now) return '未开始'
      if (exam.end_time && new Date(exam.end_time) < now) return '已结束'
      return '进行中'
    }
    
    const getStatusTagType = (exam) => {
      const now = new Date()
      if (exam.status !== 'published') return 'info'
      if (exam.start_time && new Date(exam.start_time) > now) return 'warning'
      if (exam.end_time && new Date(exam.end_time) < now) return 'danger'
      return 'success'
    }
    
    const getSubjectTagType = (exam) => {
      const subject = subjects.value.find(s => s.id === exam.subject_id)
      return subject && !subject.is_free ? 'warning' : 'primary'
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
      startingExam,
      showPurchaseDialog,
      purchasingExam,
      searchForm,
      pagination,
      getSubjectName,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      canTakeExam,
      isFreeExam,
      hasPurchased,
      hasTakenExam,
      getExamPrice,
      getOriginalPrice,
      getDisabledReason,
      startExam,
      purchaseExam,
      viewResult,
      handlePurchaseSuccess,
      getStatusLabel,
      getStatusTagType,
      getSubjectTagType,
      formatDate,
      formatDuration
    }
  }
}
</script>

<style scoped>
.exam-list {
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

.search-section {
  margin-bottom: 20px;
}

.exam-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.exam-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background-color: #fff;
  transition: all 0.3s;
  overflow: hidden;
}

.exam-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.exam-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.exam-disabled:hover {
  transform: none;
  box-shadow: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 20px 0 20px;
}

.exam-title h3 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 18px;
  font-weight: 600;
  line-height: 1.4;
}

.exam-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.exam-price {
  text-align: right;
}

.price-current {
  font-size: 20px;
  font-weight: 600;
  color: #e6a23c;
}

.price-original {
  font-size: 14px;
  color: #909399;
  text-decoration: line-through;
  margin-top: 2px;
}

.card-content {
  padding: 20px;
}

.exam-description {
  margin-bottom: 15px;
}

.exam-description p {
  margin: 0;
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.exam-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #606266;
  font-size: 14px;
}

.exam-time {
  margin-bottom: 15px;
}

.time-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 14px;
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

.exam-purchase {
  padding: 10px;
  background-color: #fef0e6;
  border-radius: 6px;
  border-left: 4px solid #e6a23c;
}

.purchase-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.purchase-label {
  color: #e6a23c;
  font-weight: 500;
}

.purchase-price {
  color: #e6a23c;
  font-weight: 600;
  font-size: 16px;
}

.card-footer {
  padding: 0 20px 20px 20px;
}

.exam-actions {
  display: flex;
  justify-content: center;
}

.pagination {
  display: flex;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .exam-grid {
    grid-template-columns: 1fr;
  }
  
  .exam-info {
    flex-direction: column;
    gap: 8px;
  }
  
  .info-item {
    justify-content: center;
  }
}
</style>
