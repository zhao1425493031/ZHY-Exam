<template>
  <div class="user-dashboard">
    <!-- 顶部导航栏 -->
    <TopNavigation />

    <!-- 主要内容区域 -->
    <div class="dashboard-content">
      <div class="container">
        <!-- 面包屑导航 -->
        <el-breadcrumb separator="/" class="breadcrumb">
          <el-breadcrumb-item>
            <router-link to="/">首页</router-link>
          </el-breadcrumb-item>
          <el-breadcrumb-item>个人中心</el-breadcrumb-item>
          <el-breadcrumb-item>我的仪表盘</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 页面标题 -->
        <div class="page-header">
          <h1>我的仪表盘</h1>
          <p>欢迎回来，{{ authStore.user?.username }}！</p>
        </div>

        <!-- 统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon size="32"><Document /></el-icon>
            </div>
            <div class="stat-content">
              <h3>{{ stats.totalExams }}</h3>
              <p>已参加考试</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon size="32"><Star /></el-icon>
            </div>
            <div class="stat-content">
              <h3>{{ stats.averageScore }}</h3>
              <p>平均成绩</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon size="32"><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <h3>{{ stats.studyHours }}</h3>
              <p>学习时长(小时)</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon size="32"><TrendCharts /></el-icon>
            </div>
            <div class="stat-content">
              <h3>{{ stats.rank }}</h3>
              <p>学习排名</p>
            </div>
          </div>
        </div>

        <!-- 主要内容区域 -->
        <div class="main-content">
          <!-- 最近考试 -->
          <div class="content-section">
            <div class="section-header">
              <h2>最近考试</h2>
              <el-button type="primary" @click="goToRecords">查看全部</el-button>
            </div>
            <div class="exam-list" v-loading="examsLoading">
              <div v-if="recentExams.length === 0" class="empty-state">
                <el-icon size="64"><Document /></el-icon>
                <p>暂无考试记录</p>
                <el-button type="primary" @click="goToCourses">开始学习</el-button>
              </div>
              <div v-else>
                <div 
                  v-for="exam in recentExams" 
                  :key="exam.id"
                  class="exam-item"
                  @click="viewExamDetail(exam)"
                >
                  <div class="exam-info">
                    <h4>{{ exam.title }}</h4>
                    <p>{{ exam.subject_name }}</p>
                    <div class="exam-meta">
                      <span class="exam-date">{{ formatDate(exam.submit_time) }}</span>
                      <span class="exam-score" :class="getScoreClass(exam.score)">
                        {{ exam.score }}分
                      </span>
                    </div>
                  </div>
                  <div class="exam-status">
                    <el-tag :type="getStatusType(exam.status)">
                      {{ getStatusText(exam.status) }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 学习进度 -->
          <div class="content-section">
            <div class="section-header">
              <h2>学习进度</h2>
              <el-button type="primary" @click="goToProgress">查看详情</el-button>
            </div>
            <div class="progress-list" v-loading="progressLoading">
              <div v-if="learningProgress.length === 0" class="empty-state">
                <el-icon size="64"><TrendCharts /></el-icon>
                <p>暂无学习进度</p>
                <el-button type="primary" @click="goToCourses">开始学习</el-button>
              </div>
              <div v-else>
                <div 
                  v-for="progress in learningProgress" 
                  :key="progress.subject_id"
                  class="progress-item"
                >
                  <div class="progress-info">
                    <h4>{{ progress.subject_name }}</h4>
                    <p>{{ progress.description }}</p>
                  </div>
                  <div class="progress-bar">
                    <el-progress 
                      :percentage="progress.completion_rate" 
                      :color="getProgressColor(progress.completion_rate)"
                    />
                    <span class="progress-text">{{ progress.completion_rate }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { Document, Star, Clock, TrendCharts } from '@element-plus/icons-vue'
import TopNavigation from '@/components/layout/TopNavigation.vue'

export default {
  name: 'UserDashboard',
  components: {
    TopNavigation,
    Document,
    Star,
    Clock,
    TrendCharts
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const examsLoading = ref(false)
    const progressLoading = ref(false)
    
    const stats = ref({
      totalExams: 0,
      averageScore: 0,
      studyHours: 0,
      rank: 0
    })
    
    const recentExams = ref([])
    const learningProgress = ref([])

    // 获取统计数据
    const fetchStats = async () => {
      try {
        // 模拟数据
        stats.value = {
          totalExams: 12,
          averageScore: 85,
          studyHours: 48,
          rank: 15
        }
      } catch (error) {
        console.error('获取统计数据失败:', error)
      }
    }

    // 获取最近考试
    const fetchRecentExams = async () => {
      try {
        examsLoading.value = true
        // 模拟数据
        recentExams.value = [
          {
            id: 1,
            title: 'Vue.js 3.0 基础测试',
            subject_name: '前端开发',
            score: 88,
            status: 'submitted',
            submit_time: '2024-01-15T10:30:00Z'
          },
          {
            id: 2,
            title: 'JavaScript 高级特性',
            subject_name: '前端开发',
            score: 92,
            status: 'submitted',
            submit_time: '2024-01-14T14:20:00Z'
          },
          {
            id: 3,
            title: 'Python 数据分析',
            subject_name: '数据分析',
            score: 76,
            status: 'submitted',
            submit_time: '2024-01-13T09:15:00Z'
          }
        ]
      } catch (error) {
        console.error('获取最近考试失败:', error)
      } finally {
        examsLoading.value = false
      }
    }

    // 获取学习进度
    const fetchLearningProgress = async () => {
      try {
        progressLoading.value = true
        // 模拟数据
        learningProgress.value = [
          {
            subject_id: 1,
            subject_name: 'Vue.js 3.0 实战开发',
            description: '深入学习Vue.js 3.0的核心特性和实战应用',
            completion_rate: 75
          },
          {
            subject_id: 2,
            subject_name: 'Python 数据分析',
            description: '掌握Python数据分析的核心技能',
            completion_rate: 60
          },
          {
            subject_id: 3,
            subject_name: 'UI/UX 设计基础',
            description: '学习现代UI/UX设计理念和实践',
            completion_rate: 45
          }
        ]
      } catch (error) {
        console.error('获取学习进度失败:', error)
      } finally {
        progressLoading.value = false
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    }

    // 获取成绩样式类
    const getScoreClass = (score) => {
      if (score >= 90) return 'excellent'
      if (score >= 80) return 'good'
      if (score >= 60) return 'pass'
      return 'fail'
    }

    // 获取状态类型
    const getStatusType = (status) => {
      switch (status) {
        case 'submitted': return 'success'
        case 'in_progress': return 'warning'
        case 'timeout': return 'danger'
        default: return 'info'
      }
    }

    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'submitted': return '已完成'
        case 'in_progress': return '进行中'
        case 'timeout': return '超时'
        default: return '未知'
      }
    }

    // 获取进度条颜色
    const getProgressColor = (percentage) => {
      if (percentage >= 80) return '#67c23a'
      if (percentage >= 60) return '#e6a23c'
      return '#f56c6c'
    }

    // 导航方法
    const goToRecords = () => {
      router.push('/user/my-records')
    }

    const goToProgress = () => {
      router.push('/user/learning-progress')
    }

    const goToCourses = () => {
      router.push('/courses')
    }

    const viewExamDetail = (exam) => {
      router.push(`/user/exam-detail/${exam.id}`)
    }

    onMounted(() => {
      fetchStats()
      fetchRecentExams()
      fetchLearningProgress()
    })

    return {
      authStore,
      stats,
      recentExams,
      learningProgress,
      examsLoading,
      progressLoading,
      formatDate,
      getScoreClass,
      getStatusType,
      getStatusText,
      getProgressColor,
      goToRecords,
      goToProgress,
      goToCourses,
      viewExamDetail
    }
  }
}
</script>

<style lang="scss" scoped>
.user-dashboard {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumb {
  padding: 20px 0;
  
  :deep(.el-breadcrumb__item) {
    .el-breadcrumb__inner {
      color: #666;
      
      &:hover {
        color: #667eea;
      }
    }
    
    &:last-child .el-breadcrumb__inner {
      color: #333;
    }
  }
}

.dashboard-content {
  padding-bottom: 4rem;
}

.page-header {
  margin-bottom: 2rem;
  
  h1 {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: #333;
  }
  
  p {
    font-size: 1.1rem;
    color: #666;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
  
  .stat-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    display: flex;
    align-items: center;
    gap: 1rem;
    
    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 12px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }
    
    .stat-content {
      h3 {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.25rem;
        color: #333;
      }
      
      p {
        color: #666;
        margin: 0;
      }
    }
  }
}

.main-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.content-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    
    h2 {
      font-size: 1.5rem;
      font-weight: bold;
      color: #333;
      margin: 0;
    }
  }
}

