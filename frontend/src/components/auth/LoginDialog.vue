<template>
  <el-dialog
    v-model="visible"
    title=""
    width="680px"
    :before-close="handleClose"
    center
    class="login-dialog"
    :show-close="false"
  >
    <div class="dialog-header">
      <div class="logo-section">
        <div class="logo-icon">
          <el-icon size="32"><User /></el-icon>
        </div>
        <h2>欢迎回来</h2>
        <p>登录您的账户以继续学习</p>
      </div>
    </div>
    
    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      label-width="0"
      @submit.prevent="handleLogin"
      class="login-form"
    >
      <el-form-item prop="username">
        <el-input
          v-model="loginForm.username"
          placeholder="请输入用户名"
          clearable
          size="large"
          prefix-icon="User"
        />
      </el-form-item>
      
      <el-form-item prop="password">
        <el-input
          v-model="loginForm.password"
          type="password"
          placeholder="请输入密码"
          show-password
          clearable
          size="large"
          prefix-icon="Lock"
        />
      </el-form-item>
      
      <el-form-item>
        <div class="form-options">
          <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
          <el-link type="primary" @click="handleForgotPassword">忘记密码？</el-link>
        </div>
      </el-form-item>
      
      <el-form-item>
        <el-button 
          type="primary" 
          @click="handleLogin" 
          :loading="loading"
          size="large"
          class="login-button"
        >
          {{ loading ? '登录中...' : '登录' }}
        </el-button>
      </el-form-item>
    </el-form>
    
    <div class="dialog-footer">
      <div class="divider">
        <span>还没有账号？</span>
      </div>
      <el-button type="text" @click="switchToRegister" class="register-link">
        立即注册
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
import { ref, reactive, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

export default {
  name: 'LoginDialog',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'switch-to-register'],
  setup(props, { emit }) {
    const authStore = useAuthStore()
    const loginFormRef = ref()
    const loading = ref(false)
    
    const visible = ref(props.modelValue)
    
    const loginForm = reactive({
      username: '',
      password: '',
      remember: false
    })
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
      ]
    }
    
    // 监听props变化
    watch(() => props.modelValue, (newVal) => {
      visible.value = newVal
    })
    
    // 监听visible变化
    watch(visible, (newVal) => {
      emit('update:modelValue', newVal)
    })
    
    const handleLogin = async () => {
      if (!loginFormRef.value) return
      
      try {
        await loginFormRef.value.validate()
        loading.value = true
        
        await authStore.loginAction({
          username: loginForm.username,
          password: loginForm.password
        })
        
        ElMessage.success('登录成功')
        handleClose()
      } catch (error) {
        console.error('登录失败:', error)
        ElMessage.error('登录失败，请检查用户名和密码')
      } finally {
        loading.value = false
      }
    }
    
    const handleClose = () => {
      visible.value = false
      // 重置表单
      loginForm.username = ''
      loginForm.password = ''
      loginForm.remember = false
      if (loginFormRef.value) {
        loginFormRef.value.resetFields()
      }
    }
    
    const switchToRegister = () => {
      handleClose()
      emit('switch-to-register')
    }
    
    const handleForgotPassword = () => {
      ElMessage.info('忘记密码功能开发中...')
    }
    
    return {
      visible,
      loginFormRef,
      loginForm,
      loginRules,
      loading,
      handleLogin,
      handleClose,
      switchToRegister,
      handleForgotPassword
    }
  }
}
</script>

<style lang="scss" scoped>
.login-dialog {
  :deep(.el-dialog) {
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  }
  
  :deep(.el-dialog__body) {
    padding: 0;
  }
}

.dialog-header {
  background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
  color: white;
  padding: 2rem;
  text-align: center;
  
  .logo-section {
    .logo-icon {
      width: 60px;
      height: 60px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 1rem;
      backdrop-filter: blur(10px);
    }
    
    h2 {
      font-size: 1.5rem;
      font-weight: bold;
      margin-bottom: 0.5rem;
    }
    
    p {
      opacity: 0.9;
      margin: 0;
    }
  }
}

.login-form {
  padding: 2rem;
  
  .el-form-item {
    margin-bottom: 1.5rem;
  }
  
  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }
  
  .login-button {
    width: 100%;
    height: 48px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
    border: none;
    
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
  }
}

.dialog-footer {
  padding: 0 2rem 2rem;
  text-align: center;
  
  .divider {
    position: relative;
    margin-bottom: 1rem;
    
    &::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      height: 1px;
      background: var(--theme-border, #e0e0e0);
    }
    
    span {
      background: white;
      padding: 0 1rem;
      color: var(--theme-textSecondary, #666);
      font-size: 14px;
    }
  }
  
  .register-link {
    color: var(--theme-primary, #667eea);
    font-weight: 600;
    font-size: 16px;
    
    &:hover {
      color: var(--theme-secondary, #764ba2);
    }
  }
}

// 输入框样式优化
:deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--theme-border, #e0e0e0);
  
  &:hover {
    border-color: var(--theme-primary, #667eea);
  }
  
  &.is-focus {
    border-color: var(--theme-primary, #667eea);
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
  }
}

:deep(.el-checkbox__label) {
  color: var(--theme-textSecondary, #666);
}

:deep(.el-link) {
  font-size: 14px;
}
</style>
