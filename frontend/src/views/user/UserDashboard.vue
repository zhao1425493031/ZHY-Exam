<template>
  <div class="user-dashboard">
    <!-- 用户信息头部 -->
    <div class="user-header">
      <div class="container">
        <div class="user-profile">
          <div class="avatar-section">
            <el-avatar :size="80" :src="userInfo.avatar || '/default-avatar.svg'">
              {{ userInfo.username?.charAt(0).toUpperCase() }}
            </el-avatar>
            <div class="online-indicator"></div>
          </div>
          <div class="user-info">
            <h1>{{ userInfo.real_name || userInfo.username }}</h1>
            <p>{{ userInfo.email }}</p>
            <div class="user-badges">
              <el-tag type="success" size="small">
                <el-icon><Star /></el-icon>
                活跃用户
              </el-tag>
              <el-tag type="info" size="small">
                <el-icon><Calendar /></el-icon>
                加入 {{ formatJoinDate(userInfo.created_at) }}
              </el-tag>
            </div>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="editProfile">
              <el-icon><Edit /></el-icon>
              编辑资料
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="dashboard-content">
      <div class="container">
        <!-- 统计概览 -->
        <div class="stats-overview">
          <div class="stat-card" v-for="(stat, index) in statsData" :key="index">
            <div class="stat-icon" :class="stat.type">
              <el-icon><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-content">
              <h3>{{ stat.value }}</h3>
              <p>{{ stat.label }}</p>
              <div class="stat-trend" :class="stat.trend">
                <el-icon><component :is="stat.trendIcon" /></el-icon>
                <span>{{ stat.change }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 主要内容区域 -->
        <div class="main-content">
          <!-- 左侧：最近活动 -->
          <div class="content-left">
            <!-- 最近考试 -->
            <div class="activity-card">
              <div class="card-header">
                <h3>
                  <el-icon><Document /></el-icon>
                  最近考试
                </h3>
                <router-link to="/user/exam-list" class="view-all">
                  查看全部 <el-icon><ArrowRight /></el-icon>
                </router-link>
              </div>
              <div class="card-content">
                <div class="exam-list" v-if="recentExams.length > 0">
                  <div class="exam-item" v-for="exam in recentExams" :key="exam.id">
                    <div class="exam-info">
                      <h4>{{ exam.title }}</h4>
                      <p>{{ exam.subject_name }}</p>
                      <span class="exam-date">{{ formatDate(exam.created_at) }}</span>
                    </div>
                    <div class="exam-score" :class="getScoreClass(exam.score)">
                      {{ exam.score || 0 }}分
                    </div>
                  </div>
                </div>
                <div class="empty-state" v-else>
                  <el-icon size="48"><Document /></el-icon>
                  <p>暂无考试记录</p>
                  <el-button type="primary" @click="$router.push('/')">
                    开始考试
                  </el-button>
                </div>
              </div>
            </div>

            <!-- 学习进度 -->
            <div class="activity-card">
              <div class="card-header">
                <h3>
                  <el-icon><TrendCharts /></el-icon>
                  学习进度
                </h3>
                <router-link to="/user/learning-progress" class="view-all">
                  查看详情 <el-icon><ArrowRight /></el-icon>
                </router-link>
              </div>
              <div class="card-content">
                <div class="progress-list" v-if="learningProgress.length > 0">
                  <div class="progress-item" v-for="progress in learningProgress" :key="progress.id">
                    <div class="progress-info">
                      <h4>{{ progress.subject_name }}</h4>
                      <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: progress.percentage + '%' }"></div>
                      </div>
                      <span class="progress-text">{{ progress.percentage }}% 完成</span>
                    </div>
                  </div>
                </div>
                <div class="empty-state" v-else>
                  <el-icon size="48"><TrendCharts /></el-icon>
                  <p>暂无学习进度</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 右侧：快捷操作和通知 -->
          <div class="content-right">
            <!-- 快捷操作 -->
            <div class="quick-actions-card">
              <div class="card-header">
                <h3>
                  <el-icon><Lightning /></el-icon>
                  快捷操作
                </h3>
              </div>
              <div class="card-content">
                <div class="action-grid">
                  <div class="action-item" @click="$router.push('/')">
                    <div class="action-icon exam">
                      <el-icon><Document /></el-icon>
                    </div>
                    <span>开始考试</span>
                  </div>
                  <div class="action-item" @click="$router.push('/user/exam-list')">
                    <div class="action-icon list">
                      <el-icon><List /></el-icon>
                    </div>
                    <span>考试列表</span>
                  </div>
                  <div class="action-item" @click="$router.push('/user/my-records')">
                    <div class="action-icon records">
                      <el-icon><Clock /></el-icon>
                    </div>
                    <span>我的记录</span>
                  </div>
                  <div class="action-item" @click="$router.push('/user/wrong-answers')">
                    <div class="action-icon wrong">
                      <el-icon><Warning /></el-icon>
                    </div>
                    <span>错题本</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 最新通知 -->
            <div class="notifications-card">
              <div class="card-header">
                <h3>
                  <el-icon><Bell /></el-icon>
                  最新通知
                </h3>
                <router-link to="/user/notifications" class="view-all">
                  查看全部 <el-icon><ArrowRight /></el-icon>
                </router-link>
              </div>
              <div class="card-content">
                <div class="notification-list" v-if="notifications.length > 0">
                  <div class="notification-item" v-for="notification in notifications" :key="notification.id">
                    <div class="notification-icon" :class="notification.type">
                      <el-icon><component :is="getNotificationIcon(notification.type)" /></el-icon>
                    </div>
                    <div class="notification-content">
                      <h4>{{ notification.title }}</h4>
                      <p>{{ notification.content }}</p>
                      <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
                    </div>
                  </div>
                </div>
                <div class="empty-state" v-else>
                  <el-icon size="48"><Bell /></el-icon>
                  <p>暂无新通知</p>
                </div>
              </div>
            </div>

            <!-- 成就展示 -->
            <div class="achievements-card">
              <div class="card-header">
                <h3>
                  <el-icon><Trophy /></el-icon>
                  学习成就
                </h3>
              </div>
              <div class="card-content">
                <div class="achievements-grid">
                  <div class="achievement-item" v-for="achievement in achievements" :key="achievement.id">
                    <div class="achievement-icon" :class="{ unlocked: achievement.unlocked }">
                      <el-icon><component :is="achievement.icon" /></el-icon>
                    </div>
                    <div class="achievement-info">
                      <h4>{{ achievement.name }}</h4>
                      <p>{{ achievement.description }}</p>
                      <div class="achievement-progress" v-if="!achievement.unlocked">
                        <div class="progress-bar">
                          <div class="progress-fill" :style="{ width: achievement.progress + '%' }"></div>
                        </div>
                        <span>{{ achievement.progress }}%</span>
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
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Star, Calendar, Edit, Document, ArrowRight, TrendCharts, 
  Lightning, List, Clock, Warning, Bell, Trophy, 
  CheckCircle, InfoFilled, WarningFilled, CircleCloseFilled
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { examRecordsApi } from '@/api/exam_records'
import { subjectsApi } from '@/api/subjects'
import { notificationApi } from '@/api/notifications'
import dayjs from 'dayjs'

