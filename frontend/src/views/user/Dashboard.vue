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
          <div class="header-content">
            <div class="welcome-section">
              <div class="welcome-badge">
                <el-icon><Star /></el-icon>
                <span>欢迎回来</span>
              </div>
              <h1>学习数据中心</h1>
              <p>你好，{{ authStore.user?.username }}！查看您的学习数据和成绩分析 📊</p>
            </div>
            <div class="header-actions">
              <ThemeSwitcher />
            </div>
          </div>
        </div>

        <!-- 统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card" v-for="(stat, index) in statsData" :key="index">
            <div class="stat-icon" :style="{ background: stat.gradient }">
              <el-icon size="28"><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-content">
              <h3>{{ stat.value }}</h3>
              <p>{{ stat.label }}</p>
              <div class="stat-trend" :class="stat.trend">
                <el-icon size="14"><TrendCharts /></el-icon>
                <span>{{ stat.change }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 主要内容区域 -->
        <div class="main-content">
          <!-- 最近考试 -->
          <div class="content-section">
            <div class="section-header">
                 <div class="section-title">
                   <h2>考试记录</h2>
                   <p>查看您的考试历史和成绩分析</p>
                 </div>
              <el-button type="primary" @click="goToRecords" class="section-action">
                <el-icon><ArrowRight /></el-icon>
                查看全部
              </el-button>
            </div>
            <div class="exam-list" v-loading="examsLoading">
              <div v-if="recentExams.length === 0" class="empty-state">
                <div class="empty-icon">
                  <el-icon size="80"><Document /></el-icon>
                </div>
                   <h3>暂无考试记录</h3>
                   <p>开始您的第一次考试，记录将在这里显示</p>
                   <el-button type="primary" @click="goToCourses" class="empty-action">
                     <el-icon><Plus /></el-icon>
                     去首页参加考试
                   </el-button>
              </div>
              <div v-else class="exam-grid">
                <div 
                  v-for="exam in recentExams" 
                  :key="exam.id"
                  class="exam-card"
                  @click="viewExamDetail(exam)"
                >
                  <div class="exam-header">
                    <div class="exam-title">
                      <h4>{{ exam.title }}</h4>
                      <span class="exam-category">{{ exam.subject_name }}</span>
                    </div>
                    <div class="exam-score" :class="getScoreClass(exam.score)">
                      {{ exam.score }}分
                    </div>
                  </div>
                  <div class="exam-footer">
                    <div class="exam-date">
                      <el-icon><Calendar /></el-icon>
                      <span>{{ formatDate(exam.submit_time) }}</span>
                    </div>
                    <el-tag :type="getStatusType(exam.status)" class="exam-status">
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
                 <div class="section-title">
                   <h2>学习分析</h2>
                   <p>跟踪您的学习进度和知识掌握情况</p>
                 </div>
              <el-button type="primary" @click="goToProgress" class="section-action">
                <el-icon><ArrowRight /></el-icon>
                查看详情
              </el-button>
            </div>
            <div class="progress-list" v-loading="progressLoading">
              <div v-if="learningProgress.length === 0" class="empty-state">
                <div class="empty-icon">
                  <el-icon size="80"><TrendCharts /></el-icon>
                </div>
                   <h3>暂无学习数据</h3>
                   <p>开始学习新课程，进度将在这里显示</p>
                   <el-button type="primary" @click="goToCourses" class="empty-action">
                     <el-icon><Plus /></el-icon>
                     去首页学习课程
                   </el-button>
              </div>
              <div v-else class="progress-grid">
                <div 
                  v-for="progress in learningProgress" 
                  :key="progress.subject_id"
                  class="progress-card"
                >
                  <div class="progress-header">
                    <h4>{{ progress.subject_name }}</h4>
                    <span class="progress-percentage">{{ progress.completion_rate }}%</span>
                  </div>
                  <p class="progress-description">{{ progress.description }}</p>
                  <div class="progress-bar-container">
                    <el-progress 
                      :percentage="progress.completion_rate" 
                      :color="getProgressColor(progress.completion_rate)"
                      :stroke-width="8"
                      :show-text="false"
                    />
                  </div>
                  <div class="progress-footer">
                    <div class="progress-stats">
                      <span class="stat-item">
                        <el-icon><Clock /></el-icon>
                        {{ Math.floor(Math.random() * 20) + 5 }}小时
                      </span>
                      <span class="stat-item">
                        <el-icon><Document /></el-icon>
                        {{ Math.floor(Math.random() * 10) + 1 }}个章节
                      </span>
                    </div>
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
import { Document, Star, Clock, TrendCharts, ArrowRight, Plus, Calendar } from '@element-plus/icons-vue'
import TopNavigation from '@/components/layout/TopNavigation.vue'
import ThemeSwitcher from '@/components/common/ThemeSwitcher.vue'

export default {
  name: 'UserDashboard',
  components: {
    TopNavigation,
    ThemeSwitcher,
    Document,
    Star,
    Clock,
    TrendCharts,
    ArrowRight,
    Plus,
    Calendar
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const examsLoading = ref(false)
    const progressLoading = ref(false)
    
       // 统计数据
       const statsData = ref([
         {
           icon: 'Document',
           value: 12,
           label: '已完成考试',
           gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
           trend: 'up',
           change: '+2 本周'
         },
         {
           icon: 'Star',
           value: 85,
           label: '平均成绩',
           gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
           trend: 'up',
           change: '+5 本月'
         },
         {
           icon: 'Clock',
           value: 48,
           label: '学习时长(小时)',
           gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
           trend: 'up',
           change: '+8 本周'
         },
         {
           icon: 'TrendCharts',
           value: 15,
           label: '学习排名',
           gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
           trend: 'up',
           change: '+3 本月'
         }
       ])
    
    const recentExams = ref([])
    const learningProgress = ref([])


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
         router.push('/')
       }

    const viewExamDetail = (exam) => {
      router.push(`/user/exam-detail/${exam.id}`)
    }

    onMounted(() => {
      fetchRecentExams()
      fetchLearningProgress()
    })

    return {
      authStore,
      statsData,
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
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumb {
  padding: 20px 0;
  
  :deep(.el-breadcrumb__item) {
    .el-breadcrumb__inner {
      color: #666;
      
      &:hover {
        color: var(--theme-primary, #667eea);
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
  margin-bottom: 3rem;
  
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    background: white;
    border-radius: 20px;
    padding: 3rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    
    .welcome-section {
      flex: 1;
      
      .welcome-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
      }
      
      h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #333;
        background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
      }
      
      p {
        font-size: 1.2rem;
        color: #666;
        font-weight: 500;
        margin: 0;
      }
    }
    
    .header-actions {
      display: flex;
      align-items: center;
      gap: 1rem;
    }
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
  
  .stat-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    
    &:hover {
      transform: translateY(-8px);
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
    }
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
    }
    
    .stat-icon {
      width: 70px;
      height: 70px;
      border-radius: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      margin-bottom: 1.5rem;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    
    .stat-content {
      h3 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: #333;
        line-height: 1;
      }
      
      p {
        color: #666;
        margin: 0 0 1rem 0;
        font-size: 1rem;
        font-weight: 500;
      }
      
      .stat-trend {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        font-weight: 600;
        
        &.up {
          color: #67c23a;
        }
        
        &.down {
          color: #f56c6c;
        }
      }
    }
  }
}

.main-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2.5rem;
}

.content-section {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 2rem;
    
    .section-title {
      h2 {
        font-size: 1.8rem;
        font-weight: 800;
        color: #333;
        margin: 0 0 0.5rem 0;
        background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }
      
      p {
        color: #666;
        margin: 0;
        font-size: 1rem;
        font-weight: 500;
      }
    }
    
    .section-action {
      border-radius: 12px;
      padding: 0.8rem 1.5rem;
      font-weight: 600;
      background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
      border: none;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
      }
    }
  }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #999;
  
  .empty-icon {
    width: 120px;
    height: 120px;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 2rem;
    color: #ccc;
  }
  
  h3 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #333;
  }
  
  p {
    font-size: 1rem;
    margin-bottom: 2rem;
    color: #666;
  }
  
  .empty-action {
    border-radius: 12px;
    padding: 1rem 2rem;
    font-weight: 600;
    background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
    border: none;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
  }
}

