<template>
  <div id="app">
    <router-view />
    
    <!-- 全局登录弹窗 -->
    <LoginDialog 
      v-model="authStore.showLoginDialog" 
      @login-success="handleLoginSuccess"
    />
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import LoginDialog from '@/components/auth/LoginDialog.vue'

export default {
  name: 'App',
  components: {
    LoginDialog
  },
  setup() {
    const authStore = useAuthStore()

    // 初始化用户状态
    onMounted(() => {
      authStore.initUser()
    })

    // 登录成功处理
    const handleLoginSuccess = () => {
      authStore.closeLoginDialog()
    }

    return {
      authStore,
      handleLoginSuccess
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}
</style>
