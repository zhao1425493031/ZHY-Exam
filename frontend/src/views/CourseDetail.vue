<template>
  <div class="course-detail">
    <!-- 导航栏 -->
    <TopNavigation />
    
    <!-- 课程详情内容 -->
    <div class="course-content" v-loading="loading">
      <div class="container">
        <!-- 面包屑导航 -->
        <el-breadcrumb separator="/" class="breadcrumb">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: '/courses' }">课程</el-breadcrumb-item>
          <el-breadcrumb-item>{{ course?.name || '课程详情' }}</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 课程基本信息 -->
        <div class="course-header" v-if="course">
          <div class="course-info">
            <div class="course-image">
              <img :src="course.image || '/default-course.svg'" :alt="course.name">
              <div class="course-badge" v-if="course.is_free">
                <el-icon><Star /></el-icon>
                <span>免费</span>
              </div>
              <div class="course-badge price" v-else>
                <el-icon><Star /></el-icon>
                <span>¥{{ course.price }}</span>
              </div>
            </div>
            
            <div class="course-meta">
              <h1 class="course-title">{{ course.name }}</h1>
              <p class="course-description">{{ course.description }}</p>
              
              <div class="course-stats">
                <div class="stat-item">
                  <el-icon><User /></el-icon>
                  <span>{{ course.student_count || 0 }} 人学习</span>
                </div>
                <div class="stat-item">
                  <el-icon><Star /></el-icon>
                  <span>{{ course.rating || '4.5' }} 分</span>
                </div>
                <div class="stat-item">
                  <el-icon><Clock /></el-icon>
                  <span>{{ course.duration || '2小时' }}</span>
                </div>
                <div class="stat-item">
                  <el-icon><Document /></el-icon>
                  <span>{{ course.difficulty || '中级' }}</span>
                </div>
              </div>
              
              <div class="course-actions">
                <el-button 
                  v-if="!course.is_subscribed" 
                  :type="course.is_free ? 'primary' : 'warning'"
                  size="large"
                  @click="addToMyCourses"
                  :loading="subscribing"
                >
                  <el-icon><Plus /></el-icon>
                  {{ course.is_free ? '添加到我的课程' : `购买课程 (¥${course.price})` }}
                </el-button>
                <el-button 
                  v-else 
                  type="success" 
                  size="large"
                  disabled
                >
                  <el-icon><Check /></el-icon>
                  已添加
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 课程内容 -->
        <div class="course-body" v-if="course">
          <div class="exams-content">
            <h3>相关考试</h3>
            <div class="exams-list" v-loading="examsLoading">
              <div class="exam-item" v-for="exam in relatedExams" :key="exam.id">
                <div class="exam-info">
                  <h4>{{ exam.title }}</h4>
                  <p>{{ exam.description }}</p>
                  <div class="exam-meta">
                    <span class="exam-duration">{{ exam.duration }}分钟</span>
                    <span class="exam-questions">{{ exam.question_count }}题</span>
                    <span class="exam-points">{{ exam.total_points }}分</span>
                  </div>
                </div>
                <div class="exam-actions">
                  <el-button 
                    type="primary" 
                    @click="startExam(exam)"
                    :disabled="!canTakeExam"
                  >
                    <el-icon><Play /></el-icon>
                    {{ getExamButtonText() }}
                  </el-button>
                </div>
              </div>
              <div v-if="!examsLoading && relatedExams.length === 0" class="no-exams">
                <el-empty description="暂无相关考试" />
              </div>
            </div>
          </div>
        </div>

        <!-- 加载失败 -->
        <div v-else-if="!loading && !course" class="error-state">
          <el-empty description="课程不存在或已被删除">
            <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
          </el-empty>
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
  Star, 
  User, 
  Clock, 
  Document, 
  Plus, 
  Play,
  Check
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { subjectsApi } from '@/api/subjects'
import { examApi } from '@/api/exams'
import { userSubjectsApi } from '@/api/user_subjects'
import TopNavigation from '@/components/layout/TopNavigation.vue'

