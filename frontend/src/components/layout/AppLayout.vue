<template>
  <div class="app-layout">
    <el-container>
      <!-- 顶部导航栏 - 只在这里定义 -->
      <el-header class="header">
        <Header />
      </el-header>
      
      <el-container>
        <!-- 侧边栏 - 只在这里定义 -->
        <el-aside class="sidebar">
          <Sidebar />
        </el-aside>
        
        <!-- 主内容区域 -->
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from './Header.vue'
import Sidebar from './Sidebar.vue'

export default {
  name: 'AppLayout',
  components: {
    Header,
    Sidebar
  }
}
</script>

<style lang="scss" scoped>
.app-layout {
  height: 100vh;
  
  .header {
    background-color: #fff;
    border-bottom: 1px solid #e4e7ed;
    padding: 0;
    height: 60px;
    line-height: 60px;
  }
  
  .sidebar {
    width: 200px;
    background-color: #304156;
    transition: width 0.3s;
    
    &.collapsed {
      width: 64px;
    }
  }
  
  .main-content {
    background-color: #f2f3f5;
    padding: 20px;
    overflow-y: auto;
  }
}
</style>
