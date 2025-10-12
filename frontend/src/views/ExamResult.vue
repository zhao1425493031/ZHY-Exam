<template>
  <div class="exam-result">
    <!-- 顶部导航栏 -->
    <TopNavigation />

    <!-- 考试结果内容 -->
    <div class="result-content">
      <div class="container">
        <!-- 结果头部 -->
        <div class="result-header">
          <div class="result-icon">
            <el-icon v-if="examResult.score >= 60" size="80" class="success-icon">
              <SuccessFilled />
            </el-icon>
            <el-icon v-else size="80" class="fail-icon">
              <CircleCloseFilled />
            </el-icon>
          </div>
          <div class="result-info">
            <h1>{{ examResult.score >= 60 ? '恭喜通过考试！' : '考试未通过' }}</h1>
            <p>{{ exam.title }} - {{ exam.subject_name }}</p>
          </div>
        </div>

        <!-- 成绩统计 -->
        <div class="score-stats">
          <div class="stat-card">
            <div class="stat-value">{{ Math.round(examResult.score) }}</div>
            <div class="stat-label">总分</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ examResult.correct_count }}</div>
            <div class="stat-label">正确题数</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ examResult.total_count }}</div>
            <div class="stat-label">总题数</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ examResult.accuracy }}%</div>
            <div class="stat-label">正确率</div>
          </div>
        </div>

        <!-- 考试详情 -->
        <div class="exam-details">
          <h3>考试详情</h3>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="label">考试时长：</span>
              <span class="value">{{ exam.duration }}分钟</span>
            </div>
            <div class="detail-item">
              <span class="label">实际用时：</span>
              <span class="value">{{ formatDuration(examResult.duration) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">提交时间：</span>
              <span class="value">{{ formatDateTime(examResult.submit_time) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">考试状态：</span>
              <el-tag :type="examResult.score >= 60 ? 'success' : 'danger'">
                {{ examResult.score >= 60 ? '通过' : '未通过' }}
              </el-tag>
            </div>
          </div>
        </div>

        <!-- 题目详情 -->
        <div class="question-details" v-if="examResult.question_details">
          <h3>答题详情</h3>
          <div class="question-list">
            <div 
              v-for="(detail, index) in examResult.question_details" 
              :key="index"
              class="question-item"
              :class="{ 'correct': detail.is_correct, 'incorrect': !detail.is_correct }"
            >
              <div class="question-header">
                <div class="question-number">第{{ index + 1 }}题</div>
                <div class="question-status">
                  <el-icon v-if="detail.is_correct" class="correct-icon">
                    <Check />
                  </el-icon>
                  <el-icon v-else class="incorrect-icon">
                    <Close />
                  </el-icon>
                  <span>{{ detail.is_correct ? '正确' : '错误' }}</span>
                </div>
              </div>
              <div class="question-content">
                <p class="question-title">{{ detail.question_title }}</p>
                <div class="answer-section">
                  <div class="answer-item">
                    <span class="label">您的答案：</span>
                    <span class="value">{{ detail.user_answer || '未作答' }}</span>
                  </div>
                  <div class="answer-item">
                    <span class="label">正确答案：</span>
                    <span class="value correct-answer">{{ detail.correct_answer }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="result-actions">
          <el-button @click="goToExamList" class="action-btn">
            <el-icon><List /></el-icon>
            返回考试列表
          </el-button>
          <el-button @click="goToWrongAnswers" class="action-btn">
            <el-icon><Warning /></el-icon>
            查看错题
          </el-button>
          <el-button type="primary" @click="retakeExam" class="action-btn">
            <el-icon><Refresh /></el-icon>
            重新考试
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { SuccessFilled, CircleCloseFilled, Check, Close, List, Warning, Refresh } from '@element-plus/icons-vue'
import TopNavigation from '@/components/layout/TopNavigation.vue'
import { examApi } from '@/api/exams'

export default {
  name: 'ExamResult',
  components: {
    TopNavigation,
    SuccessFilled,
    CircleCloseFilled,
    Check,
    Close,
    List,
    Warning,
    Refresh
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const exam = ref({})
    const examResult = ref({})

    // 获取考试结果
    const fetchExamResult = async () => {
      try {
        const examId = route.params.id
        const response = await examApi.getExamResult(examId)
        
        if (response.code === 200) {
          examResult.value = response.data
          exam.value = response.data.exam || {}
        } else {
          ElMessage.error('获取考试结果失败')
          router.push('/')
        }
      } catch (error) {
        console.error('获取考试结果失败:', error)
        ElMessage.error('获取考试结果失败')
        router.push('/')
      }
    }

    // 格式化时长
    const formatDuration = (minutes) => {
      if (!minutes) return '0分钟'
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      if (hours > 0) {
        return `${hours}小时${mins}分钟`
      }
      return `${mins}分钟`
    }

    // 格式化日期时间
    const formatDateTime = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
    }

    // 跳转到考试列表
    const goToExamList = () => {
      router.push('/')
    }

    // 跳转到错题管理
    const goToWrongAnswers = () => {
      router.push('/user/wrong-answers')
    }

    // 重新考试
    const retakeExam = () => {
      router.push(`/exam/${exam.value.id}`)
    }

    onMounted(() => {
      fetchExamResult()
    })

    return {
      exam,
      examResult,
      formatDuration,
      formatDateTime,
      goToExamList,
      goToWrongAnswers,
      retakeExam
    }
  }
}
</script>

<style lang="scss" scoped>
.exam-result {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.result-content {
  padding: 2rem 0;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  background: white;
  border-radius: 20px;
  padding: 3rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);

  .result-icon {
    .success-icon {
      color: #67c23a;
    }

    .fail-icon {
      color: #f56c6c;
    }
  }

  .result-info {
    flex: 1;

    h1 {
      font-size: 2.5rem;
      font-weight: 800;
      margin: 0 0 1rem 0;
      color: #333;
    }

    p {
      font-size: 1.2rem;
      color: #666;
      margin: 0;
    }
  }
}

.score-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;

  .stat-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-5px);
    }

    .stat-value {
      font-size: 3rem;
      font-weight: 800;
      color: var(--theme-primary, #667eea);
      margin-bottom: 0.5rem;
    }

    .stat-label {
      font-size: 1.1rem;
      color: #666;
      font-weight: 600;
    }
  }
}

.exam-details,
.question-details {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);

  h3 {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 2rem 0;
    color: #333;
  }
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;

  .detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: #f8f9fa;
    border-radius: 12px;

    .label {
      font-weight: 600;
      color: #666;
    }

    .value {
      font-weight: 700;
      color: #333;
    }
  }
}

.question-list {
  .question-item {
    border: 2px solid #e9ecef;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;

    &.correct {
      border-color: #67c23a;
      background: rgba(103, 194, 58, 0.05);
    }

    &.incorrect {
      border-color: #f56c6c;
      background: rgba(245, 108, 108, 0.05);
    }

    .question-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;

      .question-number {
        font-weight: 700;
        color: #333;
        font-size: 1.1rem;
      }

      .question-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;

        .correct-icon {
          color: #67c23a;
        }

        .incorrect-icon {
          color: #f56c6c;
        }
      }
    }

    .question-content {
      .question-title {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #555;
        margin-bottom: 1rem;
      }

      .answer-section {
        display: grid;
        gap: 0.8rem;

        .answer-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;

          .label {
            font-weight: 600;
            color: #666;
            min-width: 80px;
          }

          .value {
            color: #333;
          }

          .correct-answer {
            color: #67c23a;
            font-weight: 700;
          }
        }
      }
    }
  }
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);

  .action-btn {
    border-radius: 12px;
    padding: 1rem 2rem;
    font-weight: 600;
    font-size: 1.1rem;

    &:hover {
      transform: translateY(-2px);
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .result-header {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }

  .score-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .result-actions {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