export default {
  name: 'UserDashboard',
  components: {
    Star,
    Calendar,
    Edit,
    Document,
    ArrowRight,
    TrendCharts,
    Lightning,
    List,
    Clock,
    Warning,
    Bell,
    Trophy,
    CheckCircle,
    InfoFilled,
    WarningFilled,
    CircleCloseFilled
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const userInfo = ref({})
    const recentExams = ref([])
    const learningProgress = ref([])
    const notifications = ref([])
    const achievements = ref([])

    // 统计数据
    const statsData = ref([
      {
        icon: 'Document',
        label: '已完成考试',
        value: '0',
        change: '+0 本周',
        trend: 'positive',
        trendIcon: 'ArrowUp',
        type: 'exam'
      },
      {
        icon: 'Star',
        label: '平均成绩',
        value: '0',
        change: '+0 本月',
        trend: 'positive',
        trendIcon: 'ArrowUp',
        type: 'score'
      },
      {
        icon: 'Clock',
        label: '学习时长',
        value: '0小时',
        change: '+0 本周',
        trend: 'positive',
        trendIcon: 'ArrowUp',
        type: 'time'
      },
      {
        icon: 'TrendCharts',
        label: '学习排名',
        value: '--',
        change: '--',
        trend: 'neutral',
        trendIcon: 'Minus',
        type: 'rank'
      }
    ])

    // 获取用户信息
    const fetchUserInfo = async () => {
      try {
        userInfo.value = authStore.user || {}
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }

    // 获取最近考试记录
    const fetchRecentExams = async () => {
      try {
        const response = await examRecordsApi.getExamRecords({
          page: 1,
          size: 5
        })
        if (response.code === 200) {
          recentExams.value = response.data.items || []
        }
      } catch (error) {
        console.error('获取最近考试失败:', error)
      }
    }

    // 获取学习进度
    const fetchLearningProgress = async () => {
      try {
        const response = await subjectsApi.getSubjects({
          status: 'active',
          page: 1,
          size: 5
        })
        if (response.code === 200) {
          // 模拟学习进度数据
          learningProgress.value = (response.data.items || []).map(subject => ({
            id: subject.id,
            subject_name: subject.name,
            percentage: Math.floor(Math.random() * 100)
          }))
        }
      } catch (error) {
        console.error('获取学习进度失败:', error)
      }
    }

    // 获取通知
    const fetchNotifications = async () => {
      try {
        const response = await notificationApi.getNotifications({
          page: 1,
          size: 5
        })
        if (response.code === 200) {
          notifications.value = response.data.items || []
        }
      } catch (error) {
        console.error('获取通知失败:', error)
      }
    }

    // 初始化成就数据
    const initAchievements = () => {
      achievements.value = [
        {
          id: 1,
          name: '初试牛刀',
          description: '完成第一次考试',
          icon: 'Trophy',
          unlocked: recentExams.value.length > 0,
          progress: Math.min(100, recentExams.value.length * 100)
        },
        {
          id: 2,
          name: '学习达人',
          description: '学习时长达到10小时',
          icon: 'Clock',
          unlocked: false,
          progress: 0
        },
        {
          id: 3,
          name: '高分王者',
          description: '单次考试得分90分以上',
          icon: 'Star',
          unlocked: recentExams.value.some(exam => exam.score >= 90),
          progress: 0
        }
      ]
    }

    // 更新统计数据
    const updateStats = () => {
      const completedExams = recentExams.value.length
      const averageScore = recentExams.value.length > 0 
        ? Math.round(recentExams.value.reduce((sum, exam) => sum + (exam.score || 0), 0) / recentExams.value.length)
        : 0

      statsData.value[0].value = completedExams.toString()
      statsData.value[1].value = averageScore.toString()
      statsData.value[0].change = `+${completedExams} 本周`
      statsData.value[1].change = `+${averageScore} 本月`
    }

    // 格式化日期
    const formatDate = (date) => {
      if (!date) return ''
      return dayjs(date).format('MM/DD')
    }

    // 格式化时间
    const formatTime = (date) => {
      if (!date) return ''
      return dayjs(date).fromNow()
    }

    // 格式化加入日期
    const formatJoinDate = (date) => {
      if (!date) return ''
      return dayjs(date).format('YYYY年MM月')
    }

    // 获取分数样式类
    const getScoreClass = (score) => {
      if (!score) return 'no-score'
      if (score >= 90) return 'excellent'
      if (score >= 80) return 'good'
      if (score >= 60) return 'pass'
      return 'fail'
    }

    // 获取通知图标
    const getNotificationIcon = (type) => {
      const iconMap = {
        'system': 'InfoFilled',
        'exam': 'Document',
        'score': 'Star',
        'announcement': 'Bell'
      }
      return iconMap[type] || 'InfoFilled'
    }

    // 编辑资料
    const editProfile = () => {
      ElMessage.info('编辑资料功能开发中...')
    }

    onMounted(async () => {
      await fetchUserInfo()
      await fetchRecentExams()
      await fetchLearningProgress()
      await fetchNotifications()
      initAchievements()
      updateStats()
    })

    return {
      userInfo,
      recentExams,
      learningProgress,
      notifications,
      achievements,
      statsData,
      formatDate,
      formatTime,
      formatJoinDate,
      getScoreClass,
      getNotificationIcon,
      editProfile
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

// 用户信息头部
.user-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 0;

  .user-profile {
    display: flex;
    align-items: center;
    gap: 2rem;

    .avatar-section {
      position: relative;

      .online-indicator {
        position: absolute;
        bottom: 5px;
        right: 5px;
        width: 20px;
        height: 20px;
        background: #67c23a;
        border: 3px solid white;
        border-radius: 50%;
      }
    }

    .user-info {
      flex: 1;

      h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
      }

      p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0 0 1rem 0;
      }

      .user-badges {
        display: flex;
        gap: 0.5rem;
      }
    }

    .header-actions {
      .el-button {
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
      }
    }
  }
}

// 统计概览
.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0 2rem 0;

  .stat-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    gap: 1.5rem;

    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: white;

      &.exam {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }

      &.score {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      }

      &.time {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }

      &.rank {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
      }
    }

    .stat-content {
      flex: 1;

      h3 {
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        color: #333;
      }

      p {
        font-size: 1rem;
        color: #666;
        margin: 0 0 0.5rem 0;
      }

      .stat-trend {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        font-size: 0.9rem;

        &.positive {
          color: #67c23a;
        }

        &.negative {
          color: #f56c6c;
        }

        &.neutral {
          color: #909399;
        }
      }
    }
  }
}

