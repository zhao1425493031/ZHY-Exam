<template>
  <div class="exam-taking">
    <!-- 顶部导航栏 -->
    <TopNavigation />

    <!-- 考试内容区域 -->
    <div class="exam-content">
      <div class="container">
        <!-- 考试头部信息 -->
        <div class="exam-header">
          <div class="exam-info">
            <h1>{{ exam.title }}</h1>
            <p>{{ exam.subject_name }}</p>
          </div>
          <div class="exam-timer">
            <el-icon><Clock /></el-icon>
            <span>{{ formatTime(remainingTime) }}</span>
          </div>
        </div>

        <!-- 考试进度 -->
        <div class="exam-progress">
          <el-progress 
            :percentage="progressPercentage" 
            :color="getProgressColor(progressPercentage)"
            :stroke-width="8"
          />
          <span class="progress-text">{{ currentQuestionIndex + 1 }} / {{ exam.question_count }}</span>
        </div>

        <!-- 题目内容 -->
        <div class="question-content" v-if="currentQuestion">
          <div class="question-header">
            <h3>{{ currentQuestion.title }}</h3>
            <div class="question-meta">
              <el-tag :type="getQuestionTypeTag(currentQuestion.type)">
                {{ getQuestionTypeText(currentQuestion.type) }}
              </el-tag>
              <span class="question-points">{{ currentQuestion.points }}分</span>
            </div>
          </div>

          <div class="question-body">
            <p v-if="currentQuestion.content">{{ currentQuestion.content }}</p>
            
            <!-- 选择题选项 -->
            <div v-if="['single', 'multiple'].includes(currentQuestion.type)" class="question-options">
              <div 
                v-for="(option, index) in currentQuestion.options" 
                :key="index"
                class="option-item"
                :class="{ 'selected': isOptionSelected(index) }"
                @click="selectOption(index)"
              >
                <div class="option-label">{{ String.fromCharCode(65 + index) }}</div>
                <div class="option-content">{{ option }}</div>
              </div>
            </div>

            <!-- 判断题 -->
            <div v-if="currentQuestion.type === 'judge'" class="judge-options">
              <div 
                class="judge-item"
                :class="{ 'selected': userAnswers[currentQuestionIndex] === 'true' }"
                @click="selectJudgeAnswer('true')"
              >
                <el-icon><Check /></el-icon>
                <span>正确</span>
              </div>
              <div 
                class="judge-item"
                :class="{ 'selected': userAnswers[currentQuestionIndex] === 'false' }"
                @click="selectJudgeAnswer('false')"
              >
                <el-icon><Close /></el-icon>
                <span>错误</span>
              </div>
            </div>

            <!-- 填空题 -->
            <div v-if="currentQuestion.type === 'fill'" class="fill-answer">
              <el-input
                v-model="userAnswers[currentQuestionIndex]"
                type="textarea"
                :rows="4"
                placeholder="请输入您的答案..."
                class="fill-input"
              />
            </div>

            <!-- 简答题 -->
            <div v-if="currentQuestion.type === 'essay'" class="essay-answer">
              <el-input
                v-model="userAnswers[currentQuestionIndex]"
                type="textarea"
                :rows="6"
                placeholder="请输入您的答案..."
                class="essay-input"
              />
            </div>
          </div>
        </div>

        <!-- 考试操作按钮 -->
        <div class="exam-actions">
          <el-button 
            :disabled="currentQuestionIndex === 0"
            @click="previousQuestion"
            class="action-btn"
          >
            <el-icon><ArrowLeft /></el-icon>
            上一题
          </el-button>
          
          <el-button 
            v-if="currentQuestionIndex < exam.question_count - 1"
            type="primary"
            @click="nextQuestion"
            class="action-btn"
          >
            下一题
            <el-icon><ArrowRight /></el-icon>
          </el-button>
          
          <el-button 
            v-else
            type="success"
            @click="submitExam"
            class="action-btn submit-btn"
          >
            <el-icon><Check /></el-icon>
            提交考试
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Clock, Check, Close, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import TopNavigation from '@/components/layout/TopNavigation.vue'
import { examApi } from '@/api/exams'

