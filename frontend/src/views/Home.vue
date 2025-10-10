<template>
  <div class="home">
    <!-- 顶部导航栏 -->
    <TopNavigation />

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 轮播图区域 -->
      <section class="hero-section">
        <div class="container">
          <div class="hero-content">
            <div class="hero-badge">
              <el-icon><Star /></el-icon>
              <span>专业可信赖</span>
            </div>
            <h2>专业的在线考试平台</h2>
            <p>为教育机构和企业提供完整的在线考试解决方案，让学习更高效，让考试更公平</p>
            <div class="hero-actions">
              <el-button type="primary" size="large" @click="goToLogin" class="hero-btn-primary">
                <el-icon><User /></el-icon>
                立即开始
              </el-button>
              <el-button size="large" @click="scrollToFeatures" class="hero-btn-secondary">
                <el-icon><InfoFilled /></el-icon>
                了解更多
              </el-button>
            </div>
            <div class="hero-stats">
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
        </div>
        <!-- 装饰性元素 -->
        <div class="hero-decoration">
          <div class="floating-shape shape-1"></div>
          <div class="floating-shape shape-2"></div>
          <div class="floating-shape shape-3"></div>
        </div>
      </section>

      <!-- 课程展示区域 -->
      <section class="courses-section" id="courses">
        <div class="container">
          <div class="section-header">
            <h3>精选课程</h3>
            <p>优质课程，助您技能提升</p>
          </div>
          
          <div class="courses-grid" v-loading="coursesLoading">
            <div 
              v-for="course in filteredCourses" 
              :key="course.id"
              class="course-card"
              @click="viewCourse(course)"
            >
              <div class="course-image">
                <img :src="course.image || '/default-course.svg'" :alt="course.name">
                <div class="course-overlay">
                  <el-button type="primary" size="small" @click.stop="viewCourse(course)" class="overlay-btn">
                    <el-icon><User /></el-icon>
                    立即学习
                  </el-button>
                </div>
                <div class="course-badge" v-if="course.is_free">
                  <el-icon><Star /></el-icon>
                  <span>免费</span>
                </div>
                <div class="course-badge price" v-else>
                  <el-icon><Star /></el-icon>
                  <span>¥{{ course.price }}</span>
                </div>
                <div class="course-level">
                  <span>{{ course.difficulty || '中级' }}</span>
                </div>
              </div>
              <div class="course-content">
                <div class="course-header">
                  <h4>{{ course.name }}</h4>
                  <div class="course-rating">
                    <el-icon><Star /></el-icon>
                    <span>{{ course.rating || 4.8 }}</span>
                  </div>
                </div>
                <p class="course-description">{{ course.description }}</p>
                <div class="course-meta">
                  <div class="course-category">
                    <el-icon><Folder /></el-icon>
                    <span>{{ course.category || '未分类' }}</span>
                  </div>
                  <div class="course-students">
                    <el-icon><User /></el-icon>
                    <span>{{ course.student_count || 0 }}人学习</span>
                  </div>
                </div>
                <div class="course-footer">
                  <div class="course-instructor">
                    <el-avatar :size="28" :src="course.instructor_avatar" class="instructor-avatar">
                      {{ course.instructor_name?.charAt(0) || 'A' }}
                    </el-avatar>
                    <div class="instructor-info">
                      <span class="instructor-name">{{ course.instructor_name || '讲师' }}</span>
                      <span class="course-duration">
                        <el-icon><Clock /></el-icon>
                        {{ course.duration || '2小时' }}
                      </span>
                    </div>
                  </div>
                  <div class="course-action">
                    <el-button type="primary" size="small" @click.stop="viewCourse(course)">
                      查看详情
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="section-footer" v-if="filteredCourses.length === 0 && !coursesLoading">
            <div class="mock-courses">
              <div class="course-card mock-card" v-for="mockCourse in mockCourses" :key="mockCourse.id">
                <div class="course-image">
                  <img :src="mockCourse.image" :alt="mockCourse.name">
                  <div class="course-overlay">
                    <el-button type="primary" size="small" class="overlay-btn">
                      <el-icon><User /></el-icon>
                      立即学习
                    </el-button>
                  </div>
                  <div class="course-badge" v-if="mockCourse.is_free">
                    <el-icon><Star /></el-icon>
                    <span>免费</span>
                  </div>
                  <div class="course-badge price" v-else>
                    <el-icon><Star /></el-icon>
                    <span>¥{{ mockCourse.price }}</span>
                  </div>
                  <div class="course-level">
                    <span>{{ mockCourse.difficulty }}</span>
                  </div>
                </div>
                <div class="course-content">
                  <div class="course-header">
                    <h4>{{ mockCourse.name }}</h4>
                    <div class="course-rating">
                      <el-icon><Star /></el-icon>
                      <span>{{ mockCourse.rating }}</span>
                    </div>
                  </div>
                  <p class="course-description">{{ mockCourse.description }}</p>
                  <div class="course-meta">
                    <div class="course-category">
                      <el-icon><Folder /></el-icon>
                      <span>{{ mockCourse.category }}</span>
                    </div>
                    <div class="course-students">
                      <el-icon><User /></el-icon>
                      <span>{{ mockCourse.student_count }}人学习</span>
                    </div>
                  </div>
                  <div class="course-footer">
                    <div class="course-instructor">
                      <el-avatar :size="28" :src="mockCourse.instructor_avatar" class="instructor-avatar">
                        {{ mockCourse.instructor_name.charAt(0) }}
                      </el-avatar>
                      <div class="instructor-info">
                        <span class="instructor-name">{{ mockCourse.instructor_name }}</span>
                        <span class="course-duration">
                          <el-icon><Clock /></el-icon>
                          {{ mockCourse.duration }}
                        </span>
                      </div>
                    </div>
                    <div class="course-action">
                      <el-button type="primary" size="small">
                        查看详情
                      </el-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="section-footer" v-else-if="filteredCourses.length > 0">
            <el-button type="primary" @click="goToLogin">查看更多课程</el-button>
          </div>
        </div>
      </section>

      <!-- 功能特色区域 -->
      <section class="features-section" ref="featuresSection">
        <div class="container">
          <div class="section-header">
            <h3>平台特色</h3>
            <p>强大的功能，优秀的体验</p>
          </div>
          
          <div class="features-grid">
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon size="48"><Document /></el-icon>
              </div>
              <h4>智能组卷</h4>
              <p>支持随机组卷和手动选题，满足不同考试需求</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon size="48"><Monitor /></el-icon>
              </div>
              <h4>实时监控</h4>
              <p>考试过程实时监控，防作弊技术保障考试公平</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon size="48"><DataAnalysis /></el-icon>
              </div>
              <h4>数据分析</h4>
              <p>详细的考试数据分析和学习报告，助力教学改进</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon size="48"><User /></el-icon>
              </div>
              <h4>用户管理</h4>
              <p>完善的用户权限管理和角色分配系统</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon size="48"><Upload /></el-icon>
              </div>
              <h4>批量导入</h4>
              <p>支持用户、试题等数据的批量导入导出</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon size="48"><ChatDotRound /></el-icon>
              </div>
              <h4>在线答疑</h4>
              <p>实时在线答疑系统，及时解决学习问题</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 统计数据区域 -->
      <section class="stats-section">
        <div class="container">
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-number">{{ stats.totalUsers }}</div>
              <div class="stat-label">注册用户</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ stats.totalCourses }}</div>
              <div class="stat-label">课程数量</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ stats.totalExams }}</div>
              <div class="stat-label">考试场次</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ stats.totalQuestions }}</div>
              <div class="stat-label">题库题目</div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h4>ExamSphere</h4>
            <p>专业的在线考试管理系统</p>
          </div>
          <div class="footer-section">
            <h4>产品功能</h4>
            <ul>
              <li>在线考试</li>
              <li>题库管理</li>
              <li>成绩分析</li>
              <li>用户管理</li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>技术支持</h4>
            <ul>
              <li>使用帮助</li>
              <li>技术文档</li>
              <li>联系我们</li>
              <li>意见反馈</li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>关于我们</h4>
            <ul>
              <li>公司介绍</li>
              <li>团队介绍</li>
              <li>发展历程</li>
              <li>合作伙伴</li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2024 ExamSphere. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Document, Monitor, DataAnalysis, User, Upload, ChatDotRound, Star, Folder, Clock, InfoFilled } from '@element-plus/icons-vue'
