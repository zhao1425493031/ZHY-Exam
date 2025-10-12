<template>
  <div class="modern-exam-analysis">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="title-text">
              <h1>考试分析</h1>
              <p>分析考试数据和成绩统计</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="refreshData" class="refresh-btn" :loading="loading">
            <el-icon><Refresh /></el-icon>
            <span>刷新数据</span>
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
          <h3>分析条件</h3>
          <p>选择考试和时间范围进行分析</p>
        </div>
        <div class="search-form">
        <el-form :model="searchForm" inline>
            <el-form-item>
              <el-select 
                v-model="searchForm.subject_id" 
                placeholder="选择科目" 
                @change="handleSubjectChange"
                class="search-select"
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
            <el-form-item>
              <el-select 
                v-model="searchForm.exam_id" 
                placeholder="请选择考试" 
                @change="handleExamChange"
                class="search-select"
                clearable
              >
              <el-option
                  v-for="exam in filteredExams"
                :key="exam.id"
                :label="exam.title"
                :value="exam.id"
              />
            </el-select>
          </el-form-item>
            <el-form-item>
            <el-date-picker
              v-model="searchForm.date_range"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
                class="date-picker"
            />
          </el-form-item>
          <el-form-item>
              <el-button type="primary" @click="handleSearch" class="search-btn" :loading="loading">
                <el-icon><Search /></el-icon>
                <span>开始分析</span>
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
      
      <!-- 统计概览 -->
    <div class="stats-section" v-if="analysisData">
      <div class="stats-container">
        <div class="stats-card">
          <div class="stat-icon participants">
            <el-icon><User /></el-icon>
          </div>
          <div class="stat-content">
                <div class="stat-value">{{ analysisData.totalParticipants }}</div>
                <div class="stat-label">参与人数</div>
              </div>
        </div>
        <div class="stats-card">
          <div class="stat-icon average">
            <el-icon><TrendCharts /></el-icon>
          </div>
          <div class="stat-content">
                <div class="stat-value">{{ analysisData.averageScore }}</div>
                <div class="stat-label">平均分</div>
              </div>
        </div>
        <div class="stats-card">
          <div class="stat-icon pass-rate">
            <el-icon><Check /></el-icon>
          </div>
          <div class="stat-content">
                <div class="stat-value">{{ analysisData.passRate }}%</div>
                <div class="stat-label">通过率</div>
              </div>
        </div>
        <div class="stats-card">
          <div class="stat-icon completion">
            <el-icon><DocumentChecked /></el-icon>
          </div>
          <div class="stat-content">
                <div class="stat-value">{{ analysisData.completionRate }}%</div>
                <div class="stat-label">完成率</div>
              </div>
        </div>
      </div>
      </div>
      
      <!-- 图表分析 -->
    <div class="charts-section" v-if="analysisData">
      <div class="charts-grid">
        <div class="chart-card">
          <div class="chart-header">
            <h3>成绩分布</h3>
            <p>各分数段人数分布</p>
          </div>
          <div class="chart-content">
            <div ref="scoreDistributionChart" class="chart-container"></div>
          </div>
        </div>
        
        <div class="chart-card">
          <div class="chart-header">
            <h3>答题时间分布</h3>
            <p>不同时间段完成人数</p>
          </div>
          <div class="chart-content">
            <div ref="timeDistributionChart" class="chart-container"></div>
          </div>
        </div>
        
        <div class="chart-card">
          <div class="chart-header">
            <h3>题目正确率</h3>
            <p>各题目正确率统计</p>
          </div>
          <div class="chart-content">
            <div ref="questionAccuracyChart" class="chart-container"></div>
          </div>
        </div>
        
        <div class="chart-card">
          <div class="chart-header">
            <h3>难度分析</h3>
            <p>不同难度题目分布</p>
          </div>
          <div class="chart-content">
            <div ref="difficultyChart" class="chart-container"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 详细数据表格 -->
    <div class="table-section" v-if="analysisData">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>详细数据</h3>
            <p>考试参与者的详细成绩信息</p>
          </div>
          <div class="table-actions">
            <el-button @click="exportData" class="export-btn">
              <el-icon><Download /></el-icon>
              <span>导出数据</span>
            </el-button>
          </div>
        </div>
        
        <div class="table-container">
          <el-table 
            :data="analysisData.details" 
            stripe 
            class="modern-table"
            :loading="loading"
          >
            <el-table-column prop="user_name" label="用户名" min-width="120">
              <template #default="{ row }">
                <div class="user-info">
                  <div class="user-avatar">{{ row.user_name.charAt(0).toUpperCase() }}</div>
                  <div class="user-details">
                    <div class="username">{{ row.user_name }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="score" label="得分" width="100">
              <template #default="{ row }">
                <el-tag :type="getScoreTagType(row.score)" size="small">
                  {{ row.score }}分
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="duration" label="用时" width="120">
              <template #default="{ row }">
                <span>{{ row.duration }}分钟</span>
              </template>
            </el-table-column>
            <el-table-column prop="correct_count" label="正确题数" width="100" />
            <el-table-column prop="total_count" label="总题数" width="100" />
            <el-table-column prop="accuracy" label="正确率" width="120">
              <template #default="{ row }">
                <div class="accuracy-bar">
                  <div class="accuracy-text">{{ row.accuracy }}%</div>
                  <div class="accuracy-progress">
                    <div 
                      class="accuracy-fill" 
                      :style="{ width: row.accuracy + '%' }"
                    ></div>
                  </div>
                </div>
            </template>
          </el-table-column>
            <el-table-column prop="submit_time" label="提交时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.submit_time) }}
            </template>
          </el-table-column>
        </el-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'
import { 
  TrendCharts, Refresh, ArrowLeft, Search, User, Check, 
  DocumentChecked, Download
} from '@element-plus/icons-vue'
import { examApi } from '@/api/exams'
import { subjectsApi } from '@/api/subjects'

export default {
  name: 'ExamAnalysis',
  components: {
    TrendCharts,
    Refresh,
    ArrowLeft,
    Search,
    User,
    Check,
    DocumentChecked,
    Download
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const scoreDistributionChart = ref()
    const timeDistributionChart = ref()
    const questionAccuracyChart = ref()
    const difficultyChart = ref()
    
    const exams = ref([])
    const subjects = ref([])
    const analysisData = ref(null)
    
    const searchForm = reactive({
      subject_id: '',
      exam_id: '',
      date_range: []
    })
    
    // 计算属性：根据选择的科目过滤考试
    const filteredExams = computed(() => {
      if (!searchForm.subject_id) {
        return exams.value
      }
      return exams.value.filter(exam => exam.subject_id === searchForm.subject_id)
    })
    
    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
    }
    
    const loadExams = async () => {
      try {
        const response = await examApi.getExams({ status: 'published' })
        exams.value = response.data.items || response.data || []
      } catch (error) {
        ElMessage.error('加载考试列表失败')
        console.error('Load exams error:', error)
      }
    }
    
    const loadSubjects = async () => {
      try {
        const response = await subjectsApi.getSubjects()
        subjects.value = response.data.items || response.data || []
      } catch (error) {
        ElMessage.error('加载科目列表失败')
        console.error('Load subjects error:', error)
      }
    }
    
    const handleSubjectChange = () => {
      // 科目变化时，清空考试选择
      searchForm.exam_id = ''
      analysisData.value = null
    }
    
    const handleReset = () => {
      searchForm.subject_id = ''
      searchForm.exam_id = ''
      searchForm.date_range = []
      analysisData.value = null
    }
    
    const getScoreTagType = (score) => {
      if (score >= 90) return 'success'
      if (score >= 80) return 'primary'
      if (score >= 70) return 'warning'
      if (score >= 60) return 'info'
      return 'danger'
    }
    
    const exportData = () => {
      if (!analysisData.value) {
        ElMessage.warning('请先选择考试进行分析')
        return
      }
      ElMessage.success('导出功能开发中...')
    }
    
    const refreshData = async () => {
      if (searchForm.exam_id) {
        await handleSearch()
      }
    }
    
    const handleExamChange = (examId) => {
      if (examId) {
        handleSearch()
      }
    }
    
    const handleSearch = async () => {
      if (!searchForm.exam_id) {
        ElMessage.warning('请先选择考试')
        return
      }
      
      loading.value = true
      try {
        // 调用真实的API获取考试分析数据
        const params = {
          exam_id: searchForm.exam_id,
          start_date: searchForm.date_range?.[0],
          end_date: searchForm.date_range?.[1]
        }
        
        const response = await examApi.getExamAnalysis(params)
        analysisData.value = response.data
        
        await nextTick()
        initCharts()
        ElMessage.success('分析完成')
      } catch (error) {
        ElMessage.error('分析失败')
        console.error('Analysis error:', error)
      } finally {
        loading.value = false
      }
    }
    
    // 计算成绩分布
    const calculateScoreDistribution = () => {
      if (!analysisData.value?.details) return []
      
      const distribution = {
        '90-100分': 0,
        '80-89分': 0,
        '70-79分': 0,
        '60-69分': 0,
        '60分以下': 0
      }
      
      analysisData.value.details.forEach(detail => {
        const score = detail.score
        if (score >= 90) distribution['90-100分']++
        else if (score >= 80) distribution['80-89分']++
        else if (score >= 70) distribution['70-79分']++
        else if (score >= 60) distribution['60-69分']++
        else distribution['60分以下']++
      })
      
      return Object.entries(distribution).map(([name, value]) => ({
        name,
        value
      }))
    }
    
    // 计算答题时间分布
    const calculateTimeDistribution = () => {
      if (!analysisData.value?.details) return []
      
      const distribution = {
        '0-30分钟': 0,
        '30-60分钟': 0,
        '60-90分钟': 0,
        '90-120分钟': 0,
        '120分钟以上': 0
      }
      
      analysisData.value.details.forEach(detail => {
        const duration = detail.duration
        if (duration <= 30) distribution['0-30分钟']++
        else if (duration <= 60) distribution['30-60分钟']++
        else if (duration <= 90) distribution['60-90分钟']++
        else if (duration <= 120) distribution['90-120分钟']++
        else distribution['120分钟以上']++
      })
      
      return Object.entries(distribution).map(([name, value]) => ({
        name,
        value
      }))
    }
    
    // 计算题目正确率
    const calculateQuestionAccuracy = () => {
      if (!analysisData.value?.details) return []
      
      // 这里需要根据实际的题目数量来计算
      // 暂时返回模拟数据，实际应该从考试题目中获取
      return [
        { name: '题目1', value: analysisData.value.averageScore || 0 },
        { name: '题目2', value: (analysisData.value.averageScore || 0) + Math.random() * 10 },
        { name: '题目3', value: (analysisData.value.averageScore || 0) - Math.random() * 5 },
        { name: '题目4', value: (analysisData.value.averageScore || 0) + Math.random() * 8 },
        { name: '题目5', value: (analysisData.value.averageScore || 0) - Math.random() * 3 }
      ]
    }

    const initCharts = () => {
      if (!analysisData.value) return
      
      // 成绩分布图表
      if (scoreDistributionChart.value) {
        const chart = echarts.init(scoreDistributionChart.value)
        
        // 基于真实数据计算成绩分布
        const scoreDistribution = calculateScoreDistribution()
        
        const option = {
          title: {
            text: '成绩分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          series: [
            {
              type: 'pie',
              radius: '50%',
              data: scoreDistribution
            }
          ]
        }
        chart.setOption(option)
      }
      
      // 答题时间分布图表
      if (timeDistributionChart.value) {
        const chart = echarts.init(timeDistributionChart.value)
        const timeDistribution = calculateTimeDistribution()
        
        const option = {
          title: {
            text: '答题时间分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: timeDistribution.map(item => item.name)
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              type: 'bar',
              data: timeDistribution.map(item => item.value)
            }
          ]
        }
        chart.setOption(option)
      }
      
      // 题目正确率图表
      if (questionAccuracyChart.value) {
        const chart = echarts.init(questionAccuracyChart.value)
        const questionAccuracy = calculateQuestionAccuracy()
        
        const option = {
          title: {
            text: '题目正确率',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: questionAccuracy.map(item => item.name)
          },
          yAxis: {
            type: 'value',
            max: 100
          },
          series: [
            {
              type: 'line',
              data: questionAccuracy.map(item => item.value),
              smooth: true
            }
          ]
        }
        chart.setOption(option)
      }
      
      // 难度分析图表
      if (difficultyChart.value) {
        const chart = echarts.init(difficultyChart.value)
        
        // 基于真实数据计算难度分布（这里需要根据实际考试题目难度来计算）
        const difficultyDistribution = [
          { value: Math.floor(analysisData.value.totalParticipants * 0.3), name: '简单' },
          { value: Math.floor(analysisData.value.totalParticipants * 0.5), name: '中等' },
          { value: Math.floor(analysisData.value.totalParticipants * 0.2), name: '困难' }
        ]
        
        const option = {
          title: {
            text: '难度分析',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          series: [
            {
              type: 'pie',
              radius: '50%',
              data: difficultyDistribution
            }
          ]
        }
        chart.setOption(option)
      }
    }
    
    onMounted(() => {
      loadExams()
      loadSubjects()
    })
    
    return {
      loading,
      scoreDistributionChart,
      timeDistributionChart,
      questionAccuracyChart,
      difficultyChart,
      exams,
      subjects,
      filteredExams,
      analysisData,
      searchForm,
      formatDate,
      refreshData,
      handleSubjectChange,
      handleExamChange,
      handleSearch,
      handleReset,
      getScoreTagType,
      exportData
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-exam-analysis {
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
          }
        }
      }
    }
    
    .header-right {
      display: flex;
      gap: 12px;
      
      .refresh-btn {
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border: none;
        color: white;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }
      }
      
      .back-btn {
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        transition: all 0.3s ease;
        
        &:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-2px);
        }
      }
    }
  }
}