export default {
  name: 'CourseDetail',
  components: {
    TopNavigation,
    Star,
    User,
    Clock,
    Document,
    Plus,
    Play,
    Check
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const loading = ref(false)
    const subscribing = ref(false)
    const course = ref(null)
    const relatedExams = ref([])
    const examsLoading = ref(false)
    
    // 模拟课程大纲数据
    const chapters = ref([
      {
        title: '基础概念',
        duration: '30分钟',
        lessons: [
          { title: '什么是Vue.js', duration: '10分钟' },
          { title: 'Vue.js的特点', duration: '10分钟' },
          { title: '开发环境搭建', duration: '10分钟' }
        ]
      },
      {
        title: '组件开发',
        duration: '45分钟',
        lessons: [
          { title: '组件基础', duration: '15分钟' },
          { title: '组件通信', duration: '15分钟' },
          { title: '插槽的使用', duration: '15分钟' }
        ]
      },
      {
        title: '状态管理',
        duration: '40分钟',
        lessons: [
          { title: 'Vuex基础', duration: '20分钟' },
          { title: 'Actions和Mutations', duration: '20分钟' }
        ]
      }
    ])
    
    // 模拟学员评价数据
    const reviews = ref([
      {
        id: 1,
        name: '张三',
        avatar: '',
        rating: 5,
        date: '2024-01-15',
        content: '课程内容很实用，老师讲解得很清楚，学到了很多东西！'
      },
      {
        id: 2,
        name: '李四',
        avatar: '',
        rating: 4,
        date: '2024-01-10',
        content: '整体不错，就是有些地方讲得有点快，需要多练习。'
      },
      {
        id: 3,
        name: '王五',
        avatar: '',
        rating: 5,
        date: '2024-01-08',
        content: '非常棒的课程，从基础到进阶都有涵盖，推荐！'
      }
    ])
    
    // 获取课程详情
    const fetchCourseDetail = async () => {
      try {
        loading.value = true
        const courseId = route.params.id
        
        // 获取课程基本信息
        const response = await subjectsApi.getSubject(courseId)
        if (response.code === 200) {
          course.value = {
            ...response.data,
            student_count: Math.floor(Math.random() * 1000) + 100,
            rating: (Math.random() * 1 + 4).toFixed(1),
            duration: `${Math.floor(Math.random() * 5) + 1}小时`,
            image: response.data.cover_image || '/default-course.svg'
          }
          
          // 检查用户是否已订阅该课程
          if (authStore.isLoggedIn) {
            try {
              const subscribeResponse = await userSubjectsApi.checkSubscription(courseId)
              if (subscribeResponse.code === 200) {
                course.value.is_subscribed = subscribeResponse.data.is_subscribed
              }
            } catch (error) {
              console.error('检查订阅状态失败:', error)
            }
          }
          
          // 获取相关考试
          await fetchRelatedExams()
        } else {
          ElMessage.error('获取课程详情失败')
        }
      } catch (error) {
        console.error('获取课程详情失败:', error)
        ElMessage.error('获取课程详情失败')
      } finally {
        loading.value = false
      }
    }
    
    // 获取相关考试
    const fetchRelatedExams = async () => {
      try {
        examsLoading.value = true
        const response = await examApi.getExams({
          subject_id: route.params.id,
          status: 'published',
          page: 1,
          size: 10
        })
        
        if (response.code === 200) {
          relatedExams.value = response.data.items || []
        }
      } catch (error) {
        console.error('获取相关考试失败:', error)
      } finally {
        examsLoading.value = false
      }
    }
    
    // 检查是否可以参加考试
    const canTakeExam = computed(() => {
      if (!course.value) return false
      // 所有课程都需要先添加到我的课程才能参加考试
      return course.value.is_subscribed
    })
    
    // 添加到我的课程或购买课程
    const addToMyCourses = async () => {
      try {
        if (!authStore.isLoggedIn) {
          ElMessage.warning('请先登录')
          authStore.showLoginDialog = true
          return
        }
        
        // 如果是付费课程且未购买，显示购买提示
        if (!course.value.is_free && !course.value.is_subscribed) {
          ElMessage.info('付费课程需要购买后才能使用')
          // 这里可以跳转到支付页面或显示支付弹窗
          return
        }
        
        subscribing.value = true
        
        const response = await userSubjectsApi.subscribeSubject({
          subject_id: course.value.id
        })
        
        if (response.code === 200) {
          ElMessage.success('课程已添加到我的课程')
          course.value.is_subscribed = true
        } else {
          ElMessage.error(response.message || '添加课程失败')
        }
      } catch (error) {
        console.error('添加课程失败:', error)
        ElMessage.error('添加课程失败')
      } finally {
        subscribing.value = false
      }
    }
    
    // 开始学习
    
    
    // 获取考试按钮文本
    const getExamButtonText = () => {
      if (!authStore.isLoggedIn) {
        return '请先登录'
      }
      
      if (!course.value) {
        return '开始考试'
      }
      
      if (course.value.is_subscribed) {
        return '开始考试'
      }
      
      if (course.value.is_free) {
        return '请先添加课程'
      } else {
        return '请先购买课程'
      }
    }
    
    // 开始考试
    const startExam = (exam) => {
      // 检查是否已登录
      if (!authStore.isLoggedIn) {
        ElMessage.warning('请先登录')
        authStore.showLoginDialog = true
        return
      }
      
      // 检查是否已添加课程
      if (!canTakeExam.value) {
        if (course.value.is_free) {
          ElMessage.warning('请先将课程添加到我的课程后再参加考试')
        } else {
          ElMessage.warning('请先购买并添加课程后再参加考试')
        }
        return
      }
      
      router.push(`/exam/detail/${exam.id}`)
    }
    
    onMounted(() => {
      fetchCourseDetail()
    })
    
    return {
      loading,
      subscribing,
      course,
      relatedExams,
      examsLoading,
      chapters,
      reviews,
      canTakeExam,
      addToMyCourses,
      startExam,
      getExamButtonText
    }
  }
}
</script>

