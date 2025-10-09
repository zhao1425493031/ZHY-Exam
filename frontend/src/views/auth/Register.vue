<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-form">
        <div class="register-header">
          <h1>ExamSphere</h1>
          <p>考试管理系统</p>
        </div>
        
        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          class="register-form-content"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          
          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱"
              size="large"
              prefix-icon="Message"
            />
          </el-form-item>
          
          <el-form-item prop="realName">
            <el-input
              v-model="registerForm.realName"
              placeholder="请输入真实姓名"
              size="large"
              prefix-icon="UserFilled"
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请确认密码"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <el-form-item prop="role">
            <el-select
              v-model="registerForm.role"
              placeholder="请选择角色"
              size="large"
              style="width: 100%"
            >
              <el-option label="普通用户" value="user" />
            </el-select>
          </el-form-item>
          
          <el-form-item>
            <el-link type="primary" @click="$router.push('/login')">
              已有账号？立即登录
            </el-link>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="register-button"
              :loading="loading"
              @click="handleRegister"
            >
              注册
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
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // 表单引用
    const registerFormRef = ref()
    
    // 加载状态
    const loading = ref(false)
    
    // 表单数据
    const registerForm = reactive({
      username: '',
      email: '',
      realName: '',
      password: '',
      confirmPassword: '',
      role: 'user'
    })
    
    // 表单验证规则
    const registerRules = {
      username: commonRules.username,
      email: commonRules.email,
      realName: commonRules.realName,
      password: commonRules.password,
      confirmPassword: [
        ...commonRules.password,
        {
          validator: (rule, value, callback) => {
            if (value !== registerForm.password) {
              callback(new Error('两次输入的密码不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ]
    }
    
    // 处理注册
    const handleRegister = async () => {
      if (!registerFormRef.value) return
      
      try {
        const valid = await registerFormRef.value.validate()
        if (!valid) return
        
        loading.value = true
        
        await authStore.registerAction({
          username: registerForm.username,
          email: registerForm.email,
          real_name: registerForm.realName,
          password: registerForm.password,
          role: registerForm.role
        })
        
        // 注册成功，跳转到登录页面
        router.push('/login')
      } catch (error) {
        console.error('注册失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    return {
      registerFormRef,
      registerForm,
      registerRules,
      loading,
      handleRegister
    }
  }
}
</script>

<style lang="scss" scoped>
.register-page {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  
  .register-container {
    width: 100%;
    max-width: 450px;
    
    .register-form {
      background: #fff;
      border-radius: 12px;
      padding: 40px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
      
      .register-header {
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
      
      .register-form-content {
        .register-button {
          width: 100%;
          height: 45px;
          font-size: 16px;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .register-page {
    .register-container {
      .register-form {
        padding: 30px 20px;
      }
    }
  }
}
</style>
