<template>
  <div class="exam-detail">
    <!-- 顶部导航栏 -->
    <TopNavigation />

    <!-- 考试详情内容 -->
    <div class="exam-detail-content">
      <div class="container">
        <!-- 返回按钮 -->
        <el-button @click="goBack" class="back-btn">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>

        <!-- 考试信息卡片 -->
        <div class="exam-info-card">
          <div class="exam-header">
            <h1>{{ exam.title }}</h1>
            <el-tag :type="getStatusType(exam.status)" size="large">
              {{ getStatusText(exam.status) }}
            </el-tag>
          </div>

          <div class="exam-meta">
            <div class="meta-item">
              <el-icon><Collection /></el-icon>
              <span>科目：{{ exam.subject_name || '未知科目' }}</span>
            </div>
            <div class="meta-item">
              <el-icon><Timer /></el-icon>
              <span>时长：{{ exam.duration }} 分钟</span>
            </div>
            <div class="meta-item">
              <el-icon><Document /></el-icon>
              <span>题数：{{ exam.question_count }} 题</span>
            </div>
            <div class="meta-item">
              <el-icon><Star /></el-icon>
              <span>总分：{{ exam.total_points }} 分</span>
            </div>
          </div>

          <!-- 考试设置信息 -->
          <div class="exam-settings" v-if="exam.settings">
            <h3>考试设置</h3>
            <div class="settings-grid">
              <div class="setting-item">
                <span class="setting-label">重复考试：</span>
                <el-tag :type="exam.settings.allow_retake ? 'success' : 'warning'">
                  {{ exam.settings.allow_retake ? '允许' : '不允许' }}
                </el-tag>
              </div>
              <div class="setting-item" v-if="exam.start_time">
                <span class="setting-label">开始时间：</span>
                <span>{{ formatDateTime(exam.start_time) }}</span>
              </div>
              <div class="setting-item" v-if="exam.end_time">
                <span class="setting-label">结束时间：</span>
                <span>{{ formatDateTime(exam.end_time) }}</span>
              </div>
              <div class="setting-item" v-if="exam.settings.max_attempts">
                <span class="setting-label">最大尝试次数：</span>
                <span>{{ exam.settings.max_attempts }} 次</span>
              </div>
              <div class="setting-item" v-if="exam.settings.pass_score">
                <span class="setting-label">及格分数：</span>
                <span>{{ exam.settings.pass_score }} 分</span>
              </div>
            </div>
          </div>

          <div class="exam-description" v-if="exam.description">
            <h3>考试说明</h3>
            <p>{{ exam.description }}</p>
          </div>

          <!-- 考试记录提示 -->
          <el-alert
            v-if="availability.has_taken"
            :title="availability.message"
            type="info"
            :closable="false"
            show-icon
            class="exam-alert"
          />

          <!-- 不允许重复考试提示 -->
          <el-alert
            v-if="availability.has_taken && !availability.allow_retake"
            title="该考试不允许重复参加"
            type="warning"
            :closable="false"
            show-icon
            class="exam-alert"
          />

          <!-- 开始考试按钮 -->
          <div class="exam-actions">
            <el-button
              type="primary"
              size="large"
              @click="startExam"
              :disabled="!availability.can_take"
              :loading="starting"
              class="start-btn"
            >
              <el-icon><VideoPlay /></el-icon>
              {{ availability.has_taken ? '重新考试' : '开始考试' }}
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Collection, Timer, Document, Star, VideoPlay } from '@element-plus/icons-vue'
import TopNavigation from '@/components/layout/TopNavigation.vue'
import { examApi } from '@/api/exams'
import { useAuthStore } from '@/stores/auth'
import dayjs from 'dayjs'

