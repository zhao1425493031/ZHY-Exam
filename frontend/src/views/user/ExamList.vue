<template>
  <div class="modern-exam-list">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="title-text">
              <h1>考试列表</h1>
              <p>选择并参加您感兴趣的考试</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button @click="goToDashboard" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回个人中心</span>
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
              />
            </el-form-item>
            <el-form-item>
              <el-select
                v-model="searchForm.subject_id"
                placeholder="选择科目"
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
                class="filter-select"
              >
                <el-option label="全部状态" value="" />
                <el-option label="可参加" value="available" />
                <el-option label="进行中" value="ongoing" />
                <el-option label="已结束" value="finished" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-select
                v-model="searchForm.is_free"
                placeholder="选择收费类型"
                class="filter-select"
              >
                <el-option label="全部类型" value="" />
                <el-option label="免费" :value="true" />
                <el-option label="收费" :value="false" />
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
        </div>
        
        <div class="table-container">
          <el-table 
            :data="exams" 
            stripe 
            class="modern-table"
            :loading="loading"
          >
            <el-table-column label="考试标题" prop="title" min-width="200">
              <template #default="{ row }">
                <div class="exam-title-cell">
                  <h4>{{ row.title }}</h4>
                  <div class="exam-meta">
                    <el-tag :type="getStatusTagType(row)" size="small">
                      {{ getStatusLabel(row) }}
                    </el-tag>
                    <el-tag :type="getSubjectTagType(row)" size="small">
                      {{ getSubjectName(row.subject_id) }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="科目" width="300">
              <template #default="{ row }">
                <span>{{ getSubjectName(row.subject_id) }}</span>
              </template>
            </el-table-column>
            
            <el-table-column label="题目数" width="120">
              <template #default="{ row }">
                <span>{{ row.question_count }}题</span>
              </template>
            </el-table-column>
            
            <el-table-column label="总分" width="120">
              <template #default="{ row }">
                <span>{{ row.total_points }}分</span>
              </template>
            </el-table-column>
            
            <el-table-column label="时长" width="120">
              <template #default="{ row }">
                <span>{{ formatDuration(row.duration) }}</span>
              </template>
            </el-table-column>
            
            <el-table-column label="状态" width="150">
              <template #default="{ row }">
                <el-tag :type="getStatusTagType(row)" size="small">
                  {{ getStatusLabel(row) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column label="价格" width="150">
              <template #default="{ row }">
                <div v-if="!isFreeExam(row)" class="price-cell">
                  <div class="price-current">¥{{ getExamPrice(row) }}</div>
                  <div v-if="getOriginalPrice(row) > getExamPrice(row)" class="price-original">
                    ¥{{ getOriginalPrice(row) }}
                  </div>
                </div>
                <span v-else class="free-tag">免费</span>
              </template>
            </el-table-column>
            
            <el-table-column label="操作" width="140" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button
                    v-if="canTakeExam(row)"
                    type="primary"
                    size="small"
                    @click="startExam(row)"
                    :loading="startingExam === row.id"
                  >
                    开始考试
                  </el-button>
                  <el-button
                    v-else-if="!isFreeExam(row) && !hasPurchased(row)"
                    type="warning"
                    size="small"
                    @click="purchaseExam(row)"
                  >
                    购买考试
                  </el-button>
                  <el-button
                    v-else-if="hasTakenExam(row)"
                    type="success"
                    size="small"
                    @click="viewResult(row)"
                  >
                    查看结果
                  </el-button>
                  <el-button
                    v-else
                    size="small"
                    disabled
                  >
                    {{ getDisabledReason(row) }}
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination-section">
      <el-pagination
        :current-page="pagination.page"
        :page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="[12, 24, 48]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
        class="modern-pagination"
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
import { Search, Refresh, Document, ArrowLeft } from '@element-plus/icons-vue'
import ExamPurchase from '@/components/exam/ExamPurchase.vue'
import { examApi } from '@/api/exams'
import { subjectsApi } from '@/api/subjects'
import { formatDate, formatDuration } from '@/utils/format'

export default {
  name: 'ExamList',
  components: {
    ExamPurchase,
    Search,
    Refresh,
    Document,
    ArrowLeft
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
      // 检查用户是否已参加过此考试
      // 这里可以调用API获取用户的考试记录，但为了性能考虑，
      // 我们依赖后端的checkExamAvailability API来检查
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
        
        // 检查是否可以参加考试
        if (!response.data.can_take) {
          ElMessage.error(response.data.message || '无法参加该考试')
          return
        }
        
        // 如果有提示信息（比如已参加次数），显示提示但不阻止继续
        if (response.data.message && response.data.can_take) {
          ElMessage.info(response.data.message)
        }
        
        // 跳转到考试详情页面
        router.push(`/exam/detail/${exam.id}`)
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
    
    const goToDashboard = () => {
      router.push('/user/dashboard')
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
      formatDuration,
      goToDashboard
    }
  }
}
</script>

<style scoped>
.modern-exam-list {
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
}

.header-content {
  max-width: 1800px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left .page-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

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

.title-text h1 {
  color: white;
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 4px 0;
  letter-spacing: -0.5px;
}

.title-text p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin: 0;
  font-weight: 500;
}

.header-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.back-btn {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  font-weight: 600;
  padding: 12px 20px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.search-section {
  padding: 32px 32px 0 32px;
  max-width: 1800px;
  margin: 0 auto;
}

.search-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.search-header {
  margin-bottom: 20px;
}

.search-header h3 {
  color: #2c3e50;
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.search-header p {
  color: #6c757d;
  font-size: 14px;
  margin: 0;
  font-weight: 500;
}

.search-form .el-form-item {
  margin-bottom: 0;
  margin-right: 16px;
}

.search-input,
.filter-select {
  width: 200px;
}

.search-btn,
.reset-btn {
  border-radius: 10px;
  font-weight: 600;
  padding: 12px 20px;
  border: none;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.reset-btn {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
  border: 1px solid rgba(108, 117, 125, 0.2);
}

.reset-btn:hover {
  background: #6c757d;
  color: white;
  transform: translateY(-2px);
}

.table-section {
  padding: 32px;
  max-width: 1800px;
  margin: 0 auto;
}

.table-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title h3 {
  color: #2c3e50;
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.table-title p {
  color: #6c757d;
  font-size: 14px;
  margin: 0;
  font-weight: 500;
}

.table-container {
  border-radius: 12px;
  overflow: hidden;
}

.modern-table {
  --el-table-bg-color: transparent;
  --el-table-header-bg-color: #f8f9fa;
  --el-table-row-hover-bg-color: rgba(102, 126, 234, 0.05);
  --el-table-border-color: #e9ecef;
}

.exam-title-cell h4 {
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.exam-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.price-cell {
  text-align: center;
}

.price-current {
  font-size: 16px;
  font-weight: 700;
  color: #e6a23c;
}

.price-original {
  font-size: 12px;
  color: #909399;
  text-decoration: line-through;
}

.free-tag {
  color: #67c23a;
  font-weight: 600;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: left;
}

.pagination-section {
  padding: 0 32px 32px 32px;
  max-width: 1800px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
}

.modern-pagination {
  --el-pagination-bg-color: rgba(255, 255, 255, 0.95);
  --el-pagination-button-bg-color: transparent;
  --el-pagination-button-disabled-bg-color: transparent;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 12px 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .header-content,
  .search-section,
  .table-section,
  .pagination-section {
    max-width: 100%;
    padding-left: 16px;
    padding-right: 16px;
  }
}

@media (max-width: 768px) {
  .modern-header {
    padding: 16px 0;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .header-right {
    align-self: flex-end;
  }
  
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-form .el-form-item {
    margin-right: 0;
    margin-bottom: 16px;
  }
  
  .search-input,
  .filter-select {
    width: 100%;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .modern-table {
    min-width: 800px;
  }
}

@media (max-width: 480px) {
  .search-section,
  .table-section,
  .pagination-section {
    padding-left: 12px;
    padding-right: 12px;
  }
  
  .search-card,
  .table-card {
    padding: 16px;
  }
}
</style>
