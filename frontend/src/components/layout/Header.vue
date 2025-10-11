<template>
  <div class="header">
    <div class="header-left">
      <el-button 
        type="text" 
        @click="toggleSidebar"
        class="sidebar-toggle"
      >
        <el-icon><Fold v-if="!sidebarCollapsed" /><Expand v-else /></el-icon>
      </el-button>
      
      <div class="logo">
        <h1>ExamSphere</h1>
      </div>
    </div>
    
    <div class="header-right">
      <!-- 通知 -->
      <el-badge :value="unreadCount" :hidden="unreadCount === 0">
        <el-button type="text" @click="showNotifications">
          <el-icon><Bell /></el-icon>
        </el-button>
      </el-badge>
      
      <!-- 用户菜单 -->
      <el-dropdown @command="handleCommand">
        <div class="user-info">
          <el-avatar :size="32" :src="userAvatar">
            {{ userRealName?.charAt(0) }}
          </el-avatar>
          <span class="username">{{ userRealName }}</span>
          <el-icon><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">
              <el-icon><User /></el-icon>
              个人资料
            </el-dropdown-item>
            <el-dropdown-item command="settings">
              <el-icon><Setting /></el-icon>
              系统设置
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
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessageBox } from 'element-plus'

export default {
  name: 'Header',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // 计算属性
    const userRealName = computed(() => authStore.user?.real_name || '用户')
    const userAvatar = computed(() => authStore.user?.avatar_url || '')
    const sidebarCollapsed = computed(() => false) // TODO: 从状态管理中获取
    const unreadCount = computed(() => 0) // TODO: 从状态管理中获取
    
    // 切换侧边栏
    const toggleSidebar = () => {
      // TODO: 实现侧边栏切换逻辑
      console.log('切换侧边栏')
    }
    
    // 显示通知
    const showNotifications = () => {
      // TODO: 实现通知显示逻辑
      console.log('显示通知')
    }
    
    // 处理用户菜单命令
    const handleCommand = async (command) => {
      switch (command) {
        case 'profile':
          router.push('/profile')
          break
        case 'settings':
          router.push('/settings')
          break
        case 'logout':
          try {
            await ElMessageBox.confirm(
              '确定要退出登录吗？',
              '提示',
              {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }
            )
            await authStore.logoutAction()
            // 退出后跳转到首页
            router.push('/')
          } catch (error) {
            // 用户取消
          }
          break
      }
    }
    
    return {
      userRealName,
      userAvatar,
      sidebarCollapsed,
      unreadCount,
      toggleSidebar,
      showNotifications,
      handleCommand
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 100%;
  
  .header-left {
    display: flex;
    align-items: center;
    
    .sidebar-toggle {
      margin-right: 20px;
      font-size: 18px;
    }
    
    .logo {
      h1 {
        font-size: 20px;
        font-weight: 600;
        color: #409EFF;
        margin: 0;
      }
    }
  }
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 20px;
    
    .user-info {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      padding: 8px 12px;
      border-radius: 4px;
      transition: background-color 0.3s;
      
      &:hover {
        background-color: #f5f7fa;
      }
      
      .username {
        font-size: 14px;
        color: #606266;
      }
    }
  }
}
</style>
