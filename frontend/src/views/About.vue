<template>
  <div class="about-page">
    <!-- 顶部导航栏 -->
    <TopNavigation />

    <!-- 关于我们内容 -->
    <div class="about-content">
      <div class="container">
        <!-- 面包屑导航 -->
        <el-breadcrumb separator="/" class="breadcrumb">
          <el-breadcrumb-item>
            <router-link to="/">首页</router-link>
          </el-breadcrumb-item>
          <el-breadcrumb-item>关于我们</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 页面标题 -->
        <div class="page-header">
          <h1>关于我们</h1>
          <p>了解ExamSphere在线考试平台</p>
        </div>

        <!-- 公司介绍 -->
        <div class="company-intro">
          <div class="intro-content">
            <h2>ExamSphere 在线考试平台</h2>
            <p class="intro-text">
              ExamSphere是一个专业的在线考试管理系统，为教育机构、企业培训和个人学习提供完整的在线考试解决方案。
              我们致力于通过先进的技术和优质的服务，让考试变得更加便捷、高效和公平。
            </p>
            
            <div class="intro-features">
              <div class="feature-item">
                <el-icon size="32"><Star /></el-icon>
                <h3>专业可靠</h3>
                <p>采用先进的技术架构，确保系统稳定可靠</p>
              </div>
              <div class="feature-item">
                <el-icon size="32"><User /></el-icon>
                <h3>用户友好</h3>
                <p>简洁直观的界面设计，操作简单易用</p>
              </div>
              <div class="feature-item">
                <el-icon size="32"><Shield /></el-icon>
                <h3>安全防护</h3>
                <p>多重安全机制，保障考试公平性</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 团队介绍 -->
        <div class="team-section">
          <h2>我们的团队</h2>
          <div class="team-grid">
            <div class="team-member">
              <el-avatar :size="80" src="/default-avatar.svg">张</el-avatar>
              <h3>张老师</h3>
              <p class="position">技术总监</p>
              <p class="description">10年教育技术经验，专注于在线教育平台开发</p>
            </div>
            <div class="team-member">
              <el-avatar :size="80" src="/default-avatar.svg">李</el-avatar>
              <h3>李老师</h3>
              <p class="position">产品经理</p>
              <p class="description">深度理解教育行业需求，致力于产品创新</p>
            </div>
            <div class="team-member">
              <el-avatar :size="80" src="/default-avatar.svg">王</el-avatar>
              <h3>王老师</h3>
              <p class="position">UI/UX设计师</p>
              <p class="description">专注于用户体验设计，创造美观易用的界面</p>
            </div>
          </div>
        </div>

        <!-- 联系我们 -->
        <div class="contact-section">
          <h2>联系我们</h2>
          <div class="contact-info">
            <div class="contact-item">
              <el-icon size="24"><Message /></el-icon>
              <div>
                <h4>邮箱</h4>
                <p>contact@examsphere.com</p>
              </div>
            </div>
            <div class="contact-item">
              <el-icon size="24"><Phone /></el-icon>
              <div>
                <h4>电话</h4>
                <p>400-123-4567</p>
              </div>
            </div>
            <div class="contact-item">
              <el-icon size="24"><Location /></el-icon>
              <div>
                <h4>地址</h4>
                <p>北京市海淀区中关村软件园</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TopNavigation from '@/components/layout/TopNavigation.vue'
import { Star, User, Shield, Message, Phone, Location } from '@element-plus/icons-vue'

export default {
  name: 'About',
  components: {
    TopNavigation,
    Star,
    User,
    Shield,
    Message,
    Phone,
    Location
  }
}
</script>

<style lang="scss" scoped>
.about-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumb {
  padding: 20px 0;
  
  :deep(.el-breadcrumb__item) {
    .el-breadcrumb__inner {
      color: #666;
      
      &:hover {
        color: #667eea;
      }
    }
    
    &:last-child .el-breadcrumb__inner {
      color: #333;
    }
  }
}

.about-content {
  padding-bottom: 4rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
  
  h1 {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #333;
  }
  
  p {
    font-size: 1.1rem;
    color: #666;
  }
}

.company-intro {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  margin-bottom: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  
  .intro-content {
    h2 {
      font-size: 2rem;
      font-weight: bold;
      margin-bottom: 1.5rem;
      color: #333;
      text-align: center;
    }
    
    .intro-text {
      font-size: 1.1rem;
      line-height: 1.8;
      color: #666;
      margin-bottom: 2rem;
      text-align: center;
    }
    
    .intro-features {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 2rem;
      margin-top: 2rem;
      
      .feature-item {
        text-align: center;
        padding: 1.5rem;
        border-radius: 8px;
        background: #f8f9fa;
        
        .el-icon {
          color: #667eea;
          margin-bottom: 1rem;
        }
        
        h3 {
          font-size: 1.2rem;
          font-weight: bold;
          margin-bottom: 0.5rem;
          color: #333;
        }
        
        p {
          color: #666;
          line-height: 1.5;
        }
      }
    }
  }
}

.team-section {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  margin-bottom: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  
  h2 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 2rem;
    color: #333;
    text-align: center;
  }
  
  .team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    
    .team-member {
      text-align: center;
      padding: 1.5rem;
      border-radius: 8px;
      background: #f8f9fa;
      
      h3 {
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
        color: #333;
      }
      
      .position {
        color: #667eea;
        font-weight: 500;
        margin-bottom: 1rem;
      }
      
      .description {
        color: #666;
        line-height: 1.5;
        font-size: 0.9rem;
      }
    }
  }
}

.contact-section {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  
  h2 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 2rem;
    color: #333;
    text-align: center;
  }
  
  .contact-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    
    .contact-item {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1.5rem;
      border-radius: 8px;
      background: #f8f9fa;
      
      .el-icon {
        color: #667eea;
        flex-shrink: 0;
      }
      
      h4 {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #333;
      }
      
      p {
        color: #666;
        margin: 0;
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .company-intro,
  .team-section,
  .contact-section {
    padding: 2rem 1.5rem;
  }
  
  .intro-features,
  .team-grid,
  .contact-info {
    grid-template-columns: 1fr;
  }
}
</style>