// 主要内容区域
.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

// 卡片通用样式
.activity-card,
.quick-actions-card,
.notifications-card,
.achievements-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 2rem;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem 1rem;
    border-bottom: 1px solid #f0f0f0;

    h3 {
      font-size: 1.3rem;
      font-weight: 700;
      margin: 0;
      color: #333;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .view-all {
      color: #667eea;
      text-decoration: none;
      font-size: 0.9rem;
      display: flex;
      align-items: center;
      gap: 0.3rem;
      transition: color 0.3s ease;

      &:hover {
        color: #5a6fd8;
      }
    }
  }

  .card-content {
    padding: 1.5rem 2rem 2rem;
  }
}

// 考试列表
.exam-list {
  .exam-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid #f5f5f5;

    &:last-child {
      border-bottom: none;
    }

    .exam-info {
      flex: 1;

      h4 {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.3rem 0;
        color: #333;
      }

      p {
        font-size: 0.9rem;
        color: #666;
        margin: 0 0 0.3rem 0;
      }

      .exam-date {
        font-size: 0.8rem;
        color: #999;
      }
    }

    .exam-score {
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-weight: 600;
      font-size: 0.9rem;

      &.excellent {
        background: #f0f9ff;
        color: #1890ff;
      }

      &.good {
        background: #f6ffed;
        color: #52c41a;
      }

      &.pass {
        background: #fff7e6;
        color: #fa8c16;
      }

      &.fail {
        background: #fff2f0;
        color: #ff4d4f;
      }

      &.no-score {
        background: #f5f5f5;
        color: #999;
      }
    }
  }
}