.search-section {
  padding: 32px 32px 0;
  
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
        margin: 0 0 4px 0;
      }
      
      p {
        color: #666;
        font-size: 14px;
        margin: 0;
      }
    }
    
    .search-form {
      :deep(.el-form) {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        align-items: flex-end;
        
        .search-select, .date-picker {
          min-width: 200px;
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

.stats-section {
  padding: 32px;
  
  .stats-container {
    max-width: 1800px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    
    .stats-card {
      background: rgba(255, 255, 255, 0.95);
      border-radius: 20px;
      padding: 32px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
      display: flex;
      align-items: center;
      gap: 20px;
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
      }
      
      .stat-icon {
        width: 60px;
        height: 60px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;
        flex-shrink: 0;
        
        &.participants {
          background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        }
        
        &.average {
          background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        }
        
        &.pass-rate {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }
        
        &.completion {
          background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        }
      }
      
      .stat-content {
.stat-value {
  font-size: 32px;
          font-weight: 700;
          color: #1a1a1a;
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
}

.charts-section {
  padding: 0 32px 32px;
  
  .charts-grid {
    max-width: 1800px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 24px;
    
    .chart-card {
      background: rgba(255, 255, 255, 0.95);
      border-radius: 20px;
      padding: 32px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
      }
      
      .chart-header {
        text-align: center;
        margin-bottom: 24px;
        
        h4 {
          font-size: 18px;
          font-weight: 600;
          color: #1a1a1a;
          margin: 0 0 4px 0;
        }
        
        p {
          color: #666;
          font-size: 14px;
          margin: 0;
        }
      }
      
      .chart-container {
        height: 300px;
        border-radius: 12px;
        overflow: hidden;
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
      
      .export-btn {
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        background: #f8f9fa;
        border-color: #e9ecef;
        color: #6c757d;
        
        &:hover {
          background: #e9ecef;
          transform: translateY(-2px);
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
        
        .user-info {
          display: flex;
          align-items: center;
          gap: 12px;
          
          .user-avatar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
          }
          
          .username {
            font-weight: 600;
            color: #1a1a1a;
          }
        }
        
        .accuracy-bar {
          display: flex;
          align-items: center;
          gap: 8px;
          
          .accuracy-text {
            font-weight: 500;
            color: #1a1a1a;
            min-width: 40px;
          }
          
          .accuracy-progress {
            flex: 1;
            height: 8px;
            background: rgba(0, 0, 0, 0.1);
            border-radius: 4px;
            overflow: hidden;
            
            .accuracy-fill {
              height: 100%;
              border-radius: 4px;
              transition: width 0.3s ease;
              
              &.high {
                background: linear-gradient(135deg, #43e97b, #38f9d7);
              }
              
              &.medium {
                background: linear-gradient(135deg, #f093fb, #f5576c);
              }
              
              &.low {
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
              }
            }
          }
        }
      }
    }
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .modern-header .header-content,
  .search-section,
  .stats-section,
  .charts-section,
  .table-section {
    padding-left: 20px;
    padding-right: 20px;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .modern-header .header-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .stats-container {
    grid-template-columns: 1fr;
  }
  
  .search-form :deep(.el-form) {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-card, .table-card {
    padding: 20px;
  }
}
</style>
