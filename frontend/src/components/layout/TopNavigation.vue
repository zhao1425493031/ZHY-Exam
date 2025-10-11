<template>
  <div class="top-navigation">
    <div class="nav-container">
      <!-- 左侧Logo和品牌 -->
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <h1>ExamSphere</h1>
          <span class="brand-subtitle">在线考试平台</span>
        </router-link>
      </div>

      <!-- 中间导航菜单 -->
      <nav class="nav-menu">
        <el-menu
          mode="horizontal"
          :default-active="activeMenu"
          class="nav-menu-items"
          @select="handleMenuSelect"
        >
          <el-menu-item index="home">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          
          <el-sub-menu index="courses">
            <template #title>
              <el-icon><Reading /></el-icon>
              <span>课程学习</span>
            </template>
            <el-menu-item index="courses-all">全部课程</el-menu-item>
            <el-menu-item index="courses-free">免费课程</el-menu-item>
            <el-menu-item index="courses-paid">付费课程</el-menu-item>
            <el-menu-item index="courses-programming">编程开发</el-menu-item>
            <el-menu-item index="courses-design">设计创意</el-menu-item>
            <el-menu-item index="courses-business">商业管理</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="exams">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>在线考试</span>
            </template>
            <el-menu-item index="exams-available">可参加考试</el-menu-item>
            <el-menu-item index="exams-history">考试历史</el-menu-item>
            <el-menu-item index="exams-results">成绩查询</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="features">
            <el-icon><Star /></el-icon>
            <span>功能特色</span>
          </el-menu-item>

          <el-menu-item index="about">
            <el-icon><InfoFilled /></el-icon>
            <span>关于我们</span>
          </el-menu-item>
        </el-menu>
      </nav>

      <!-- 右侧用户区域 -->
      <div class="nav-user">
        <!-- 未登录状态 -->
        <div v-if="!authStore.isLoggedIn" class="user-actions">
          <ThemeSwitcher />
          <el-button type="primary" @click="showLoginDialog">登录</el-button>
          <el-button @click="showRegisterDialog">注册</el-button>
        </div>

        <!-- 已登录状态 -->
        <div v-else class="user-info">
          <!-- 消息通知 -->
          <el-badge :value="unreadCount" :hidden="unreadCount === 0" class="notification-badge">
            <el-button circle @click="toggleNotification">
              <el-icon><Bell /></el-icon>
            </el-button>
          </el-badge>

          <!-- 用户头像和下拉菜单 -->
          <el-dropdown @command="handleUserCommand" trigger="click">
            <div class="user-avatar">
              <el-avatar :src="authStore.user?.avatar_url" :size="32">
                {{ authStore.user?.username?.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ authStore.user?.username }}</span>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="dashboard">
                  <el-icon><Monitor /></el-icon>
                  我的仪表盘
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- 通知面板 -->
    <div v-if="showNotification" class="notification-panel" @click.stop>
      <div class="notification-header">
        <h4>消息通知</h4>
        <el-button type="text" @click="markAllRead">全部已读</el-button>
      </div>
      <div class="notification-list">
        <div v-if="notifications.length === 0" class="no-notifications">
          <el-empty description="暂无消息" :image-size="80" />
        </div>
        <div v-else>
          <div 
            v-for="notification in notifications" 
            :key="notification.id"
            class="notification-item"
            :class="{ unread: !notification.is_read }"
            @click="markAsRead(notification.id)"
          >
            <div class="notification-content">
              <h5>{{ notification.title }}</h5>
              <p>{{ notification.content }}</p>
              <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 登录弹窗 -->
    <LoginDialog 
      v-model="loginDialogVisible" 
      @switch-to-register="switchToRegister" 
    />
    
    <!-- 注册弹窗 -->
    <RegisterDialog 
      v-model="registerDialogVisible" 
      @switch-to-login="switchToLogin" 
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  House, Reading, Star, InfoFilled, Bell, ArrowDown, User, 
  Monitor, SwitchButton, Document 
} from '@element-plus/icons-vue'
import LoginDialog from '@/components/auth/LoginDialog.vue'
import RegisterDialog from '@/components/auth/RegisterDialog.vue'
import ThemeSwitcher from '@/components/common/ThemeSwitcher.vue'