export default {
  name: 'ExamTaking',
  components: {
    TopNavigation,
    Clock,
    Check,
    Close,
    ArrowLeft,
    ArrowRight
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const exam = ref({})
    const questions = ref([])
    const currentQuestionIndex = ref(0)
    const userAnswers = ref({})
    const remainingTime = ref(0)
    const examStartTime = ref(null)
    const timer = ref(null)

    // 计算属性
    const currentQuestion = computed(() => {
      return questions.value[currentQuestionIndex.value] || null
    })

    const progressPercentage = computed(() => {
      return Math.round(((currentQuestionIndex.value + 1) / exam.value.question_count) * 100)
    })

    // 获取考试数据
    const fetchExam = async () => {
      try {
        const examId = route.params.id
        const response = await examApi.getExam(examId)
        
        if (response.code === 200) {
          exam.value = response.data
          questions.value = response.data.questions || []
          remainingTime.value = exam.value.duration * 60 // 转换为秒
          examStartTime.value = new Date()
          startTimer()
        } else {
          ElMessage.error('获取考试信息失败')
          router.push('/')
        }
      } catch (error) {
        console.error('获取考试失败:', error)
        ElMessage.error('获取考试信息失败')
        router.push('/')
      }
    }

    // 开始计时器
    const startTimer = () => {
      timer.value = setInterval(() => {
        remainingTime.value--
        if (remainingTime.value <= 0) {
          submitExam()
        }
      }, 1000)
    }

    // 格式化时间
    const formatTime = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      
      if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      }
      return `${minutes}:${secs.toString().padStart(2, '0')}`
    }

    // 获取进度条颜色
    const getProgressColor = (percentage) => {
      if (percentage >= 80) return '#67c23a'
      if (percentage >= 60) return '#e6a23c'
      return '#f56c6c'
    }

    // 获取题目类型标签
    const getQuestionTypeTag = (type) => {
      const typeMap = {
        'single': 'primary',
        'multiple': 'success',
        'judge': 'warning',
        'fill': 'info',
        'essay': 'danger'
      }
      return typeMap[type] || 'info'
    }

    // 获取题目类型文本
    const getQuestionTypeText = (type) => {
      const typeMap = {
        'single': '单选题',
        'multiple': '多选题',
        'judge': '判断题',
        'fill': '填空题',
        'essay': '简答题'
      }
      return typeMap[type] || '未知'
    }

    // 选择选项
    const selectOption = (index) => {
      const currentAnswer = userAnswers.value[currentQuestionIndex.value]
      const optionValue = String.fromCharCode(65 + index)
      
      if (currentQuestion.value.type === 'single') {
        userAnswers.value[currentQuestionIndex.value] = optionValue
      } else if (currentQuestion.value.type === 'multiple') {
        const answers = currentAnswer ? currentAnswer.split('') : []
        if (answers.includes(optionValue)) {
          answers.splice(answers.indexOf(optionValue), 1)
        } else {
          answers.push(optionValue)
        }
        userAnswers.value[currentQuestionIndex.value] = answers.sort().join('')
      }
    }

    // 判断选项是否被选中
    const isOptionSelected = (index) => {
      const currentAnswer = userAnswers.value[currentQuestionIndex.value]
      const optionValue = String.fromCharCode(65 + index)
      
      if (currentQuestion.value.type === 'single') {
        return currentAnswer === optionValue
      } else if (currentQuestion.value.type === 'multiple') {
        return currentAnswer && currentAnswer.includes(optionValue)
      }
      return false
    }

    // 选择判断题答案
    const selectJudgeAnswer = (answer) => {
      userAnswers.value[currentQuestionIndex.value] = answer
    }

    // 上一题
    const previousQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--
      }
    }

    // 下一题
    const nextQuestion = () => {
      if (currentQuestionIndex.value < exam.value.question_count - 1) {
        currentQuestionIndex.value++
      }
    }

    // 提交考试
    const submitExam = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要提交考试吗？提交后将无法修改答案。',
          '确认提交',
          {
            confirmButtonText: '确定提交',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        // 停止计时器
        if (timer.value) {
          clearInterval(timer.value)
        }

        // 提交答案
        const submitData = {
          exam_id: exam.value.id,
          answers: userAnswers.value,
          submit_time: new Date().toISOString()
        }

        const response = await examApi.submitExam(submitData)
        
        if (response.code === 200) {
          ElMessage.success('考试提交成功！')
          router.push(`/exam/result/${exam.value.id}`)
        } else {
          ElMessage.error('考试提交失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('提交考试失败:', error)
          ElMessage.error('考试提交失败')
        }
      }
    }

    onMounted(() => {
      fetchExam()
    })

    // 组件卸载时清理计时器
    const cleanup = () => {
      if (timer.value) {
        clearInterval(timer.value)
      }
    }

    return {
      exam,
      questions,
      currentQuestionIndex,
      userAnswers,
      remainingTime,
      currentQuestion,
      progressPercentage,
      formatTime,
      getProgressColor,
      getQuestionTypeTag,
      getQuestionTypeText,
      selectOption,
      isOptionSelected,
      selectJudgeAnswer,
      previousQuestion,
      nextQuestion,
      submitExam,
      cleanup
    }
  },
  beforeUnmount() {
    this.cleanup()
  }
}
</script>

