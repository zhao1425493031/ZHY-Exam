<template>
  <div class="sidebar">
    <el-menu
      :default-active="activeMenu"
      :collapse="collapsed"
      :unique-opened="true"
      router
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
      <!-- 仪表盘 -->
      <el-menu-item index="/dashboard">
        <el-icon><Odometer /></el-icon>
        <template #title>仪表盘</template>
      </el-menu-item>
      
      <!-- 管理员菜单 -->
      <template v-if="isAdmin">
        <el-sub-menu index="admin">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/admin/users">用户管理</el-menu-item>
          <el-menu-item index="/admin/subjects">科目管理</el-menu-item>
          <el-menu-item index="/admin/questions">试题管理</el-menu-item>
          <el-menu-item index="/admin/exams">考试管理</el-menu-item>
          <el-menu-item index="/admin/question-bank">题库管理</el-menu-item>
          <el-menu-item index="/admin/exam-creation">创建考试</el-menu-item>
          <el-menu-item index="/admin/exam-analysis">考试分析</el-menu-item>
        </el-sub-menu>
      </template>
      
      <!-- 用户菜单 -->
      <template v-if="isUser">
        <el-sub-menu index="user">
          <template #title>
            <el-icon><Reading /></el-icon>
            <span>用户中心</span>
          </template>
          <el-menu-item index="/user/exam-list">考试列表</el-menu-item>
          <el-menu-item index="/user/my-records">我的记录</el-menu-item>
        </el-sub-menu>
      </template>
      
      <!-- 通用菜单 -->
      <el-menu-item index="/profile">
        <el-icon><User /></el-icon>
        <template #title>个人资料</template>
      </el-menu-item>
      
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <template #title>系统设置</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Sidebar',
  setup() {
    const route = useRoute()
    const authStore = useAuthStore()
    
    // 计算属性
    const activeMenu = computed(() => route.path)
    const collapsed = computed(() => false) // TODO: 从状态管理中获取
    const isAdmin = computed(() => authStore.isAdmin)
    const isUser = computed(() => authStore.isUser)
    
    return {
      activeMenu,
      collapsed,
      isAdmin,
      isUser
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebar {
  height: 100%;
  
  .el-menu {
    border-right: none;
    height: 100%;
    
    .el-menu-item {
      &:hover {
        background-color: #263445 !important;
      }
      
      &.is-active {
        background-color: #409EFF !important;
        color: #fff !important;
      }
    }
    
    .el-sub-menu {
      .el-sub-menu__title:hover {
        background-color: #263445 !important;
      }
    }
  }
}
</style>