import { subjectsApi } from '@/api/subjects'
import TopNavigation from '@/components/layout/TopNavigation.vue'

export default {
  name: 'Home',
  components: {
    TopNavigation,
    Document,
    Monitor,
    DataAnalysis,
    User,
    Upload,
    ChatDotRound,
    Star,
    Folder,
    Clock,
    InfoFilled
  },
  setup() {
    const router = useRouter()
    const coursesLoading = ref(false)
    const courses = ref([])
    const stats = ref({
      totalUsers: 0,
      totalCourses: 0,
      totalExams: 0,
      totalQuestions: 0
    })
    const featuresSection = ref(null)

    // 假课程数据
    const mockCourses = ref([
      {
        id: 1,
        name: 'Vue.js 前端开发实战',
        description: '从零开始学习Vue.js，掌握现代前端开发技术，构建响应式Web应用',
        category: '编程开发',
        is_free: true,
        price: 0,
        difficulty: '中级',
        rating: 4.8,
        student_count: 1256,
        instructor_name: '李老师',
        instructor_avatar: '',
        duration: '3小时',
        image: '/course-vue.svg'
      },
      {
        id: 2,
        name: 'UI/UX 设计基础',
        description: '学习用户界面和用户体验设计原理，掌握设计工具和设计思维',
        category: '设计创意',
        is_free: false,
        price: 299,
        difficulty: '初级',
        rating: 4.6,
        student_count: 892,
        instructor_name: '王老师',
        instructor_avatar: '',
        duration: '2.5小时',
        image: '/course-design.svg'
      },
      {
        id: 3,
        name: 'Python 数据分析',
        description: '使用Python进行数据分析，学习pandas、numpy等库的使用',
        category: '编程开发',
        is_free: false,
        price: 399,
        difficulty: '高级',
        rating: 4.9,
        student_count: 634,
        instructor_name: '陈老师',
        instructor_avatar: '',
        duration: '4小时',
        image: '/course-python.svg'
      }
    ])

    // 过滤后的课程（现在直接返回课程列表）
    const filteredCourses = computed(() => {
      return courses.value
    })

    // 获取课程列表
    const fetchCourses = async () => {
      try {
        console.log('开始获取课程列表...')
        coursesLoading.value = true
        const response = await subjectsApi.getSubjects({
          status: 'active',
          page: 1,
          size: 12
        })
        
        console.log('API响应:', response)
        
        // 为课程添加模拟数据
        courses.value = (response.data.items || []).map(course => ({
          ...course,
          student_count: Math.floor(Math.random() * 1000) + 100,
          rating: (Math.random() * 1 + 4).toFixed(1),
          instructor_name: '张老师',
          instructor_avatar: '',
          duration: `${Math.floor(Math.random() * 5) + 1}小时`,
          image: course.image || '/default-course.svg'
        }))
        
        console.log('处理后的课程数据:', courses.value)
      } catch (error) {
        console.error('获取课程列表失败:', error)
        // 如果是401错误，不显示错误消息，使用模拟数据
        if (error.response?.status === 401) {
          console.log('使用模拟数据...')
          // 使用模拟数据
          courses.value = [
            {
              id: 1,
              name: 'Vue.js 3.0 实战开发',
              description: '从零开始学习Vue.js 3.0，掌握现代前端开发技能',
              category: 'programming',
              is_free: false,
              price: 299,
              student_count: 1250,
              rating: 4.8,
              instructor_name: '张老师',
              instructor_avatar: '',
              duration: '3小时',
              image: '/default-course.svg'
            },
            {
              id: 2,
              name: 'Python 数据分析',
              description: '学习使用Python进行数据分析和可视化',
              category: 'programming',
              is_free: true,
              price: 0,
              student_count: 890,
              rating: 4.6,
              instructor_name: '李老师',
              instructor_avatar: '',
              duration: '2.5小时',
              image: '/default-course.svg'
            },
            {
              id: 3,
              name: 'UI/UX 设计基础',
              description: '掌握现代UI/UX设计原理和实践技巧',
              category: 'design',
              is_free: false,
              price: 199,
              student_count: 650,
              rating: 4.7,
              instructor_name: '王老师',
              instructor_avatar: '',
              duration: '2小时',
              image: '/default-course.svg'
            }
          ]
          console.log('设置模拟数据:', courses.value)
        } else {
          ElMessage.error('获取课程列表失败')
        }
      } finally {
        coursesLoading.value = false
        console.log('课程加载完成，最终数据:', courses.value)
      }
    }


    // 获取统计数据
    const fetchStats = async () => {
      try {
        // 这里可以调用统计API获取真实数据
        // 暂时使用模拟数据
        stats.value = {
          totalUsers: 1250,
          totalCourses: 45,
          totalExams: 320,
          totalQuestions: 8500
        }
      } catch (error) {
        console.error('获取统计数据失败:', error)
      }
    }

    // 跳转到登录页面
    const goToLogin = () => {
      // 由于现在使用弹窗模式，这里可以跳转到课程页面或者显示提示
      router.push('/courses')
    }

    // 跳转到注册页面
    const goToRegister = () => {
      router.push('/register')
    }

    // 查看课程详情
    const viewCourse = (course) => {
      router.push(`/course/${course.id}`)
    }

    // 滚动到功能特色区域
    const scrollToFeatures = () => {
      if (featuresSection.value) {
        featuresSection.value.scrollIntoView({ behavior: 'smooth' })
      }
    }

    onMounted(() => {
      console.log('Home.vue mounted, fetching courses...')
      fetchCourses()
      fetchStats()
    })

    return {
      coursesLoading,
      courses,
      mockCourses,
      filteredCourses,
      stats,
      featuresSection,
      fetchCourses,
      goToLogin,
      goToRegister,
      viewCourse,
      scrollToFeatures
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

// 主要内容区域
.main-content {
  min-height: calc(100vh - 60px);
}

// 轮播图区域
.hero-section {
  background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
  color: white;
  padding: 6rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
  min-height: 80vh;
  display: flex;
  align-items: center;

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

  .hero-content {
    position: relative;
    z-index: 1;
    max-width: 800px;
    margin: 0 auto;
    
    .hero-badge {
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
    }
    
    h2 {
      font-size: 4rem;
      font-weight: 800;
      margin-bottom: 1.5rem;
      text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      background: linear-gradient(45deg, #ffffff, #f0f0f0);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      line-height: 1.2;
    }

    p {
      font-size: 1.4rem;
      margin-bottom: 3rem;
      opacity: 0.95;
      font-weight: 300;
      line-height: 1.6;
    }

    .hero-actions {
      display: flex;
      gap: 1.5rem;
      justify-content: center;
      margin-bottom: 4rem;
      
      .el-button {
        padding: 1.2rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 15px;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        
        &.hero-btn-primary {
          background: rgba(255, 255, 255, 0.2);
          border: 2px solid rgba(255, 255, 255, 0.3);
          backdrop-filter: blur(10px);
          color: white;
          
          &:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
          }
        }
        
        &.hero-btn-secondary {
          background: transparent;
          border: 2px solid rgba(255, 255, 255, 0.6);
          color: white;
          
          &:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.9);
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
          }
        }
      }
    }

    .hero-stats {
      display: flex;
      justify-content: center;
      gap: 3rem;
      
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

  .hero-decoration {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    
    .floating-shape {
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      animation: float 6s ease-in-out infinite;
      
      &.shape-1 {
        width: 80px;
        height: 80px;
        top: 20%;
        left: 10%;
        animation-delay: 0s;
      }
      
      &.shape-2 {
        width: 120px;
        height: 120px;
        top: 60%;
        right: 15%;
        animation-delay: 2s;
      }
      
      &.shape-3 {
        width: 60px;
        height: 60px;
        bottom: 30%;
        left: 20%;
        animation-delay: 4s;
      }
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

// 课程展示区域
.courses-section {
  padding: 4rem 0;
  background: white;

  .section-header {
    text-align: center;
    margin-bottom: 3rem;

    h3 {
      font-size: 2.5rem;
      font-weight: bold;
      margin-bottom: 1rem;
      color: #333;
    }

    p {
      font-size: 1.1rem;
      color: #666;
      margin-bottom: 2rem;
    }

    .course-filters {
      display: flex;
      justify-content: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
  }

  .courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
  }

  .course-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;

    &:hover {
      transform: translateY(-8px);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);

      .course-overlay {
        opacity: 1;
      }
    }

    .course-image {
      position: relative;
      height: 200px;
      overflow: hidden;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
      }

      .course-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
      }

      .course-badge {
        position: absolute;
        top: 1rem;
        right: 1rem;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        z-index: 2;

        &.price {
          background: linear-gradient(135deg, #ff6b6b, #ee5a52);
          color: white;
        }

        &:not(.price) {
          background: linear-gradient(135deg, #4ecdc4, #44a08d);
          color: white;
        }
      }
    }

    .course-content {
      padding: 1.5rem;

      h4 {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
        color: #333;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .course-description {
        color: #666;
        margin-bottom: 1rem;
        line-height: 1.5;
        font-size: 0.9rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .course-meta {
        margin-bottom: 1rem;

        .course-category {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.8rem;
          font-size: 0.9rem;
          color: #667eea;
          font-weight: 500;
        }

        .course-stats {
          display: flex;
          justify-content: space-between;
          font-size: 0.85rem;
          color: #999;

          .course-students,
          .course-rating {
            display: flex;
            align-items: center;
            gap: 0.3rem;
          }
        }
      }

      .course-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 1rem;
        border-top: 1px solid #f0f0f0;

        .course-instructor {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.85rem;
          color: #666;
        }

        .course-duration {
          display: flex;
          align-items: center;
          gap: 0.3rem;
          font-size: 0.85rem;
          color: #999;
        }
      }
    }
  }

  .section-footer {
    text-align: center;
    margin-top: 2rem;
  }
}

// 假课程样式
.mock-courses {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
  
  .mock-card {
    opacity: 0.8;
    transition: opacity 0.3s ease;
    
    &:hover {
      opacity: 1;
    }
  }
}

// 功能特色区域
.features-section {
  padding: 4rem 0;
  background: #f8f9fa;

  .section-header {
    text-align: center;
    margin-bottom: 3rem;

    h3 {
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

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
  }

  .feature-item {
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-5px);
    }

    .feature-icon {
      color: #667eea;
      margin-bottom: 1rem;
    }

    h4 {
      font-size: 1.3rem;
      font-weight: bold;
      margin-bottom: 1rem;
      color: #333;
    }

    p {
      color: #666;
      line-height: 1.5;
    }
  }
}

// 统计数据区域
.stats-section {
  padding: 3rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    text-align: center;
  }

  .stat-item {
    .stat-number {
      font-size: 3rem;
      font-weight: bold;
      margin-bottom: 0.5rem;
    }

    .stat-label {
      font-size: 1.1rem;
      opacity: 0.9;
    }
  }
}

// 页脚
.footer {
  background: #333;
  color: white;
  padding: 3rem 0 1rem;

  .footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
  }

  .footer-section {
    h4 {
      font-size: 1.2rem;
      font-weight: bold;
      margin-bottom: 1rem;
    }

    p {
      color: #ccc;
      line-height: 1.5;
    }

    ul {
      list-style: none;
      padding: 0;

      li {
        margin-bottom: 0.5rem;

        a {
          color: #ccc;
          text-decoration: none;
          transition: color 0.3s ease;

          &:hover {
            color: white;
          }
        }
      }
    }
  }

  .footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #555;
    color: #ccc;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .hero-section .hero-content h2 {
    font-size: 2rem;
  }

  .hero-section .hero-content .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .courses-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .footer-content {
    grid-template-columns: 1fr;
  }
}
</style>