export default {
  name: 'ExamDetail',
  components: {
    TopNavigation,
    ArrowLeft,
    Collection,
    Timer,
    Document,
    Star,
    VideoPlay
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const exam = ref({})
    const availability = ref({
      can_take: true,
      has_taken: false,
      attempt_count: 0,
      allow_retake: true,
      message: ''
    })
    const starting = ref(false)

    // 获取考试详情
    const fetchExamDetail = async () => {
      try {
        const examId = route.params.id
        const response = await examApi.getExam(examId)
        
        if (response.code === 200) {
          exam.value = response.data
          
          // 如果用户已登录，检查考试可用性
          if (authStore.isLoggedIn) {
            await checkExamAvailability(examId)
          }
        } else {
          ElMessage.error('获取考试信息失败')
          router.push('/')
        }
      } catch (error) {
        console.error('获取考试详情失败:', error)
        ElMessage.error('获取考试信息失败')
        router.push('/')
      }
    }

    // 检查考试可用性
    const checkExamAvailability = async (examId) => {
      try {
        const response = await examApi.checkExamAvailability(examId)
        if (response.code === 200) {
          availability.value = response.data
        }
      } catch (error) {
        console.error('检查考试可用性失败:', error)
      }
    }

    // 开始考试
    const startExam = async () => {
      // 检查是否登录
      if (!authStore.isLoggedIn) {
        ElMessage.warning('请先登录')
        authStore.openLoginDialog()
        return
      }

      // 确认开始考试
      try {
        await ElMessageBox.confirm(
          `确定开始考试吗？考试时长 ${exam.value.duration} 分钟，共 ${exam.value.question_count} 题。`,
          '开始考试确认',
          {
            confirmButtonText: '开始考试',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        starting.value = true
        
        // 跳转到考试页面
        router.push(`/exam/${exam.value.id}`)
      } catch {
        // 用户取消
      } finally {
        starting.value = false
      }
    }

    // 返回
    const goBack = () => {
      router.back()
    }

    // 获取状态类型
    const getStatusType = (status) => {
      const typeMap = {
        'draft': 'info',
        'published': 'success',
        'ongoing': 'warning',
        'finished': 'danger',
        'cancelled': 'info'
      }
      return typeMap[status] || 'info'
    }

    // 获取状态文本
    const getStatusText = (status) => {
      const textMap = {
        'draft': '草稿',
        'published': '已发布',
        'ongoing': '进行中',
        'finished': '已结束',
        'cancelled': '已取消'
      }
      return textMap[status] || '未知'
    }

    // 格式化日期时间
    const formatDateTime = (dateTime) => {
      if (!dateTime) return ''
      return dayjs(dateTime).format('YYYY-MM-DD HH:mm:ss')
    }

    onMounted(() => {
      fetchExamDetail()
    })

    return {
      exam,
      availability,
      starting,
      startExam,
      goBack,
      getStatusType,
      getStatusText,
      formatDateTime
    }
  }
}
</script>

<style lang="scss" scoped>
.exam-detail {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.exam-detail-content {
  padding: 2rem 0;
}

.back-btn {
  margin-bottom: 1.5rem;
  border-radius: 12px;
  padding: 0.8rem 1.5rem;
  font-weight: 600;
}

.exam-info-card {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);

  .exam-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid #f0f0f0;

    h1 {
      font-size: 2rem;
      font-weight: 800;
      margin: 0;
      color: #333;
      background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
  }

  .exam-meta {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;

    .meta-item {
      display: flex;
      align-items: center;
      gap: 0.8rem;
      padding: 1rem;
      background: rgba(102, 126, 234, 0.05);
      border-radius: 12px;
      font-size: 1.1rem;
      color: #555;

      .el-icon {
        font-size: 1.5rem;
        color: var(--theme-primary, #667eea);
      }
    }
  }

  .exam-settings {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 12px;
    border: 1px solid #dee2e6;

    h3 {
      font-size: 1.3rem;
      font-weight: 700;
      margin: 0 0 1rem 0;
      color: #333;
    }

    .settings-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1rem;

      .setting-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.8rem;
        background: white;
        border-radius: 8px;
        border: 1px solid #e9ecef;

        .setting-label {
          font-weight: 600;
          color: #495057;
          min-width: 120px;
        }
      }
    }
  }

  .exam-description {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 12px;

    h3 {
      font-size: 1.3rem;
      font-weight: 700;
      margin: 0 0 1rem 0;
      color: #333;
    }

    p {
      font-size: 1.1rem;
      line-height: 1.8;
      color: #666;
      margin: 0;
      white-space: pre-wrap;
    }
  }

  .exam-alert {
    margin-bottom: 2rem;
    border-radius: 12px;
    padding: 1rem 1.5rem;

    :deep(.el-alert__title) {
      font-size: 1.1rem;
    }
  }

  .exam-actions {
    display: flex;
    justify-content: center;
    padding-top: 1rem;

    .start-btn {
      padding: 1.2rem 3rem;
      font-size: 1.2rem;
      font-weight: 700;
      border-radius: 15px;
      background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
      border: none;
      box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
      transition: all 0.3s ease;

      &:hover:not(:disabled) {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
      }

      &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .exam-info-card {
    padding: 2rem 1.5rem;

    .exam-header {
      flex-direction: column;
      gap: 1rem;
      align-items: flex-start;

      h1 {
        font-size: 1.5rem;
      }
    }

    .exam-meta {
      grid-template-columns: 1fr;
    }

    .exam-settings .settings-grid {
      grid-template-columns: 1fr;
    }

    .exam-actions .start-btn {
      width: 100%;
    }
  }
}
</style>