export default {
  name: 'TopNavigation',
  components: {
    House,
    Reading,
    Star,
    InfoFilled,
    Bell,
    ArrowDown,
    User,
    Monitor,
    SwitchButton,
    Document,
    LoginDialog,
    RegisterDialog,
    ThemeSwitcher
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    const showNotification = ref(false)
    const notifications = ref([])
    const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)
    
    // 弹窗相关
    const loginDialogVisible = ref(false)
    const registerDialogVisible = ref(false)

    // 当前激活的菜单
    const activeMenu = computed(() => {
      const path = route.path
      if (path === '/') return 'home'
      if (path.startsWith('/courses')) return 'courses'
      if (path.startsWith('/features')) return 'features'
      if (path.startsWith('/about')) return 'about'
      return ''
    })

    // 获取通知列表
    const fetchNotifications = async () => {
      if (!authStore.isLoggedIn) return
      
      try {
        // 这里应该调用API获取通知
        // const response = await notificationApi.getNotifications()
        // notifications.value = response.data.items || []
        
        // 暂时使用模拟数据
        notifications.value = [
          {
            id: 1,
            title: '新课程上线',
            content: '《Vue.js 3.0 实战开发》课程已上线，欢迎学习！',
            is_read: false,
            created_at: '2024-01-15T10:30:00Z'
          },
          {
            id: 2,
            title: '考试提醒',
            content: '您有一个考试将在明天开始，请做好准备。',
            is_read: true,
            created_at: '2024-01-14T15:20:00Z'
          }
        ]
      } catch (error) {
        console.error('获取通知失败:', error)
      }
    }

    // 切换通知面板
    const toggleNotification = () => {
      showNotification.value = !showNotification.value
      if (showNotification.value) {
        fetchNotifications()
      }
    }

    // 标记为已读
    const markAsRead = async (notificationId) => {
      try {
        // 这里应该调用API标记已读
        // await notificationApi.markAsRead(notificationId)
        
        const notification = notifications.value.find(n => n.id === notificationId)
        if (notification) {
          notification.is_read = true
        }
      } catch (error) {
        console.error('标记已读失败:', error)
      }
    }

    // 全部已读
    const markAllRead = async () => {
      try {
        // 这里应该调用API全部已读
        // await notificationApi.markAllRead()
        
        notifications.value.forEach(n => n.is_read = true)
      } catch (error) {
        console.error('全部已读失败:', error)
      }
    }

    // 格式化时间
    const formatTime = (timeStr) => {
      const time = new Date(timeStr)
      const now = new Date()
      const diff = now - time
      
      if (diff < 60000) return '刚刚'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
      return `${Math.floor(diff / 86400000)}天前`
    }

    // 菜单选择处理
    const handleMenuSelect = (index) => {
      switch (index) {
        case 'home':
          router.push('/')
          break
        case 'courses-all':
          router.push('/courses')
          break
        case 'courses-free':
          router.push('/courses?type=free')
          break
        case 'courses-paid':
          router.push('/courses?type=paid')
          break
        case 'courses-programming':
          router.push('/courses?category=programming')
          break
        case 'courses-design':
          router.push('/courses?category=design')
          break
        case 'courses-business':
          router.push('/courses?category=business')
          break
        case 'exams-available':
          router.push('/#exams')
          break
        case 'exams-history':
          router.push('/user/dashboard')
          break
        case 'exams-results':
          router.push('/user/dashboard')
          break
        case 'features':
          router.push('/#features')
          break
        case 'about':
          router.push('/about')
          break
      }
    }

    // 用户命令处理
    const handleUserCommand = (command) => {
      switch (command) {
        case 'profile':
        case 'dashboard':
          router.push('/user/dashboard')
          break
        case 'logout':
          handleLogout()
          break
      }
    }
    
    // 弹窗相关方法
    const showLoginDialog = () => {
      loginDialogVisible.value = true
    }
    
    const showRegisterDialog = () => {
      registerDialogVisible.value = true
    }
    
    const switchToRegister = () => {
      loginDialogVisible.value = false
      registerDialogVisible.value = true
    }
    
    const switchToLogin = () => {
      registerDialogVisible.value = false
      loginDialogVisible.value = true
    }

    // 退出登录
    const handleLogout = async () => {
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await authStore.logoutAction()
        ElMessage.success('退出登录成功')
        router.push('/')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('退出登录失败:', error)
          ElMessage.error('退出登录失败')
        }
      }
    }

    // 显示登录弹窗
    const goToLogin = () => {
      authStore.openLoginDialog()
    }

    // 显示注册弹窗（通过登录弹窗切换）
    const goToRegister = () => {
      authStore.openLoginDialog()
    }

    // 点击外部关闭通知面板
    const handleClickOutside = (event) => {
      if (!event.target.closest('.notification-panel') && !event.target.closest('.notification-badge')) {
        showNotification.value = false
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
      if (authStore.isLoggedIn) {
        fetchNotifications()
      }
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      authStore,
      showNotification,
      notifications,
      unreadCount,
      activeMenu,
      toggleNotification,
      markAsRead,
      markAllRead,
      formatTime,
      handleMenuSelect,
      handleUserCommand,
      goToLogin,
      goToRegister,
      loginDialogVisible,
      registerDialogVisible,
      showLoginDialog,
      showRegisterDialog,
      switchToRegister,
      switchToLogin
    }
  }
}
</script>

