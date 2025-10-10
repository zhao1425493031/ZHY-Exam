<template>
  <div class="course-detail">
    <!-- 顶部导航栏 -->
    <TopNavigation />

    <!-- 课程详情内容 -->
    <div class="course-content">
      <div class="container">
        <!-- 面包屑导航 -->
        <el-breadcrumb separator="/" class="breadcrumb">
          <el-breadcrumb-item>
            <router-link to="/">首页</router-link>
          </el-breadcrumb-item>
          <el-breadcrumb-item>
            <router-link to="/courses">课程</router-link>
          </el-breadcrumb-item>
          <el-breadcrumb-item>{{ course.name }}</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 课程基本信息 -->
        <div class="course-header" v-loading="loading">
          <div class="course-info">
            <div class="course-image">
              <img :src="course.image || '/default-course.svg'" :alt="course.name">
              <div class="course-badge" v-if="course.is_free">
                <span>免费</span>
              </div>
              <div class="course-badge price" v-else>
                <span>¥{{ course.price }}</span>
              </div>
            </div>
            
            <div class="course-details">
              <h1>{{ course.name }}</h1>
              <p class="course-description">{{ course.description }}</p>
              
              <div class="course-meta">
                <div class="meta-item">
                  <el-icon><Folder /></el-icon>
                  <span>{{ course.category || '未分类' }}</span>
                </div>
                <div class="meta-item">
                  <el-icon><User /></el-icon>
                  <span>{{ course.student_count || 0 }}人学习</span>
                </div>
                <div class="meta-item">
                  <el-icon><Star /></el-icon>
                  <span>{{ course.rating || 4.8 }}分</span>
                </div>
                <div class="meta-item">
                  <el-icon><Clock /></el-icon>
                  <span>{{ course.duration || '2小时' }}</span>
                </div>
              </div>

              <div class="course-instructor">
                <el-avatar :size="40" :src="course.instructor_avatar">
                  {{ course.instructor_name?.charAt(0) || 'A' }}
                </el-avatar>
                <div class="instructor-info">
                  <h4>{{ course.instructor_name || '讲师' }}</h4>
                  <p>{{ course.instructor_title || '资深讲师' }}</p>
                </div>
              </div>

              <div class="course-actions">
                <el-button 
                  type="primary" 
                  size="large" 
                  @click="enrollCourse"
                  :loading="enrolling"
                >
                  {{ course.is_free ? '免费学习' : `立即购买 ¥${course.price}` }}
                </el-button>
                <el-button size="large" @click="toggleFavorite">
                  <el-icon><Star /></el-icon>
                  {{ isFavorited ? '已收藏' : '收藏' }}
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 课程内容 -->
        <div class="course-sections">
          <el-tabs v-model="activeTab" class="course-tabs">
            <el-tab-pane label="课程介绍" name="intro">
              <div class="course-intro">
                <h3>课程简介</h3>
                <p>{{ course.description }}</p>
                
                <h3>学习目标</h3>
                <ul>
                  <li>掌握核心知识点</li>
                  <li>提升实践能力</li>
                  <li>获得认证证书</li>
                </ul>

                <h3>适合人群</h3>
                <ul>
                  <li>初学者</li>
                  <li>有一定基础的学员</li>
                  <li>希望提升技能的职场人士</li>
                </ul>
              </div>
            </el-tab-pane>

            <el-tab-pane label="课程大纲" name="outline">
              <div class="course-outline">
                <div v-for="(chapter, index) in courseOutline" :key="index" class="chapter">
                  <div class="chapter-header">
                    <h4>{{ chapter.title }}</h4>
                    <span class="chapter-duration">{{ chapter.duration }}</span>
                  </div>
                  <div class="lessons">
                    <div v-for="(lesson, lessonIndex) in chapter.lessons" :key="lessonIndex" class="lesson">
                      <div class="lesson-info">
                        <el-icon><VideoPlay /></el-icon>
                        <span>{{ lesson.title }}</span>
                      </div>
                      <span class="lesson-duration">{{ lesson.duration }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane label="学员评价" name="reviews">
              <div class="course-reviews">
                <div class="reviews-summary">
                  <div class="rating-overview">
                    <div class="rating-score">{{ course.rating || 4.8 }}</div>
                    <div class="rating-stars">
                      <el-rate v-model="course.rating" disabled show-score />
                    </div>
                    <p>基于{{ course.review_count || 128 }}条评价</p>
                  </div>
                </div>

                <div class="reviews-list">
                  <div v-for="review in reviews" :key="review.id" class="review-item">
                    <div class="review-header">
                      <el-avatar :size="32" :src="review.user_avatar">
                        {{ review.username?.charAt(0) }}
                      </el-avatar>
                      <div class="review-user">
                        <h5>{{ review.username }}</h5>
                        <el-rate v-model="review.rating" disabled size="small" />
                      </div>
                      <span class="review-time">{{ formatTime(review.created_at) }}</span>
                    </div>
                    <p class="review-content">{{ review.content }}</p>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <!-- 相关课程 -->
        <div class="related-courses">
          <h3>相关课程</h3>
          <div class="courses-grid">
            <div 
              v-for="relatedCourse in relatedCourses" 
              :key="relatedCourse.id"
              class="course-card"
              @click="viewCourse(relatedCourse)"
            >
              <div class="course-image">
                <img :src="relatedCourse.image || '/default-course.svg'" :alt="relatedCourse.name">
                <div class="course-badge" v-if="relatedCourse.is_free">
                  <span>免费</span>
                </div>
                <div class="course-badge price" v-else>
                  <span>¥{{ relatedCourse.price }}</span>
                </div>
              </div>
              <div class="course-content">
                <h4>{{ relatedCourse.name }}</h4>
                <p>{{ relatedCourse.description }}</p>
                <div class="course-meta">
                  <span class="course-students">{{ relatedCourse.student_count }}人学习</span>
                  <span class="course-rating">{{ relatedCourse.rating }}分</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Folder, User, Star, Clock, VideoPlay 
} from '@element-plus/icons-vue'
import TopNavigation from '@/components/layout/TopNavigation.vue'
import { subjectsApi } from '@/api/subjects'