.exam-list, .progress-list {
  .empty-state {
    text-align: center;
    padding: 3rem 0;
    color: #999;
    
    .el-icon {
      margin-bottom: 1rem;
    }
    
    p {
      margin-bottom: 1rem;
    }
  }
}

.exam-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: #667eea;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
  }
  
  .exam-info {
    h4 {
      font-size: 1.1rem;
      font-weight: bold;
      margin-bottom: 0.25rem;
      color: #333;
    }
    
    p {
      color: #666;
      margin-bottom: 0.5rem;
    }
    
    .exam-meta {
      display: flex;
      gap: 1rem;
      
      .exam-date {
        color: #999;
        font-size: 0.9rem;
      }
      
      .exam-score {
        font-weight: bold;
        
        &.excellent {
          color: #67c23a;
        }
        
        &.good {
          color: #e6a23c;
        }
        
        &.pass {
          color: #409eff;
        }
        
        &.fail {
          color: #f56c6c;
        }
      }
    }
  }
}

.progress-item {
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 1rem;
  
  .progress-info {
    margin-bottom: 1rem;
    
    h4 {
      font-size: 1.1rem;
      font-weight: bold;
      margin-bottom: 0.25rem;
      color: #333;
    }
    
    p {
      color: #666;
      margin: 0;
    }
  }
  
  .progress-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    
    .el-progress {
      flex: 1;
    }
    
    .progress-text {
      font-weight: bold;
      color: #333;
      min-width: 50px;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .content-section {
    padding: 1.5rem;
  }
  
  .exam-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>