<style lang="scss" scoped>
.top-navigation {
  position: relative;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
}

// 品牌区域
.nav-brand {
  .brand-link {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: #333;

    h1 {
      font-size: 1.8rem;
      font-weight: bold;
      margin: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .brand-subtitle {
      font-size: 0.8rem;
      color: #666;
      margin-left: 8px;
    }
  }
}

// 导航菜单
.nav-menu {
  flex: 1;
  display: flex;
  justify-content: center;

  .nav-menu-items {
    border: none;
    background: transparent;

    :deep(.el-menu-item) {
      height: 60px;
      line-height: 60px;
      border-bottom: none;
      
      &:hover {
        background-color: #f5f7fa;
        color: #667eea;
      }

      &.is-active {
        background-color: #f0f2ff;
        color: #667eea;
        border-bottom: 2px solid #667eea;
      }
    }

    :deep(.el-sub-menu) {
      .el-sub-menu__title {
        height: 60px;
        line-height: 60px;
        border-bottom: none;

        &:hover {
          background-color: #f5f7fa;
          color: #667eea;
        }
      }
    }
  }
}

// 用户区域
.nav-user {
  display: flex;
  align-items: center;
  gap: 16px;

  .user-actions {
    display: flex;
    gap: 8px;
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;

    .notification-badge {
      :deep(.el-badge__content) {
        background-color: #f56c6c;
      }
    }

    .user-avatar {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 20px;
      transition: background-color 0.3s;

      &:hover {
        background-color: #f5f7fa;
      }

      .username {
        font-size: 14px;
        color: #333;
        font-weight: 500;
      }

      .dropdown-icon {
        font-size: 12px;
        color: #999;
      }
    }
  }
}

// 通知面板
.notification-panel {
  position: absolute;
  top: 100%;
  right: 20px;
  width: 350px;
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1001;

  .notification-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid #e4e7ed;

    h4 {
      margin: 0;
      font-size: 16px;
      color: #333;
    }
  }

  .notification-list {
    max-height: 400px;
    overflow-y: auto;

    .no-notifications {
      padding: 20px;
      text-align: center;
    }

    .notification-item {
      padding: 16px 20px;
      border-bottom: 1px solid #f0f0f0;
      cursor: pointer;
      transition: background-color 0.3s;

      &:hover {
        background-color: #f8f9fa;
      }

      &.unread {
        background-color: #f0f2ff;
        border-left: 3px solid #667eea;
      }

      &:last-child {
        border-bottom: none;
      }

      .notification-content {
        h5 {
          margin: 0 0 8px 0;
          font-size: 14px;
          color: #333;
          font-weight: 500;
        }

        p {
          margin: 0 0 8px 0;
          font-size: 13px;
          color: #666;
          line-height: 1.4;
        }

        .notification-time {
          font-size: 12px;
          color: #999;
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .nav-container {
    padding: 0 16px;
  }

  .nav-menu {
    display: none;
  }

  .nav-brand h1 {
    font-size: 1.5rem;
  }

  .brand-subtitle {
    display: none;
  }

  .notification-panel {
    right: 16px;
    width: 300px;
  }
}
</style>