<style lang="scss" scoped>
.course-detail {
  min-height: 100vh;
  background: #f5f5f5;
}

.course-content {
  padding-top: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.breadcrumb {
  margin-bottom: 2rem;
}

.course-header {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.course-info {
  display: flex;
  gap: 2rem;
}

.course-image {
  position: relative;
  flex-shrink: 0;
  
  img {
    width: 300px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
  }
  
  .course-badge {
    position: absolute;
    top: 1rem;
    left: 1rem;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    
    &.price {
      background: #ff6b6b;
    }
  }
}

.course-meta {
  flex: 1;
}

.course-title {
  font-size: 2rem;
  font-weight: bold;
  margin: 0 0 1rem 0;
  color: #333;
}

.course-description {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.course-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  
  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #666;
    font-size: 0.9rem;
  }
}

.course-actions {
  display: flex;
  gap: 1rem;
}

.course-body {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.course-tabs {
  :deep(.el-tabs__content) {
    padding-top: 2rem;
  }
}

.intro-content {
  h3 {
    color: #333;
    margin-bottom: 1rem;
  }
  
  p, ul {
    color: #666;
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }
  
  ul {
    padding-left: 1.5rem;
  }
  
  li {
    margin-bottom: 0.5rem;
  }
}

.outline-content {
  .chapter-list {
    .chapter-item {
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      margin-bottom: 1rem;
      overflow: hidden;
    }
    
    .chapter-header {
      background: #f8f9fa;
      padding: 1rem;
      display: flex;
      align-items: center;
      gap: 1rem;
      border-bottom: 1px solid #e0e0e0;
      
      h4 {
        margin: 0;
        flex: 1;
        color: #333;
      }
      
      .chapter-duration {
        color: #666;
        font-size: 0.9rem;
      }
    }
    
    .lesson-list {
      .lesson-item {
        padding: 0.75rem 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        border-bottom: 1px solid #f0f0f0;
        
        &:last-child {
          border-bottom: none;
        }
        
        .lesson-duration {
          margin-left: auto;
          color: #666;
          font-size: 0.9rem;
        }
      }
    }
  }
}

.exams-content {
  .exams-list {
    .exam-item {
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      padding: 1.5rem;
      margin-bottom: 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .exam-info {
        flex: 1;
        
        h4 {
          margin: 0 0 0.5rem 0;
          color: #333;
        }
        
        p {
          color: #666;
          margin: 0 0 1rem 0;
          line-height: 1.5;
        }
        
        .exam-meta {
          display: flex;
          gap: 1rem;
          
          span {
            background: #f0f0f0;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            color: #666;
          }
        }
      }
    }
  }
}

.reviews-content {
  .review-item {
    border-bottom: 1px solid #f0f0f0;
    padding: 1.5rem 0;
    
    &:last-child {
      border-bottom: none;
    }
    
    .review-header {
      display: flex;
      align-items: center;
      gap: 1rem;
      margin-bottom: 1rem;
      
      .review-info {
        flex: 1;
        
        .review-name {
          font-weight: 500;
          color: #333;
          margin-right: 1rem;
        }
      }
      
      .review-date {
        color: #999;
        font-size: 0.9rem;
      }
    }
    
    .review-content {
      color: #666;
      line-height: 1.6;
      margin: 0;
    }
  }
}

.error-state {
  text-align: center;
  padding: 4rem 0;
}

// 响应式设计
@media (max-width: 768px) {
  .course-info {
    flex-direction: column;
  }
  
  .course-image img {
    width: 100%;
    height: 200px;
  }
  
  .course-stats {
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .course-actions {
    flex-direction: column;
  }
  
  .exam-item {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 1rem;
  }
}
</style>