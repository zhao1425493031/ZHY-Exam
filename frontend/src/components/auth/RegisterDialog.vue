<template>
  <el-dialog
    v-model="visible"
    title=""
    width="680px"
    :before-close="handleClose"
    center
    class="register-dialog"
    :show-close="false"
  >
    <div class="dialog-header">
      <div class="logo-section">
        <div class="logo-icon">
          <el-icon size="32"><UserFilled /></el-icon>
        </div>
        <h2>创建账户</h2>
        <p>加入我们，开始您的学习之旅</p>
      </div>
    </div>
    
    <el-form
      ref="registerFormRef"
      :model="registerForm"
      :rules="registerRules"
      label-width="0"
      @submit.prevent="handleRegister"
      class="register-form"
    >
      <div class="form-row">
        <el-form-item prop="username" class="form-item-half">
          <el-input
            v-model="registerForm.username"
            placeholder="用户名"
            clearable
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="email" class="form-item-half">
          <el-input
            v-model="registerForm.email"
            placeholder="邮箱"
            clearable
            size="large"
            prefix-icon="Message"
          />
        </el-form-item>
      </div>
      
      <div class="form-row">
        <el-form-item prop="password" class="form-item-half">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="密码"
            show-password
            clearable
            size="large"
            prefix-icon="Lock"
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword" class="form-item-half">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="确认密码"
            show-password
            clearable
            size="large"
            prefix-icon="Lock"
          />
        </el-form-item>
      </div>
      
      <el-form-item prop="real_name">
        <el-input
          v-model="registerForm.real_name"
          placeholder="真实姓名"
          clearable
          size="large"
          prefix-icon="User"
        />
      </el-form-item>
      
      <el-form-item prop="agree">
        <div class="agreement-section">
          <el-checkbox v-model="registerForm.agree">
            我已阅读并同意
            <el-link type="primary" @click="showTerms">《用户协议》</el-link>
            和
            <el-link type="primary" @click="showPrivacy">《隐私政策》</el-link>
          </el-checkbox>
        </div>
      </el-form-item>
      
      <el-form-item>
        <el-button 
          type="primary" 
          @click="handleRegister" 
          :loading="loading"
          size="large"
          class="register-button"
        >
          {{ loading ? '注册中...' : '创建账户' }}
        </el-button>
      </el-form-item>
    </el-form>
    
    <div class="dialog-footer">
      <div class="divider">
        <span>已有账号？</span>
      </div>
      <el-button type="text" @click="switchToLogin" class="login-link">
        立即登录
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
import { ref, reactive, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

export default {
  name: 'RegisterDialog',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'switch-to-login'],
  setup(props, { emit }) {
    const authStore = useAuthStore()
    const registerFormRef = ref()
    const loading = ref(false)
    
    const visible = ref(props.modelValue)
    
    const registerForm = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      real_name: '',
      agree: false
    })
    
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    const validateAgree = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请阅读并同意用户协议和隐私政策'))
      } else {
        callback()
      }
    }
    
    const registerRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
        { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字、下划线', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        { validator: validateConfirmPassword, trigger: 'blur' }
      ],
      real_name: [
        { max: 50, message: '真实姓名长度不能超过 50 个字符', trigger: 'blur' }
      ],
      agree: [
        { validator: validateAgree, trigger: 'change' }
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
    
    const handleRegister = async () => {
      if (!registerFormRef.value) return
      
      try {
        await registerFormRef.value.validate()
        loading.value = true
        
        await authStore.registerAction({
          username: registerForm.username,
          email: registerForm.email,
          password: registerForm.password,
          real_name: registerForm.real_name
        })
        
        ElMessage.success('注册成功')
        handleClose()
      } catch (error) {
        console.error('注册失败:', error)
        ElMessage.error('注册失败，请检查输入信息')
      } finally {
        loading.value = false
      }
    }
    
    const handleClose = () => {
      visible.value = false
      // 重置表单
      Object.keys(registerForm).forEach(key => {
        if (typeof registerForm[key] === 'boolean') {
          registerForm[key] = false
        } else {
          registerForm[key] = ''
        }
      })
      if (registerFormRef.value) {
        registerFormRef.value.resetFields()
      }
    }
    
    const switchToLogin = () => {
      handleClose()
      emit('switch-to-login')
    }
    
    const showTerms = () => {
      ElMessage.info('用户协议页面开发中...')
    }
    
    const showPrivacy = () => {
      ElMessage.info('隐私政策页面开发中...')
    }
    
    return {
      visible,
      registerFormRef,
      registerForm,
      registerRules,
      loading,
      handleRegister,
      handleClose,
      switchToLogin,
      showTerms,
      showPrivacy
    }
  }
}
</script>

<style lang="scss" scoped>
.register-dialog {
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

.register-form {
  padding: 2rem;
  
  .form-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    
    .form-item-half {
      flex: 1;
      margin-bottom: 0;
    }
  }
  
  .agreement-section {
    text-align: left;
    font-size: 14px;
    line-height: 1.5;
  }
  
  .register-button {
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
  
  .login-link {
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

// 响应式设计
@media (max-width: 480px) {
  .register-form {
    .form-row {
      flex-direction: column;
      gap: 0;
      
      .form-item-half {
        margin-bottom: 1rem;
      }
    }
  }
}
</style>
