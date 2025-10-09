<template>
  <div class="not-found">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <div class="error-message">页面未找到</div>
      <div class="error-description">
        抱歉，您访问的页面不存在或已被删除
      </div>
      <div class="error-actions">
        <el-button type="primary" @click="goHome">
          返回首页
        </el-button>
        <el-button @click="goBack">
          返回上页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'NotFound',
  setup() {
    const router = useRouter()
    
    const goHome = () => {
      router.push('/dashboard')
    }
    
    const goBack = () => {
      router.go(-1)
    }
    
    return {
      goHome,
      goBack
    }
  }
}
</script>

<style lang="scss" scoped>
.not-found {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  
  .not-found-content {
    text-align: center;
    color: #fff;
    
    .error-code {
      font-size: 120px;
      font-weight: 700;
      margin-bottom: 20px;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .error-message {
      font-size: 32px;
      font-weight: 600;
      margin-bottom: 16px;
    }
    
    .error-description {
      font-size: 16px;
      margin-bottom: 40px;
      opacity: 0.8;
    }
    
    .error-actions {
      .el-button {
        margin: 0 10px;
        padding: 12px 24px;
        font-size: 16px;
      }
    }
  }
}

@media (max-width: 768px) {
  .not-found {
    .not-found-content {
      .error-code {
        font-size: 80px;
      }
      
      .error-message {
        font-size: 24px;
      }
      
      .error-description {
        font-size: 14px;
      }
    }
  }
}
</style>
