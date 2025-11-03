<template>
  <div class="admin-dashboard">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="logo-section">
            <div class="logo-icon">
              <el-icon><Setting /></el-icon>
            </div>
            <div class="logo-text">
              <h1>管理员控制台</h1>
              <p>ExamSphere 后台管理系统</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <div class="user-info">
            <el-avatar :size="40" :src="userAvatar" class="user-avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <div class="user-details">
              <span class="user-name">系统管理员</span>
              <span class="user-role">Administrator</span>
            </div>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="goToHome" class="action-btn">
              <el-icon><HomeFilled /></el-icon>
              <span>返回首页</span>
            </el-button>
            <el-button type="danger" @click="logout" class="action-btn">
              <el-icon><SwitchButton /></el-icon>
              <span>退出登录</span>
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 现代化统计卡片 -->
    <div class="stats-section">
      <div class="section-header">
        <h2>系统概览</h2>
        <p>实时数据统计</p>
      </div>
      <div class="stats-grid">
        <div class="stat-card modern-card" v-for="(stat, index) in statsData" :key="index">
          <div class="stat-icon" :class="stat.iconClass">
            <el-icon><component :is="stat.icon" /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
            <div class="stat-trend" :class="stat.trendClass">
              <el-icon><component :is="stat.trendIcon" /></el-icon>
              <span>{{ stat.trend }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 现代化功能模块 -->
    <div class="modules-section">
      <div class="section-header">
        <h2>管理功能</h2>
        <p>快速访问系统管理功能</p>
      </div>
      <div class="modules-grid">
        <div 
          class="module-card modern-card" 
          :class="{ 'disabled': module.disabled }"
          v-for="(module, index) in modulesData" 
          :key="index"
          @click="goToModule(module.path)"
        >
          <div class="module-icon" :class="module.iconClass">
            <el-icon><component :is="module.icon" /></el-icon>
          </div>
          <div class="module-content">
            <h3>{{ module.title }}</h3>
            <p>{{ module.description }}</p>
          </div>
          <div class="module-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>
    </div>

    <!-- 快速操作面板 -->
    <div class="quick-actions-section">
      <div class="section-header">
        <h2>快速操作</h2>
        <p>常用管理功能</p>
      </div>
      <div class="quick-actions-grid">
        <div class="quick-action-card" v-for="(action, index) in quickActions" :key="index">
          <div class="action-icon" :class="action.iconClass">
            <el-icon><component :is="action.icon" /></el-icon>
          </div>
          <div class="action-content">
            <h4>{{ action.title }}</h4>
            <p>{{ action.description }}</p>
          </div>
          <el-button type="primary" size="small" @click="action.handler">
            {{ action.buttonText }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Setting, HomeFilled, SwitchButton, User, Reading, Document, 
  QuestionFilled, Collection, EditPen, TrendCharts, Lock, 
  Upload, DataAnalysis, ArrowRight, Plus, Search, Download,
  TrendCharts as TrendUp, TrendCharts as TrendDown, Link
} from '@element-plus/icons-vue'

export default {
  name: 'AdminDashboard',
  components: {
    Setting,
    HomeFilled,
    SwitchButton,
    User,
    Reading,
    Document,
    QuestionFilled,
    Collection,
    EditPen,
    TrendCharts,
    Lock,
    Upload,
    DataAnalysis,
    ArrowRight,
    Plus,
    Search,
    Download,
    TrendUp,
    TrendDown,
    Link
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // 用户头像
    const userAvatar = ref('')
    
    // 统计数据
    const statsData = ref([
      {
        icon: 'User',
        iconClass: 'users',
        value: '1,250',
        label: '总用户数',
        trend: '+12%',
        trendClass: 'trend-up',
        trendIcon: 'TrendUp'
      },
      {
        icon: 'Reading',
        iconClass: 'subjects',
        value: '45',
        label: '科目总数',
        trend: '+8%',
        trendClass: 'trend-up',
        trendIcon: 'TrendUp'
      },
      {
        icon: 'Document',
        iconClass: 'exams',
        value: '320',
        label: '考试总数',
        trend: '+15%',
        trendClass: 'trend-up',
        trendIcon: 'TrendUp'
      },
      {
        icon: 'QuestionFilled',
        iconClass: 'questions',
        value: '8,500',
        label: '试题总数',
        trend: '+23%',
        trendClass: 'trend-up',
        trendIcon: 'TrendUp'
      }
    ])

    // 功能模块数据
    const modulesData = ref([
      {
        icon: 'User',
        iconClass: 'users',
        title: '用户管理',
        description: '管理系统用户账户和权限',
        path: '/admin/users'
      },
      {
        icon: 'Reading',
        iconClass: 'subjects',
        title: '科目管理',
        description: '管理考试科目和分类',
        path: '/admin/subjects'
      },
      {
        icon: 'Link',
        iconClass: 'user-subjects',
        title: '用户课程关联',
        description: '管理用户和课程之间的关联',
        path: '/admin/user-subjects'
      },
      {
        icon: 'QuestionFilled',
        iconClass: 'questions',
        title: '试题管理',
        description: '管理题库和试题内容',
        path: '/admin/questions'
      },
      {
        icon: 'Document',
        iconClass: 'exams',
        title: '考试管理',
        description: '创建和管理考试',
        path: '/admin/exams'
      },
      {
        icon: 'Collection',
        iconClass: 'question-bank',
        title: '题库管理',
        description: '管理试题分类和标签',
        path: '/admin/question-bank'
      },
      {
        icon: 'EditPen',
        iconClass: 'exam-creation',
        title: '考试创建',
        description: '快速创建和配置考试',
        path: '/admin/exam-creation'
      },
      {
        icon: 'TrendCharts',
        iconClass: 'exam-analysis',
        title: '考试分析',
        description: '分析考试数据和成绩',
        path: '/admin/exam-analysis'
      },
      {
        icon: 'Lock',
        iconClass: 'permissions disabled',
        title: '权限管理',
        description: '即将推出 - 角色和权限配置功能',
        path: null,
        disabled: false
      },
      {
        icon: 'Upload',
        iconClass: 'import-export',
        title: '导入导出',
        description: '批量导入导出数据',
        path: '/admin/import-export'
      },
      {
        icon: 'DataAnalysis',
        iconClass: 'statistics',
        title: '统计分析',
        description: '系统数据统计分析',
        path: '/admin/statistics'
      }
    ])

    // 快速操作
    const quickActions = ref([
      {
        icon: 'Plus',
        iconClass: 'add-user',
        title: '添加用户',
        description: '快速创建新用户账户',
        buttonText: '立即添加',
        handler: () => goToModule('/admin/users')
      },
      {
        icon: 'Search',
        iconClass: 'search',
        title: '搜索用户',
        description: '查找特定用户信息',
        buttonText: '开始搜索',
        handler: () => goToModule('/admin/users')
      },
      {
        icon: 'Download',
        iconClass: 'export',
        title: '导出数据',
        description: '导出系统数据报告',
        buttonText: '导出',
        handler: () => goToModule('/admin/import-export')
      }
    ])

    // 跳转到功能模块
    const goToModule = (path) => {
      if (!path) {
        ElMessage.info('该功能即将推出，敬请期待！')
        return
      }
      router.push(path)
    }

    // 返回首页
    const goToHome = () => {
      router.push('/')
    }

    // 退出登录
    const logout = async () => {
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await authStore.logoutAction()
        router.push('/')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('退出登录失败:', error)
        }
      }
    }

    onMounted(() => {
      // 初始化数据
    })

    return {
      userAvatar,
      statsData,
      modulesData,
      quickActions,
      goToModule,
      goToHome,
      logout
    }
  }
}
</script>