// 学习进度
.progress-list {
  .progress-item {
    margin-bottom: 1.5rem;

    &:last-child {
      margin-bottom: 0;
    }

    h4 {
      font-size: 1rem;
      font-weight: 600;
      margin: 0 0 0.8rem 0;
      color: #333;
    }

    .progress-bar {
      width: 100%;
      height: 8px;
      background: #f0f0f0;
      border-radius: 4px;
      overflow: hidden;
      margin-bottom: 0.5rem;

      .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
      }
    }

    .progress-text {
      font-size: 0.9rem;
      color: #666;
    }
  }
}

// 快捷操作
.action-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;

  .action-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.8rem;
    padding: 1.5rem 1rem;
    border-radius: 15px;
    background: #f8f9fa;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      background: #e9ecef;
      transform: translateY(-2px);
    }

    .action-icon {
      width: 50px;
      height: 50px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      color: white;

      &.exam {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }

      &.list {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      }

      &.records {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }

      &.wrong {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
      }
    }

    span {
      font-size: 0.9rem;
      font-weight: 600;
      color: #333;
    }
  }
}

// 通知列表
.notification-list {
  .notification-item {
    display: flex;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #f5f5f5;

    &:last-child {
      border-bottom: none;
    }

    .notification-icon {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      color: white;
      flex-shrink: 0;

      &.system {
        background: #1890ff;
      }

      &.exam {
        background: #52c41a;
      }

      &.score {
        background: #fa8c16;
      }

      &.announcement {
        background: #722ed1;
      }
    }

    .notification-content {
      flex: 1;

      h4 {
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 0.3rem 0;
        color: #333;
      }

      p {
        font-size: 0.9rem;
        color: #666;
        margin: 0 0 0.3rem 0;
        line-height: 1.4;
      }

      .notification-time {
        font-size: 0.8rem;
        color: #999;
      }
    }
  }
}

