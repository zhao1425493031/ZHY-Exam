<template>
  <div class="modern-my-records">
    <!-- 顶部导航栏 -->
    <TopNavigation />
    
    <!-- 页面内容 -->
    <div class="page-content">
      <div class="content-container">
        <!-- 页面标题 -->
        <div class="modern-header">
          <div class="page-title">
            <el-icon class="title-icon"><Notebook /></el-icon>
            <h1 class="title-text">我的考试记录</h1>
          </div>
          <div class="header-right">
            <el-button type="info" @click="goToDashboard">
              <el-icon><ArrowLeft /></el-icon>
              返回个人中心
            </el-button>
          </div>
        </div>

        <!-- 统计概览 -->
        <div class="statistics-section">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="6">
              <div class="stat-card">
                <div class="stat-icon-wrapper blue">
                  <el-icon class="stat-icon"><Document /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ statistics.total_exams }}</div>
                  <div class="stat-label">总考试次数</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <div class="stat-card">
                <div class="stat-icon-wrapper green">
                  <el-icon class="stat-icon"><Trophy /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ statistics.average_score }}</div>
                  <div class="stat-label">平均分数</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <div class="stat-card">
                <div class="stat-icon-wrapper orange">
                  <el-icon class="stat-icon"><Medal /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ statistics.pass_rate }}%</div>
                  <div class="stat-label">及格率</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <div class="stat-card">
                <div class="stat-icon-wrapper red">
                  <el-icon class="stat-icon"><Warning /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ statistics.wrong_answers }}</div>
                  <div class="stat-label">错题数量</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 搜索筛选区域 -->
        <div class="search-section">
          <div class="search-card">
            <div class="search-header">
              <el-icon><Search /></el-icon>
              <span>筛选条件</span>
            </div>
            <el-form :model="searchForm" class="search-form">
              <el-row :gutter="20">
                <el-col :xs="24" :sm="12" :md="6">
                  <el-form-item>
                    <el-input
                      v-model="searchForm.keyword"
                      placeholder="搜索考试标题"
                      class="search-input"
                      clearable
                      @keyup.enter="handleSearch"
                    >
                      <template #prefix>
                        <el-icon><Search /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="12" :md="6">
                  <el-form-item>
                    <el-select
                      v-model="searchForm.subject_id"
                      placeholder="选择科目"
                      class="filter-select"
                      clearable
                    >
                      <el-option
                        v-for="subject in subjects"
                        :key="subject.id"
                        :label="subject.name"
                        :value="subject.id"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="12" :md="6">
                  <el-form-item>
                    <el-select
                      v-model="searchForm.status"
                      placeholder="选择状态"
                      class="filter-select"
                      clearable
                    >
                      <el-option label="已完成" value="submitted" />
                      <el-option label="进行中" value="in_progress" />
                      <el-option label="已超时" value="timeout" />
                      <el-option label="已取消" value="cancelled" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="12" :md="6">
                  <el-form-item>
                    <el-button type="primary" class="search-btn" @click="handleSearch">
                      <el-icon><Search /></el-icon>
                      搜索
                    </el-button>
                    <el-button class="reset-btn" @click="handleReset">
                      <el-icon><Refresh /></el-icon>
                      重置
                    </el-button>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </div>
        </div>

        <!-- 表格区域 -->
        <div class="table-section">
          <div class="table-card">
            <div class="table-header">
              <div class="table-title">
                <el-icon><List /></el-icon>
                <span>考试记录列表</span>
                <el-tag v-if="pagination.total > 0" type="info" size="small">
                  共 {{ pagination.total }} 条记录
                </el-tag>
              </div>
              <div class="table-actions" v-if="selectedRecords.length > 0">
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
            
            <div class="table-container">
              <el-table
                :data="records"
                v-loading="loading"
                @selection-change="handleSelectionChange"
                stripe
                style="width: 100%"
              >
                <el-table-column type="selection" width="55" />
                
                <el-table-column label="考试标题" min-width="250">
                  <template #default="{ row }">
                    <div class="exam-title-cell">
                      <div class="exam-name">{{ row.exam_title || '未知考试' }}</div>
                      <div class="exam-subject">
                        <el-tag size="small" type="info">{{ row.subject_name || '未知科目' }}</el-tag>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                
                <el-table-column label="分数" width="120" align="center">
                  <template #default="{ row }">
                    <el-tag :type="getScoreType(row.score)" size="large">
                      {{ row.score !== null ? row.score : '--' }} 分
                    </el-tag>
                  </template>
                </el-table-column>
                
                <el-table-column label="状态" width="120" align="center">
                  <template #default="{ row }">
                    <el-tag :type="getStatusType(row.status)" size="small">
                      {{ getStatusText(row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
                
                <el-table-column label="开始时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.start_time) }}
                  </template>
                </el-table-column>
                
                <el-table-column label="提交时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.submit_time) }}
                  </template>
                </el-table-column>
                
                <el-table-column label="用时" width="120" align="center">
                  <template #default="{ row }">
                    {{ calculateDuration(row) }}
                  </template>
                </el-table-column>
                
                <el-table-column label="操作" width="280" fixed="right">
                  <template #default="{ row }">
                    <div class="action-buttons">
                      <el-button 
                        size="small" 
                        type="primary" 
                        @click="viewResult(row)"
                        v-if="row.status === 'submitted'"
                      >
                        <el-icon><View /></el-icon>
                        查看结果
                      </el-button>
                      <el-button 
                        size="small" 
                        type="success" 
                        @click="retakeExam(row)"
                      >
                        <el-icon><Refresh /></el-icon>
                        重新考试
                      </el-button>
                      <el-button 
                        size="small" 
                        type="danger" 
                        @click="deleteRecord(row)"
                      >
                        <el-icon><Delete /></el-icon>
                        删除
                      </el-button>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <!-- 分页 -->
            <div class="pagination-section">
              <el-pagination
                v-model:current-page="pagination.page"
                v-model:page-size="pagination.size"
                :page-sizes="[10, 20, 50, 100]"
                :total="pagination.total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handlePageChange"
                class="modern-pagination"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document,
  Trophy,
  Medal,
  Warning,
  Search,
  Refresh,
  List,
  Download,
  Delete,
  View,
  Notebook,
  ArrowLeft
} from '@element-plus/icons-vue'
import TopNavigation from '@/components/layout/TopNavigation.vue'
import { examRecordsApi } from '@/api/exam_records'
import { subjectsApi } from '@/api/subjects'
import { examScoringApi } from '@/api/exam_scoring'
import dayjs from 'dayjs'

export default {
  name: 'MyRecords',
  components: {
    TopNavigation,
    Document,
    Trophy,
    Medal,
    Warning,
    Search,
    Refresh,
    List,
    Download,
    Delete,
    View,
    Notebook,
    ArrowLeft
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const records = ref([])
    const subjects = ref([])
    const selectedRecords = ref([])

    const searchForm = reactive({
      keyword: '',
      subject_id: null,
      status: null,
      date_range: null
    })

    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })

    const statistics = reactive({
      total_exams: 0,
      average_score: 0,
      pass_rate: 0,
      wrong_answers: 0
    })

    // 加载考试记录
    const loadRecords = async () => {
      try {
        loading.value = true
        
        const params = {
          page: pagination.page,
          size: pagination.size,
          keyword: searchForm.keyword || undefined,
          subject_id: searchForm.subject_id || undefined,
          status: searchForm.status || undefined
        }

        const response = await examRecordsApi.getMyRecords(params)
        
        if (response.code === 200) {
          records.value = response.data.items || []
          pagination.total = response.data.total || 0
          
          // 计算统计数据
          calculateStatistics()
        } else {
          ElMessage.error(response.message || '加载记录失败')
        }
      } catch (error) {
        console.error('加载记录失败:', error)
        ElMessage.error('加载记录失败')
      } finally {
        loading.value = false
      }
    }

    // 加载科目列表
    const loadSubjects = async () => {
      try {
        const response = await subjectsApi.getSubjects({ status: 'active' })
        if (response.code === 200) {
          subjects.value = response.data.items || []
        }
      } catch (error) {
        console.error('加载科目失败:', error)
      }
    }

    // 计算统计数据
    const calculateStatistics = () => {
      if (!records.value || records.value.length === 0) {
        statistics.total_exams = 0
        statistics.average_score = 0
        statistics.pass_rate = 0
        statistics.wrong_answers = 0
        return
      }

      const submittedRecords = records.value.filter(r => r.status === 'submitted' && r.score !== null)
      
      statistics.total_exams = records.value.length
      
      if (submittedRecords.length > 0) {
        const totalScore = submittedRecords.reduce((sum, r) => sum + (r.score || 0), 0)
        statistics.average_score = Math.round(totalScore / submittedRecords.length)
        
        const passedCount = submittedRecords.filter(r => r.score >= 60).length
        statistics.pass_rate = Math.round((passedCount / submittedRecords.length) * 100)
      } else {
        statistics.average_score = 0
        statistics.pass_rate = 0
      }
      
      // 获取错题数量
      fetchWrongAnswersCount()
    }

    // 获取错题数量
    const fetchWrongAnswersCount = async () => {
      try {
        const response = await examScoringApi.getWrongAnswers({
          page: 1,
          size: 1000 // 获取所有错题用于统计
        })
        statistics.wrong_answers = response.data.total || 0
        console.log('错题统计:', statistics.wrong_answers)
      } catch (error) {
        console.warn('获取错题数量失败:', error)
        statistics.wrong_answers = 0
      }
    }

    // 格式化日期
    const formatDate = (date) => {
      if (!date) return '--'
      return dayjs(date).format('YYYY-MM-DD HH:mm')
    }

    // 计算用时
    const calculateDuration = (record) => {
      if (!record.start_time || !record.submit_time) return '--'
      
      const start = dayjs(record.start_time)
      const end = dayjs(record.submit_time)
      const minutes = end.diff(start, 'minute')
      
      if (minutes < 60) {
        return `${minutes}分钟`
      } else {
        const hours = Math.floor(minutes / 60)
        const mins = minutes % 60
        return `${hours}小时${mins}分钟`
      }
    }

    // 获取分数类型
    const getScoreType = (score) => {
      if (score === null || score === undefined) return 'info'
      if (score >= 90) return 'success'
      if (score >= 60) return 'warning'
      return 'danger'
    }

    // 获取状态类型
    const getStatusType = (status) => {
      const typeMap = {
        'submitted': 'success',
        'in_progress': 'primary',
        'timeout': 'warning',
        'cancelled': 'info'
      }
      return typeMap[status] || 'info'
    }

    // 获取状态文本
    const getStatusText = (status) => {
      const textMap = {
        'submitted': '已完成',
        'in_progress': '进行中',
        'timeout': '已超时',
        'cancelled': '已取消'
      }
      return textMap[status] || '未知'
    }

    // 搜索
    const handleSearch = () => {
      pagination.page = 1
      loadRecords()
    }

    // 重置
    const handleReset = () => {
      searchForm.keyword = ''
      searchForm.subject_id = null
      searchForm.status = null
      searchForm.date_range = null
      pagination.page = 1
      loadRecords()
    }

    // 选择变化
    const handleSelectionChange = (selection) => {
      selectedRecords.value = selection
    }

    // 查看结果
    const viewResult = (record) => {
      router.push(`/user/exam-result/${record.id}`)
    }

    // 重新考试
    const retakeExam = async (record) => {
      try {
        await ElMessageBox.confirm(
          '确定要重新参加该考试吗？',
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        router.push(`/exam/detail/${record.exam_id}`)
      } catch (error) {
        // 用户取消
      }
    }

    // 删除记录
    const deleteRecord = async (record) => {
      try {
        await ElMessageBox.confirm(
          '确定要删除该考试记录吗？删除后无法恢复。',
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const response = await examRecordsApi.deleteRecord(record.id)
        if (response.code === 200) {
          ElMessage.success('删除成功')
          loadRecords()
        } else {
          ElMessage.error(response.message || '删除失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除记录失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }

    // 批量导出
    const batchExport = () => {
      ElMessage.info('批量导出功能开发中')
    }

    // 批量删除
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedRecords.value.length} 条记录吗？删除后无法恢复。`,
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const ids = selectedRecords.value.map(r => r.id)
        const response = await examRecordsApi.batchDelete(ids)
        
        if (response.code === 200) {
          ElMessage.success('批量删除成功')
          selectedRecords.value = []
          loadRecords()
        } else {
          ElMessage.error(response.message || '批量删除失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('批量删除失败:', error)
          ElMessage.error('批量删除失败')
        }
      }
    }

    // 分页处理
    const handlePageChange = (page) => {
      pagination.page = page
      loadRecords()
    }

    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadRecords()
    }

    // 返回个人中心
    const goToDashboard = () => {
      router.push('/user/dashboard')
    }

    onMounted(() => {
      loadRecords()
      loadSubjects()
    })

    return {
      loading,
      records,
      subjects,
      selectedRecords,
      searchForm,
      pagination,
      statistics,
      formatDate,
      calculateDuration,
      getScoreType,
      getStatusType,
      getStatusText,
      handleSearch,
      handleReset,
      handleSelectionChange,
      viewResult,
      retakeExam,
      deleteRecord,
      batchExport,
      batchDelete,
      handlePageChange,
      handleSizeChange,
      goToDashboard,
      fetchWrongAnswersCount
    }
  }
}
</script>

<style scoped>
.modern-my-records {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.page-content {
  padding-top: 80px;
}

.content-container {
  max-width: 1800px;
  margin: 0 auto;
  padding: 2rem;
}

/* 页面标题 */
.modern-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.page-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.title-icon {
  font-size: 2rem;
  color: #667eea;
}

.title-text {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-right {
  display: flex;
  gap: 1rem;
}

/* 统计卡片 */
.statistics-section {
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  margin-bottom: 1rem;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.stat-icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.stat-icon-wrapper.blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon-wrapper.green {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-icon-wrapper.orange {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-icon-wrapper.red {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #7f8c8d;
}

/* 搜索区域 */
.search-section {
  margin-bottom: 2rem;
}

.search-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.search-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.search-form {
  margin: 0;
}

.search-form .el-form-item {
  margin-bottom: 0;
}

.search-input,
.filter-select {
  width: 100%;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.search-input :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.filter-select :deep(.el-input__wrapper) {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.search-btn,
.reset-btn {
  border-radius: 12px;
  padding: 0.6rem 1.5rem;
  font-weight: 600;
}

.search-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

/* 表格区域 */
.table-section {
  margin-bottom: 2rem;
}

.table-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.table-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.table-actions {
  display: flex;
  gap: 0.5rem;
}

.table-container {
  border-radius: 12px;
  overflow: hidden;
}

.table-container :deep(.el-table) {
  border-radius: 12px;
}

.table-container :deep(.el-table th) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  border: none;
}

.table-container :deep(.el-table td) {
  border-bottom: 1px solid #f0f0f0;
}

.table-container :deep(.el-table__body tr:hover) {
  background-color: rgba(102, 126, 234, 0.08);
}

.table-container :deep(.el-table__body tr) {
  transition: all 0.3s ease;
}

.table-container :deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
  border: none;
}

.exam-title-cell {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.exam-name {
  font-weight: 600;
  color: #2c3e50;
}

.exam-subject {
  font-size: 0.85rem;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: left;
}

.action-buttons .el-button {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.action-buttons .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 分页 */
.pagination-section {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

.modern-pagination {
  background: rgba(255, 255, 255, 0.5);
  padding: 1rem;
  border-radius: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-container {
    padding: 1rem;
  }

  .modern-header {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .page-title {
    flex-direction: column;
    text-align: center;
  }

  .title-text {
    font-size: 1.5rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .search-card {
    padding: 1rem;
  }

  .table-card {
    padding: 1rem;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>