<style lang="scss" scoped>
.admin-dashboard {
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
      .logo-section {
        display: flex;
        align-items: center;
        gap: 16px;
        
        .logo-icon {
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
        
        .logo-text {
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
      align-items: center;
      gap: 24px;
      
      .user-info {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(255, 255, 255, 0.1);
        padding: 8px 16px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        
        .user-avatar {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .user-details {
          display: flex;
          flex-direction: column;
          
          .user-name {
            color: white;
            font-size: 14px;
            font-weight: 600;
          }
          
          .user-role {
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
          }
        }
      }
      
      .header-actions {
        display: flex;
        gap: 12px;
        
        .action-btn {
          padding: 12px 20px;
          font-weight: 600;
          border-radius: 12px;
          display: flex;
          align-items: center;
          gap: 8px;
          transition: all 0.3s ease;
          
          &.el-button--primary {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.3);
            color: white;
            
            &:hover {
              background: rgba(255, 255, 255, 0.3);
              transform: translateY(-2px);
            }
          }
          
          &.el-button--danger {
            background: rgba(245, 108, 108, 0.8);
            border-color: rgba(245, 108, 108, 0.9);
            
            &:hover {
              background: rgba(245, 108, 108, 1);
              transform: translateY(-2px);
            }
          }
        }
      }
    }
  }
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
  
  h2 {
    color: white;
    font-size: 32px;
    font-weight: 700;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
  }
  
  p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 16px;
    margin: 0;
    font-weight: 500;
  }
}