// 成就展示
.achievements-grid {
  .achievement-item {
    display: flex;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #f5f5f5;

    &:last-child {
      border-bottom: none;
    }

    .achievement-icon {
      width: 50px;
      height: 50px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      background: #f5f5f5;
      color: #999;
      flex-shrink: 0;

      &.unlocked {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: white;
      }
    }

    .achievement-info {
      flex: 1;

      h4 {
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 0.3rem 0;
        color: #333;
      }

      p {
        font-size: 0.9rem;
        color: #666;
        margin: 0 0 0.5rem 0;
      }

      .achievement-progress {
        display: flex;
        align-items: center;
        gap: 0.5rem;

        .progress-bar {
          flex: 1;
          height: 4px;
          background: #f0f0f0;
          border-radius: 2px;
          overflow: hidden;

          .progress-fill {
            height: 100%;
            background: #667eea;
            transition: width 0.3s ease;
          }
        }

        span {
          font-size: 0.8rem;
          color: #666;
          min-width: 35px;
        }
      }
    }
  }
}

// 空状态
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #999;

  .el-icon {
    margin-bottom: 1rem;
  }

  p {
    margin: 0 0 1rem 0;
    font-size: 1rem;
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .user-header {
    padding: 1.5rem 0;

    .user-profile {
      flex-direction: column;
      text-align: center;
      gap: 1.5rem;
    }
  }

  .stats-overview {
    grid-template-columns: 1fr;
    margin: -0.5rem 0 1.5rem 0;

    .stat-card {
      padding: 1.5rem;
    }
  }

  .action-grid {
    grid-template-columns: 1fr;
  }

  .activity-card,
  .quick-actions-card,
  .notifications-card,
  .achievements-card {
    margin-bottom: 1.5rem;

    .card-header {
      padding: 1rem 1.5rem 0.5rem;
    }

    .card-content {
      padding: 1rem 1.5rem 1.5rem;
    }
  }
}
</style>