export default {
  name: 'CourseDetail',
  components: {
    TopNavigation,
    Folder,
    User,
    Star,
    Clock,
    VideoPlay
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const loading = ref(false)
    const enrolling = ref(false)
    const course = ref({})
    const isFavorited = ref(false)
    const activeTab = ref('intro')
    const reviews = ref([])
    const relatedCourses = ref([])

    // 课程大纲
    const courseOutline = ref([
      {
        title: '第一章：基础入门',
        duration: '30分钟',
        lessons: [
          { title: '课程介绍', duration: '5分钟' },
          { title: '环境搭建', duration: '10分钟' },
          { title: '第一个项目', duration: '15分钟' }
        ]
      },
      {
        title: '第二章：核心概念',
        duration: '45分钟',
        lessons: [
          { title: '核心概念讲解', duration: '20分钟' },
          { title: '实践练习', duration: '25分钟' }
        ]
      },
      {
        title: '第三章：进阶应用',
        duration: '60分钟',
        lessons: [
          { title: '高级特性', duration: '30分钟' },
          { title: '项目实战', duration: '30分钟' }
        ]
      }
    ])

    // 获取课程详情
    const fetchCourseDetail = async () => {
      try {
        loading.value = true
        const courseId = route.params.id
        
        // 这里应该调用API获取课程详情
        // const response = await subjectsApi.getSubject(courseId)
        // course.value = response.data
        
        // 暂时使用模拟数据
        course.value = {
          id: courseId,
          name: 'Vue.js 3.0 实战开发',
          description: '从零开始学习Vue.js 3.0，掌握现代前端开发技能，通过实际项目提升开发能力。',
          category: 'programming',
          is_free: false,
          price: 299,
          student_count: 1250,
          rating: 4.8,
          duration: '3小时',
          instructor_name: '张老师',
          instructor_title: '前端架构师',
          instructor_avatar: '',
          image: '/default-course.svg',
          review_count: 128
        }
      } catch (error) {
        console.error('获取课程详情失败:', error)
        ElMessage.error('获取课程详情失败')
      } finally {
        loading.value = false
      }
    }

    // 获取相关课程
    const fetchRelatedCourses = async () => {
      try {
        const response = await subjectsApi.getSubjects({
          category: course.value.category,
          page: 1,
          size: 4
        })
        
        relatedCourses.value = (response.data.items || []).map(item => ({
          ...item,
          student_count: Math.floor(Math.random() * 1000) + 100,
          rating: (Math.random() * 1 + 4).toFixed(1),
          image: item.image || '/default-course.svg'
        }))
      } catch (error) {
        console.error('获取相关课程失败:', error)
      }
    }

    // 获取评价
    const fetchReviews = async () => {
      try {
        // 这里应该调用API获取评价
        // const response = await reviewApi.getReviews(course.value.id)
        // reviews.value = response.data.items || []
        
        // 暂时使用模拟数据
        reviews.value = [
          {
            id: 1,
            username: '学员A',
            rating: 5,
            content: '课程内容很实用，老师讲解得很清楚，推荐！',
            created_at: '2024-01-10T10:30:00Z',
            user_avatar: ''
          },
          {
            id: 2,
            username: '学员B',
            rating: 4,
            content: '整体不错，希望能有更多实战项目。',
            created_at: '2024-01-08T15:20:00Z',
            user_avatar: ''
          }
        ]
      } catch (error) {
        console.error('获取评价失败:', error)
      }
    }

    // 报名课程
    const enrollCourse = async () => {
      try {
        enrolling.value = true
        
        // 这里应该调用API报名课程
        // await courseApi.enrollCourse(course.value.id)
        
        ElMessage.success('报名成功！')
        router.push('/dashboard')
      } catch (error) {
        console.error('报名失败:', error)
        ElMessage.error('报名失败')
      } finally {
        enrolling.value = false
      }
    }

    // 切换收藏状态
    const toggleFavorite = () => {
      isFavorited.value = !isFavorited.value
      ElMessage.success(isFavorited.value ? '已收藏' : '已取消收藏')
    }

    // 查看课程
    const viewCourse = (course) => {
      router.push(`/course/${course.id}`)
    }

    // 格式化时间
    const formatTime = (timeStr) => {
      const time = new Date(timeStr)
      return time.toLocaleDateString('zh-CN')
    }

    onMounted(() => {
      fetchCourseDetail()
      fetchRelatedCourses()
      fetchReviews()
    })

    return {
      loading,
      enrolling,
      course,
      isFavorited,
      activeTab,
      courseOutline,
      reviews,
      relatedCourses,
      enrollCourse,
      toggleFavorite,
      viewCourse,
      formatTime
    }
  }
}
</script>

