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
          <div class="header-badge">
            <el-icon><Star /></el-icon>
            <span>专业可信赖</span>
          </div>
          <h1>关于我们</h1>
          <p>了解ExamSphere在线考试平台，探索我们的使命与愿景</p>
          <div class="header-stats">
            <div class="stat-item">
              <div class="stat-number">10K+</div>
              <div class="stat-label">用户</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">500+</div>
              <div class="stat-label">课程</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">99%</div>
              <div class="stat-label">满意度</div>
            </div>
          </div>
        </div>

        <!-- 公司介绍 -->
        <div class="company-intro">
          <div class="intro-content">
            <div class="intro-header">
              <h2>ExamSphere 在线考试平台</h2>
              <div class="intro-subtitle">让学习更高效，让考试更公平</div>
            </div>
            <p class="intro-text">
              ExamSphere是一个专业的在线考试管理系统，为教育机构、企业培训和个人学习提供完整的在线考试解决方案。
              我们致力于通过先进的技术和优质的服务，让考试变得更加便捷、高效和公平。
            </p>
            
            <div class="intro-features">
              <div class="feature-item">
                <div class="feature-icon">
                  <el-icon size="32"><Star /></el-icon>
                </div>
                <h3>专业可靠</h3>
                <p>采用先进的技术架构，确保系统稳定可靠</p>
              </div>
              <div class="feature-item">
                <div class="feature-icon">
                  <el-icon size="32"><User /></el-icon>
                </div>
                <h3>用户友好</h3>
                <p>简洁直观的界面设计，操作简单易用</p>
              </div>
              <div class="feature-item">
                <div class="feature-icon">
                  <el-icon size="32"><Shield /></el-icon>
                </div>
                <h3>安全防护</h3>
                <p>多重安全机制，保障考试公平性</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 团队介绍 -->
        <div class="team-section">
          <div class="section-header">
            <h2>我们的团队</h2>
            <p>专业团队，用心服务</p>
          </div>
          <div class="team-grid">
            <div class="team-member">
              <div class="member-avatar">
                <el-avatar :size="100" src="/default-avatar.svg">张</el-avatar>
                <div class="avatar-ring"></div>
              </div>
              <h3>张老师</h3>
              <p class="position">技术总监</p>
              <p class="description">10年教育技术经验，专注于在线教育平台开发</p>
              <div class="member-social">
                <el-icon><Message /></el-icon>
                <el-icon><Phone /></el-icon>
              </div>
            </div>
            <div class="team-member">
              <div class="member-avatar">
                <el-avatar :size="100" src="/default-avatar.svg">李</el-avatar>
                <div class="avatar-ring"></div>
              </div>
              <h3>李老师</h3>
              <p class="position">产品经理</p>
              <p class="description">深度理解教育行业需求，致力于产品创新</p>
              <div class="member-social">
                <el-icon><Message /></el-icon>
                <el-icon><Phone /></el-icon>
              </div>
            </div>
            <div class="team-member">
              <div class="member-avatar">
                <el-avatar :size="100" src="/default-avatar.svg">王</el-avatar>
                <div class="avatar-ring"></div>
              </div>
              <h3>王老师</h3>
              <p class="position">UI/UX设计师</p>
              <p class="description">专注于用户体验设计，创造美观易用的界面</p>
              <div class="member-social">
                <el-icon><Message /></el-icon>
                <el-icon><Phone /></el-icon>
              </div>
            </div>
          </div>
        </div>

        <!-- 联系我们 -->
        <div class="contact-section">
          <div class="section-header">
            <h2>联系我们</h2>
            <p>随时为您提供专业服务</p>
          </div>
          <div class="contact-info">
            <div class="contact-item">
              <div class="contact-icon">
                <el-icon size="28"><Message /></el-icon>
              </div>
              <div class="contact-content">
                <h4>邮箱</h4>
                <p>contact@examsphere.com</p>
                <span class="contact-desc">24小时内回复</span>
              </div>
            </div>
            <div class="contact-item">
              <div class="contact-icon">
                <el-icon size="28"><Phone /></el-icon>
              </div>
              <div class="contact-content">
                <h4>电话</h4>
                <p>400-123-4567</p>
                <span class="contact-desc">工作日 9:00-18:00</span>
              </div>
            </div>
            <div class="contact-item">
              <div class="contact-icon">
                <el-icon size="28"><Location /></el-icon>
              </div>
              <div class="contact-content">
                <h4>地址</h4>
                <p>北京市海淀区中关村软件园</p>
                <span class="contact-desc">欢迎预约参观</span>
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
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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
        color: var(--theme-primary, #667eea);
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
  margin-bottom: 4rem;
  padding: 4rem 0;
  background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
  border-radius: 20px;
  color: white;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.1)"/><circle cx="10" cy="60" r="0.5" fill="rgba(255,255,255,0.1)"/><circle cx="90" cy="40" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    opacity: 0.3;
  }
  
  .header-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.15);
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    position: relative;
    z-index: 1;
  }
  
  h1 {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    background: linear-gradient(45deg, #ffffff, #f0f0f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    position: relative;
    z-index: 1;
  }
  
  p {
    font-size: 1.3rem;
    margin-bottom: 3rem;
    opacity: 0.95;
    font-weight: 300;
    line-height: 1.6;
    position: relative;
    z-index: 1;
  }
  
  .header-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    position: relative;
    z-index: 1;
    
    .stat-item {
      text-align: center;
      
      .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
      }
      
      .stat-label {
        font-size: 1rem;
        opacity: 0.8;
        font-weight: 500;
      }
    }
  }
}