.stats-section {
  padding: 60px 32px;
  
  .stats-grid {
    max-width: 1800px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
  }
  
  .stat-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    display: flex;
    align-items: center;
    gap: 24px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    &:hover {
      transform: translateY(-8px);
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
    }
    
    .stat-icon {
      width: 72px;
      height: 72px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      color: white;
      
      &.users {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }
      
      &.subjects {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      }
      
      &.exams {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }
      
      &.questions {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
      }
    }
    
    .stat-content {
      flex: 1;
      
      .stat-number {
        font-size: 36px;
        font-weight: 800;
        color: #1a1a1a;
        margin: 0 0 8px 0;
        letter-spacing: -1px;
      }
      
      .stat-label {
        color: #666;
        font-size: 16px;
        margin: 0 0 8px 0;
        font-weight: 600;
      }
      
      .stat-trend {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 14px;
        font-weight: 600;
        
        &.trend-up {
          color: #10b981;
        }
        
        &.trend-down {
          color: #ef4444;
        }
      }
    }
  }
}

.modules-section {
  padding: 60px 32px;
  background: rgba(255, 255, 255, 0.05);
  
  .modules-grid {
    max-width: 1800px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
  }
  
  .module-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 20px;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    &:hover {
      transform: translateY(-8px);
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
      background: white;
    }
    
    &.disabled {
      opacity: 0.6;
      cursor: not-allowed;
      background: rgba(255, 255, 255, 0.7);
      
      &::before {
        background: linear-gradient(90deg, #9ca3af 0%, #6b7280 100%);
      }
      
      &:hover {
        transform: none;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        background: rgba(255, 255, 255, 0.7);
      }
      
      .module-icon {
        &.disabled {
          background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%) !important;
        }
      }
      
      .module-content {
        h3 {
          color: #6b7280;
        }
        
        p {
          color: #9ca3af;
        }
      }
      
      .module-arrow {
        opacity: 0.5;
      }
    }
    
    .module-icon {
      width: 64px;
      height: 64px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: white;
      flex-shrink: 0;
      
      &.users {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }
      
      &.subjects {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      }
      
      &.user-subjects {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }
      
      &.questions {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }
      
      &.exams {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
      }
      
      &.question-bank {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
      }
      
      &.exam-creation {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
      }
      
      &.exam-analysis {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
      }
      
      &.permissions {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
      }
      
      &.import-export {
        background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
      }
      
      &.statistics {
        background: linear-gradient(135deg, #fad0c4 0%, #ffd1ff 100%);
      }
    }
    
    .module-content {
      flex: 1;
      
      h3 {
        font-size: 20px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0 0 8px 0;
        letter-spacing: -0.3px;
      }
      
      p {
        color: #666;
        font-size: 14px;
        line-height: 1.5;
        margin: 0;
        font-weight: 500;
      }
    }
    
    .module-arrow {
      color: #999;
      font-size: 16px;
      transition: all 0.3s ease;
    }
    
    &:hover .module-arrow {
      color: #667eea;
      transform: translateX(4px);
    }
  }
}

.quick-actions-section {
  padding: 60px 32px;
  
  .quick-actions-grid {
    max-width: 1800px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
  }
  
  .quick-action-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 20px;
    
    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }
    
    .action-icon {
      width: 56px;
      height: 56px;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      color: white;
      flex-shrink: 0;
      
      &.add-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }
      
      &.search {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }
      
      &.export {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
      }
    }
    
    .action-content {
      flex: 1;
      
      h4 {
        font-size: 18px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0 0 4px 0;
      }
      
      p {
        color: #666;
        font-size: 14px;
        margin: 0;
        font-weight: 500;
      }
    }
    
    .el-button {
      border-radius: 12px;
      font-weight: 600;
      padding: 10px 20px;
    }
  }
}

@media (max-width: 768px) {
  .modern-header .header-content {
    flex-direction: column;
    gap: 24px;
    text-align: center;
    
    .header-right {
      width: 100%;
      justify-content: center;
      flex-direction: column;
      gap: 16px;
    }
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
  }
  
  .modules-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
  }
  
  .quick-actions-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
  }
}
</style>