<style lang="scss" scoped>
.exam-taking {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.exam-content {
  padding: 2rem 0;
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);

  .exam-info {
    h1 {
      font-size: 2rem;
      font-weight: 800;
      margin: 0 0 0.5rem 0;
      color: #333;
      background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    p {
      color: #666;
      margin: 0;
      font-size: 1.1rem;
    }
  }

  .exam-timer {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    font-size: 1.2rem;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
  }
}

.exam-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  border-radius: 20px;
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);

  :deep(.el-progress) {
    flex: 1;
  }

  .progress-text {
    font-weight: 600;
    color: #666;
    min-width: 80px;
    text-align: right;
  }
}

.question-content {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);

  .question-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 2rem;

    h3 {
      font-size: 1.5rem;
      font-weight: 700;
      margin: 0;
      color: #333;
      line-height: 1.4;
      flex: 1;
      margin-right: 2rem;
    }

    .question-meta {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      align-items: flex-end;

      .question-points {
        font-weight: 600;
        color: var(--theme-primary, #667eea);
        font-size: 1.1rem;
      }
    }
  }

  .question-body {
    p {
      font-size: 1.1rem;
      line-height: 1.6;
      color: #555;
      margin-bottom: 2rem;
    }
  }
}

.question-options {
  display: grid;
  gap: 1rem;

  .option-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.5rem;
    border: 2px solid #e9ecef;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      border-color: var(--theme-primary, #667eea);
      background: rgba(102, 126, 234, 0.05);
    }

    &.selected {
      border-color: var(--theme-primary, #667eea);
      background: rgba(102, 126, 234, 0.1);
    }

    .option-label {
      width: 40px;
      height: 40px;
      background: var(--theme-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 1.1rem;
    }

    .option-content {
      flex: 1;
      font-size: 1.1rem;
      line-height: 1.5;
    }
  }
}

.judge-options {
  display: flex;
  gap: 2rem;

  .judge-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 2rem;
    border: 2px solid #e9ecef;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1.1rem;
    font-weight: 600;

    &:hover {
      border-color: var(--theme-primary, #667eea);
      background: rgba(102, 126, 234, 0.05);
    }

    &.selected {
      border-color: var(--theme-primary, #667eea);
      background: rgba(102, 126, 234, 0.1);
      color: var(--theme-primary, #667eea);
    }
  }
}

.fill-input,
.essay-input {
  :deep(.el-textarea__inner) {
    border-radius: 12px;
    border: 2px solid #e9ecef;
    font-size: 1.1rem;
    line-height: 1.6;

    &:focus {
      border-color: var(--theme-primary, #667eea);
    }
  }
}

.exam-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border-radius: 20px;
  padding: 1.5rem 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);

  .action-btn {
    border-radius: 12px;
    padding: 1rem 2rem;
    font-weight: 600;
    font-size: 1.1rem;

    &.submit-btn {
      background: var(--theme-gradient, linear-gradient(135deg, #67c23a 0%, #85ce61 100%));
      border: none;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(103, 194, 58, 0.3);
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .exam-header {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }

  .question-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;

    h3 {
      margin-right: 0;
    }

    .question-meta {
      align-items: flex-start;
    }
  }

  .judge-options {
    flex-direction: column;
    gap: 1rem;
  }

  .exam-actions {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
