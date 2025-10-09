<template>
  <div class="dashboard">
    <div class="page-header">
      <h1 class="page-title">仪表盘</h1>
      <p class="page-description">欢迎使用 ExamSphere 考试管理系统</p>
    </div>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon users">
            <el-icon><User /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalUsers }}</div>
            <div class="stat-label">总用户数</div>
          </div>
        </div>
      </el-col>
      
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon subjects">
            <el-icon><Reading /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalSubjects }}</div>
            <div class="stat-label">科目数量</div>
          </div>
        </div>
      </el-col>
      
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon questions">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalQuestions }}</div>
            <div class="stat-label">试题数量</div>
          </div>
        </div>
      </el-col>
      
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon exams">
            <el-icon><EditPen /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalExams }}</div>
            <div class="stat-label">考试数量</div>
          </div>
        </div>
      </el-col>
    </el-row>
    
    <!-- 快速操作 -->
    <el-row :gutter="20" class="quick-actions-row">
      <el-col :span="12">
        <div class="card-container">
          <h3>快速操作</h3>
          <div class="quick-actions">
            <el-button 
              v-if="isAdmin" 
              type="primary" 
              @click="$router.push('/admin/users')"
            >
              用户管理
            </el-button>
            <el-button 
              v-if="isUser" 
              type="warning" 
              @click="$router.push('/user/exam-list')"
            >
              参加考试
            </el-button>
          </div>
        </div>
      </el-col>
      
      <el-col :span="12">
        <div class="card-container">
          <h3>最近活动</h3>
          <div class="recent-activities">
            <div v-if="recentActivities.length === 0" class="no-data">
              暂无最近活动
            </div>
            <div 
              v-else
              v-for="activity in recentActivities" 
              :key="activity.id"
              class="activity-item"
            >
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-time">{{ formatDate(activity.created_at) }}</div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { formatDate } from '@/utils'

export default {
  name: 'Dashboard',
  setup() {
    const authStore = useAuthStore()
    
    // 响应式数据
    const stats = ref({
      totalUsers: 0,
      totalSubjects: 0,
      totalQuestions: 0,
      totalExams: 0
    })
    
    const recentActivities = ref([])
    
    // 计算属性
    const isAdmin = computed(() => authStore.isAdmin)
    const isUser = computed(() => authStore.isUser)
    
    // 加载统计数据
    const loadStats = async () => {
      try {
        // TODO: 调用API获取统计数据
        // 这里先使用模拟数据
        stats.value = {
          totalUsers: 156,
          totalSubjects: 12,
          totalQuestions: 1250,
          totalExams: 45
        }
      } catch (error) {
        console.error('加载统计数据失败:', error)
      }
    }
    
    // 加载最近活动
    const loadRecentActivities = async () => {
      try {
        // TODO: 调用API获取最近活动
        // 这里先使用模拟数据
        recentActivities.value = [
          {
            id: 1,
            title: '用户 张三 完成了考试《Java基础测试》',
            created_at: new Date()
          },
          {
            id: 2,
            title: '教师 李四 创建了新试题',
            created_at: new Date(Date.now() - 3600000)
          }
        ]
      } catch (error) {
        console.error('加载最近活动失败:', error)
      }
    }
    
    // 组件挂载时加载数据
    onMounted(() => {
      loadStats()
      loadRecentActivities()
    })
    
    return {
      stats,
      recentActivities,
      isAdmin,
      isUser,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  .stats-row {
    margin-bottom: 20px;
    
    .stat-card {
      background: #fff;
      border-radius: 8px;
      padding: 20px;
      display: flex;
      align-items: center;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
      
      .stat-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20px;
        font-size: 24px;
        color: #fff;
        
        &.users {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        &.subjects {
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        &.questions {
          background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        
        &.exams {
          background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }
      }
      
      .stat-content {
        .stat-number {
          font-size: 28px;
          font-weight: 600;
          color: #303133;
          margin-bottom: 5px;
        }
        
        .stat-label {
          font-size: 14px;
          color: #909399;
        }
      }
    }
  }
  
  .quick-actions-row {
    .card-container {
      h3 {
        margin-bottom: 20px;
        color: #303133;
      }
      
      .quick-actions {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
      }
      
      .recent-activities {
        .no-data {
          text-align: center;
          color: #909399;
          padding: 40px 0;
        }
        
        .activity-item {
          padding: 10px 0;
          border-bottom: 1px solid #f0f0f0;
          
          &:last-child {
            border-bottom: none;
          }
          
          .activity-content {
            .activity-title {
              font-size: 14px;
              color: #303133;
              margin-bottom: 5px;
            }
            
            .activity-time {
              font-size: 12px;
              color: #909399;
            }
          }
        }
      }
    }
  }
}
</style>