.company-intro {
  background: white;
  border-radius: 20px;
  padding: 4rem;
  margin-bottom: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  
  .intro-content {
    .intro-header {
      text-align: center;
      margin-bottom: 2rem;
      
      h2 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #333;
        background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }
      
      .intro-subtitle {
        font-size: 1.2rem;
        color: #666;
        font-weight: 500;
      }
    }
    
    .intro-text {
      font-size: 1.2rem;
      line-height: 1.8;
      color: #666;
      margin-bottom: 3rem;
      text-align: center;
      max-width: 800px;
      margin-left: auto;
      margin-right: auto;
    }
    
    .intro-features {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 2rem;
      margin-top: 3rem;
      
      .feature-item {
        text-align: center;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
        
        &:hover {
          transform: translateY(-5px);
          box-shadow: 0 15px 30px rgba(102, 126, 234, 0.15);
          background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        }
        
        .feature-icon {
          width: 80px;
          height: 80px;
          background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 1.5rem;
          box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
          
          .el-icon {
            color: white;
          }
        }
        
        h3 {
          font-size: 1.4rem;
          font-weight: 700;
          margin-bottom: 1rem;
          color: #333;
        }
        
        p {
          color: #666;
          line-height: 1.6;
          font-size: 1rem;
        }
      }
    }
  }
}

.team-section {
  background: white;
  border-radius: 20px;
  padding: 4rem;
  margin-bottom: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  
  .section-header {
    text-align: center;
    margin-bottom: 3rem;
    
    h2 {
      font-size: 2.5rem;
      font-weight: 800;
      margin-bottom: 1rem;
      color: #333;
      background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    p {
      font-size: 1.2rem;
      color: #666;
      font-weight: 500;
    }
  }
  
  .team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2.5rem;
    
    .team-member {
      text-align: center;
      padding: 2.5rem 2rem;
      border-radius: 20px;
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      transition: all 0.3s ease;
      border: 1px solid rgba(102, 126, 234, 0.1);
      
      &:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
      }
      
      .member-avatar {
        position: relative;
        display: inline-block;
        margin-bottom: 1.5rem;
        
        .avatar-ring {
          position: absolute;
          top: -5px;
          left: -5px;
          right: -5px;
          bottom: -5px;
          border: 3px solid var(--theme-primary, #667eea);
          border-radius: 50%;
          opacity: 0;
          transition: all 0.3s ease;
        }
        
        &:hover .avatar-ring {
          opacity: 1;
          transform: scale(1.1);
        }
      }
      
      h3 {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1rem 0 0.5rem 0;
        color: #333;
      }
      
      .position {
        color: var(--theme-primary, #667eea);
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
      }
      
      .description {
        color: #666;
        line-height: 1.6;
        font-size: 1rem;
        margin-bottom: 1.5rem;
      }
      
      .member-social {
        display: flex;
        justify-content: center;
        gap: 1rem;
        
        .el-icon {
          width: 40px;
          height: 40px;
          background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
          color: white;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.3s ease;
          
          &:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
          }
        }
      }
    }
  }
}

.contact-section {
  background: white;
  border-radius: 20px;
  padding: 4rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  
  .section-header {
    text-align: center;
    margin-bottom: 3rem;
    
    h2 {
      font-size: 2.5rem;
      font-weight: 800;
      margin-bottom: 1rem;
      color: #333;
      background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    p {
      font-size: 1.2rem;
      color: #666;
      font-weight: 500;
    }
  }
  
  .contact-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    
    .contact-item {
      display: flex;
      align-items: flex-start;
      gap: 1.5rem;
      padding: 2rem;
      border-radius: 16px;
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      transition: all 0.3s ease;
      border: 1px solid rgba(102, 126, 234, 0.1);
      
      &:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
      }
      
      .contact-icon {
        width: 60px;
        height: 60px;
        background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        
        .el-icon {
          color: white;
        }
      }
      
      .contact-content {
        flex: 1;
        
        h4 {
          font-size: 1.3rem;
          font-weight: 700;
          margin-bottom: 0.5rem;
          color: #333;
        }
        
        p {
          color: #333;
          margin: 0 0 0.5rem 0;
          font-size: 1.1rem;
          font-weight: 600;
        }
        
        .contact-desc {
          color: #666;
          font-size: 0.9rem;
          font-style: italic;
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .page-header {
    padding: 3rem 1rem;
    
    h1 {
      font-size: 2.5rem;
    }
    
    p {
      font-size: 1.1rem;
    }
    
    .header-stats {
      gap: 2rem;
      
      .stat-item .stat-number {
        font-size: 2rem;
      }
    }
  }
  
  .company-intro,
  .team-section,
  .contact-section {
    padding: 2rem 1.5rem;
    margin-bottom: 2rem;
  }
  
  .intro-features,
  .team-grid,
  .contact-info {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .intro-features .feature-item,
  .team-member,
  .contact-item {
    padding: 1.5rem;
  }
  
  .contact-item {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
}
</style>
