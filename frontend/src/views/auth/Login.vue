<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-form">
        <div class="login-header">
          <h1>ExamSphere</h1>
          <p>考试管理系统</p>
        </div>
        
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form-content"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              prefix-icon="Lock"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          
          <el-form-item>
            <div class="login-options">
              <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
              <el-link type="primary" @click="$router.push('/register')">
                还没有账号？立即注册
              </el-link>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-button"
              :loading="loading"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { commonRules } from '@/utils/validation'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // 表单引用
    const loginFormRef = ref()
    
    // 加载状态
    const loading = ref(false)
    
    // 表单数据
    const loginForm = reactive({
      username: '',
      password: '',
      remember: false
    })
    
    // 表单验证规则
    const loginRules = {
      username: commonRules.username,
      password: commonRules.password
    }
    
    // 处理登录
    const handleLogin = async () => {
      if (!loginFormRef.value) return
      
      try {
        const valid = await loginFormRef.value.validate()
        if (!valid) return
        
        loading.value = true
        
        await authStore.loginAction({
          username: loginForm.username,
          password: loginForm.password
        })
        
        // 登录成功，跳转到仪表盘
        router.push('/dashboard')
      } catch (error) {
        console.error('登录失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    return {
      loginFormRef,
      loginForm,
      loginRules,
      loading,
      handleLogin
    }
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  
  .login-container {
    width: 400px;
    
    .login-form {
      background: #fff;
      border-radius: 12px;
      padding: 40px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
      
      .login-header {
        text-align: center;
        margin-bottom: 30px;
        
        h1 {
          font-size: 28px;
          font-weight: 600;
          color: #409EFF;
          margin-bottom: 8px;
        }
        
        p {
          color: #909399;
          font-size: 14px;
        }
      }
      
      .login-form-content {
        .login-options {
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
        }
        
        .login-button {
          width: 100%;
          height: 45px;
          font-size: 16px;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .login-page {
    .login-container {
      width: 90%;
      
      .login-form {
        padding: 30px 20px;
      }
    }
  }
}
</style>

