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
            <h2>专业的在线考试平台</h2>
            <p>为教育机构和企业提供完整的在线考试解决方案</p>
            <div class="hero-actions">
              <el-button type="primary" size="large" @click="goToLogin">
                立即开始
              </el-button>
              <el-button size="large" @click="scrollToFeatures">
                了解更多
              </el-button>
            </div>
          </div>
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
              v-for="course in courses" 
              :key="course.id"
              class="course-card"
              @click="viewCourse(course)"
            >
              <div class="course-image">
                <img :src="course.image" :alt="course.name" />
                <div class="course-overlay">
                  <el-button type="primary" size="small">查看详情</el-button>
                </div>
              </div>
              <div class="course-content">
                <h4>{{ course.name }}</h4>
                <p>{{ course.description }}</p>
                <div class="course-meta">
                  <span class="course-price" :class="{ free: course.is_free }">
                    {{ course.is_free ? '免费' : `¥${course.price}` }}
                  </span>
                  <span class="course-students">{{ course.student_count }}人学习</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { subjectsApi } from '@/api/subjects'
import TopNavigation from '@/components/layout/TopNavigation.vue'

export default {
  name: 'Home',
  components: {
    TopNavigation
  },
  setup() {
    const router = useRouter()
    const coursesLoading = ref(false)
    const courses = ref([])

    // 获取课程列表
    const fetchCourses = async () => {
      try {
        coursesLoading.value = true
        const response = await subjectsApi.getSubjects({
          status: 'active',
          page: 1,
          size: 12
        })
        
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
      } catch (error) {
        console.error('获取课程列表失败:', error)
        // 如果是401错误，不显示错误消息，使用模拟数据
        if (error.response?.status === 401) {
          // Use mock data
          courses.value = [
            { 
              id: 1, 
              name: 'Vue.js 3.0 实战开发', 
              description: '深入学习Vue.js 3.0的核心特性和实战应用', 
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
              description: '掌握Python数据分析的核心技能', 
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
              description: '学习现代UI/UX设计理念和实践', 
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
        } else {
          ElMessage.error('获取课程列表失败')
        }
      } finally {
        coursesLoading.value = false
      }
    }

    // 跳转到登录页面
    const goToLogin = () => {
      // 由于现在使用弹窗模式，这里可以跳转到课程页面或者显示提示
      router.push('/courses')
    }

    // 滚动到功能区域
    const scrollToFeatures = () => {
      const element = document.getElementById('courses')
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    }

    // 查看课程详情
    const viewCourse = (course) => {
      router.push(`/course/${course.id}`)
    }

    onMounted(() => {
      fetchCourses()
    })

    return {
      coursesLoading,
      courses,
      goToLogin,
      scrollToFeatures,
      viewCourse
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;

  .hero-content {
    h2 {
      font-size: 3rem;
      font-weight: bold;
      margin-bottom: 1rem;
    }

    p {
      font-size: 1.2rem;
      margin-bottom: 2rem;
      opacity: 0.9;
    }

    .hero-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
    }
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
    }
  }

  .courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;

    .course-card {
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
      overflow: hidden;
      transition: all 0.3s ease;
      cursor: pointer;

      &:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
      }

      .course-image {
        position: relative;
        height: 200px;
        overflow: hidden;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .course-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          opacity: 0;
          transition: opacity 0.3s ease;
        }

        &:hover .course-overlay {
          opacity: 1;
        }
      }

      .course-content {
        padding: 1.5rem;

        h4 {
          font-size: 1.2rem;
          font-weight: bold;
          margin-bottom: 0.5rem;
          color: #333;
        }

        p {
          color: #666;
          line-height: 1.5;
          margin-bottom: 1rem;
        }

        .course-meta {
          display: flex;
          justify-content: space-between;
          align-items: center;

          .course-price {
            font-size: 1.1rem;
            font-weight: bold;
            color: #667eea;

            &.free {
              color: #52c41a;
            }
          }

          .course-students {
            color: #999;
            font-size: 0.9rem;
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .hero-section {
    padding: 2rem 0;

    .hero-content {
      h2 {
        font-size: 2rem;
      }

      p {
        font-size: 1rem;
      }

      .hero-actions {
        flex-direction: column;
        align-items: center;
      }
    }
  }

  .courses-section {
    padding: 2rem 0;

    .courses-grid {
      grid-template-columns: 1fr;
    }
  }
}
</style>