.exam-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.exam-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(102, 126, 234, 0.1);
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(102, 126, 234, 0.15);
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  }
  
  .exam-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
    
    .exam-title {
      flex: 1;
      
      h4 {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: #333;
        line-height: 1.3;
      }
      
      .exam-category {
        display: inline-block;
        background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
      }
    }
    
    .exam-score {
      font-size: 1.5rem;
      font-weight: 800;
      padding: 0.5rem 1rem;
      border-radius: 12px;
      
      &.excellent {
        background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
        color: white;
      }
      
      &.good {
        background: linear-gradient(135deg, #e6a23c 0%, #f0c78a 100%);
        color: white;
      }
      
      &.pass {
        background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);
        color: white;
      }
      
      &.fail {
        background: linear-gradient(135deg, #f56c6c 0%, #f89898 100%);
        color: white;
      }
    }
  }
  
  .exam-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .exam-date {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: #666;
      font-size: 0.9rem;
    }
    
    .exam-status {
      border-radius: 8px;
      font-weight: 600;
    }
  }
}

.progress-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.progress-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  border: 1px solid rgba(102, 126, 234, 0.1);
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(102, 126, 234, 0.15);
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  }
  
  .progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    
    h4 {
      font-size: 1.2rem;
      font-weight: 700;
      margin: 0;
      color: #333;
    }
    
    .progress-percentage {
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--theme-primary, #667eea);
    }
  }
  
  .progress-description {
    color: #666;
    margin: 0 0 1.5rem 0;
    line-height: 1.5;
  }
  
  .progress-bar-container {
    margin-bottom: 1rem;
    
    :deep(.el-progress-bar__outer) {
      border-radius: 10px;
      background: #e9ecef;
    }
    
    :deep(.el-progress-bar__inner) {
      border-radius: 10px;
    }
  }
  
  .progress-footer {
    .progress-stats {
      display: flex;
      gap: 1.5rem;
      
      .stat-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #666;
        font-size: 0.9rem;
        font-weight: 500;
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .page-header .header-content {
    flex-direction: column;
    gap: 2rem;
    padding: 2rem;
    
    .welcome-section h1 {
      font-size: 2.5rem;
    }
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .content-section {
    padding: 1.5rem;
  }
  
  .exam-grid,
  .progress-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>