<style lang="scss" scoped>
.course-detail {
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

.course-content {
  padding-bottom: 4rem;
}

.course-header {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.course-info {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  align-items: start;
}

.course-image {
  position: relative;
  border-radius: 8px;
  overflow: hidden;

  img {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }

  .course-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;

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

.course-details {
  h1 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #333;
  }

  .course-description {
    font-size: 1.1rem;
    color: #666;
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }

  .course-meta {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;

    .meta-item {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.9rem;
      color: #666;

      .el-icon {
        color: #667eea;
      }
    }
  }

  .course-instructor {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;

    .instructor-info {
      h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        color: #333;
      }

      p {
        margin: 0;
        font-size: 0.9rem;
        color: #666;
      }
    }
  }

  .course-actions {
    display: flex;
    gap: 1rem;
  }
}

.course-sections {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);

  .course-tabs {
    :deep(.el-tabs__header) {
      margin-bottom: 2rem;
    }
  }
}

.course-intro {
  h3 {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #333;
  }

  p {
    color: #666;
    line-height: 1.6;
    margin-bottom: 2rem;
  }

  ul {
    margin-bottom: 2rem;
    
    li {
      color: #666;
      line-height: 1.6;
      margin-bottom: 0.5rem;
    }
  }
}

.course-outline {
  .chapter {
    margin-bottom: 2rem;
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    overflow: hidden;

    .chapter-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 1.5rem;
      background: #f8f9fa;
      border-bottom: 1px solid #e4e7ed;

      h4 {
        margin: 0;
        font-size: 1.1rem;
        color: #333;
      }

      .chapter-duration {
        font-size: 0.9rem;
        color: #666;
      }
    }

    .lessons {
      .lesson {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #f0f0f0;

        &:last-child {
          border-bottom: none;
        }

        .lesson-info {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: #666;

          .el-icon {
            color: #667eea;
          }
        }

        .lesson-duration {
          font-size: 0.9rem;
          color: #999;
        }
      }
    }
  }
}

.course-reviews {
  .reviews-summary {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 8px;

    .rating-overview {
      text-align: center;

      .rating-score {
        font-size: 3rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5rem;
      }

      .rating-stars {
        margin-bottom: 0.5rem;
      }

      p {
        margin: 0;
        color: #666;
      }
    }
  }

  .reviews-list {
    .review-item {
      padding: 1.5rem;
      border-bottom: 1px solid #f0f0f0;

      &:last-child {
        border-bottom: none;
      }

      .review-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;

        .review-user {
          flex: 1;

          h5 {
            margin: 0 0 0.5rem 0;
            font-size: 1rem;
            color: #333;
          }
        }

        .review-time {
          font-size: 0.9rem;
          color: #999;
        }
      }

      .review-content {
        color: #666;
        line-height: 1.6;
        margin: 0;
      }
    }
  }
}

.related-courses {
  h3 {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
    color: #333;
  }

  .courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }

  .course-card {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    cursor: pointer;

    &:hover {
      transform: translateY(-4px);
    }

    .course-image {
      position: relative;
      height: 150px;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .course-badge {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        padding: 0.3rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;

        &.price {
          background: #ff6b6b;
          color: white;
        }

        &:not(.price) {
          background: #4ecdc4;
          color: white;
        }
      }
    }

    .course-content {
      padding: 1rem;

      h4 {
        font-size: 1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #333;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      p {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.8rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .course-meta {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        color: #999;
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .course-info {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .course-meta {
    grid-template-columns: 1fr !important;
  }

  .course-actions {
    flex-direction: column;
  }

  .courses-grid {
    grid-template-columns: 1fr;
  }
}
</style>
