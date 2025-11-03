<template>
  <div class="exam-taking">
    <!-- 考试头部 -->
    <div class="exam-header">
      <div class="header-left">
        <h1>{{ exam.title }}</h1>
        <div class="exam-info">
          <span>{{ exam.question_count }}题 | {{ exam.total_points }}分</span>
        </div>
      </div>
      <div class="header-right">
        <div class="timer-section">
          <div class="timer-display">
            <el-icon><Timer /></el-icon>
            <span class="timer-text">{{ formatTime(remainingTime) }}</span>
          </div>
          <div class="timer-progress">
            <el-progress
              :percentage="timeProgress"
              :color="getTimerColor(timeProgress)"
              :show-text="false"
            />
          </div>
        </div>
        <div class="exam-actions">
          <el-button @click="pauseExam" :disabled="isPaused">
            <el-icon><VideoPause /></el-icon>
            {{ isPaused ? '已暂停' : '暂停' }}
          </el-button>
          <el-button type="primary" @click="submitExam">
            <el-icon><Check /></el-icon>
            提交考试
          </el-button>
        </div>
      </div>
    </div>

    <!-- 考试内容 -->
    <div class="exam-content">
      <div class="content-left">
        <!-- 题目区域 -->
        <div class="question-area">
          <div class="question-header">
            <div class="question-nav">
              <el-button
                v-if="currentQuestionIndex > 0"
                @click="previousQuestion"
                :disabled="isSubmitting"
              >
                <el-icon><ArrowLeft /></el-icon>
                上一题
              </el-button>
              <span class="question-counter">
                第 {{ currentQuestionIndex + 1 }} 题 / 共 {{ questions.length }} 题
              </span>
              <el-button
                v-if="currentQuestionIndex < questions.length - 1"
                @click="nextQuestion"
                :disabled="isSubmitting"
              >
                下一题
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
            <div class="question-type">
              <el-tag :type="getTypeTagType(currentQuestion.type)" size="small">
                {{ getTypeLabel(currentQuestion.type) }}
              </el-tag>
              <span class="question-points">{{ currentQuestion.points }}分</span>
            </div>
          </div>

          <div class="question-content">
            <div class="question-title">
              <h3>{{ currentQuestion.title }}</h3>
            </div>
            
            <div v-if="currentQuestion.content" class="question-description">
              <p>{{ currentQuestion.content }}</p>
            </div>

            <!-- 单选题 -->
            <div v-if="currentQuestion.type === 'single'" class="question-options">
              <el-radio-group
                v-model="answers[currentQuestionIndex]"
                @change="saveAnswer"
              >
                <div
                  v-for="(option, index) in currentQuestion.options"
                  :key="index"
                  class="option-item"
                >
                  <el-radio :value="String.fromCharCode(65 + index)">
                    {{ String.fromCharCode(65 + index) }}. {{ option }}
                  </el-radio>
                </div>
              </el-radio-group>
            </div>

            <!-- 多选题 -->
            <div v-if="currentQuestion.type === 'multiple'" class="question-options">
              <el-checkbox-group
                v-model="answers[currentQuestionIndex]"
                @change="saveAnswer"
              >
                <div
                  v-for="(option, index) in currentQuestion.options"
                  :key="index"
                  class="option-item"
                >
                  <el-checkbox :value="String.fromCharCode(65 + index)">
                    {{ String.fromCharCode(65 + index) }}. {{ option }}
                  </el-checkbox>
                </div>
              </el-checkbox-group>
            </div>

            <!-- 判断题 -->
            <div v-if="currentQuestion.type === 'judge'" class="question-options">
              <el-radio-group
                v-model="answers[currentQuestionIndex]"
                @change="saveAnswer"
              >
                <div class="option-item">
                  <el-radio value="true">正确</el-radio>
                </div>
                <div class="option-item">
                  <el-radio value="false">错误</el-radio>
                </div>
              </el-radio-group>
            </div>

            <!-- 填空题 -->
            <div v-if="currentQuestion.type === 'fill'" class="question-options">
              <el-input
                v-model="answers[currentQuestionIndex]"
                type="textarea"
                :rows="4"
                placeholder="请输入答案"
                @input="saveAnswer"
              />
            </div>

            <!-- 简答题 -->
            <div v-if="currentQuestion.type === 'essay'" class="question-options">
              <el-input
                v-model="answers[currentQuestionIndex]"
                type="textarea"
                :rows="8"
                placeholder="请输入答案"
                @input="saveAnswer"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="content-right">
        <!-- 答题卡 -->
        <div class="answer-sheet">
          <div class="sheet-header">
            <h4>答题卡</h4>
            <div class="sheet-stats">
              <span>已答：{{ answeredCount }}/{{ questions.length }}</span>
            </div>
          </div>
          <div class="sheet-content">
            <div class="question-grid">
              <div
                v-for="(question, index) in questions"
                :key="question.id"
                class="question-item"
                :class="{
                  'item-current': index === currentQuestionIndex,
                  'item-answered': answers[index] && answers[index].length > 0,
                  'item-marked': markedQuestions.includes(index)
                }"
                @click="goToQuestion(index)"
              >
                {{ index + 1 }}
              </div>
            </div>
          </div>
          <div class="sheet-legend">
            <div class="legend-item">
              <span class="legend-color current"></span>
              <span>当前题目</span>
            </div>
            <div class="legend-item">
              <span class="legend-color answered"></span>
              <span>已答题</span>
            </div>
            <div class="legend-item">
              <span class="legend-color marked"></span>
              <span>标记题目</span>
            </div>
            <div class="legend-item">
              <span class="legend-color unanswered"></span>
              <span>未答题</span>
            </div>
          </div>
        </div>

        <!-- 考试信息 -->
        <div class="exam-info-card">
          <div class="info-header">
            <h4>考试信息</h4>
          </div>
          <div class="info-content">
            <div class="info-item">
              <span class="info-label">考试时长：</span>
              <span class="info-value">{{ formatDuration(exam.duration) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">剩余时间：</span>
              <span class="info-value">{{ formatTime(remainingTime) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">已答题目：</span>
              <span class="info-value">{{ answeredCount }}/{{ questions.length }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">标记题目：</span>
              <span class="info-value">{{ markedQuestions.length }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 提交确认对话框 -->
    <el-dialog
      v-model="showSubmitDialog"
      title="提交考试"
      width="50%"
      :close-on-click-modal="false"
    >
      <div class="submit-content">
        <div class="submit-warning">
          <el-icon color="#e6a23c"><Warning /></el-icon>
          <span>提交后将无法修改答案，请确认是否提交？</span>
        </div>
        
        <div class="submit-stats">
          <div class="stat-item">
            <span class="stat-label">已答题目：</span>
            <span class="stat-value">{{ answeredCount }}/{{ questions.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">未答题目：</span>
            <span class="stat-value">{{ questions.length - answeredCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">标记题目：</span>
            <span class="stat-value">{{ markedQuestions.length }}</span>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showSubmitDialog = false">取消</el-button>
          <el-button type="primary" @click="confirmSubmit" :loading="isSubmitting">
            确认提交
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Timer, VideoPause, Check, ArrowLeft, ArrowRight, Warning
} from '@element-plus/icons-vue'
import { examApi } from '@/api/exams'
import { formatDate, formatDuration } from '@/utils/format'

export default {
  name: 'ExamTaking',
  components: {
    Timer,
    VideoPause,
    Check,
    ArrowLeft,
    ArrowRight,
    Warning
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    // 响应式数据
    const exam = ref({})
    const questions = ref([])
    const answers = ref([])
    const markedQuestions = ref([])
    const currentQuestionIndex = ref(0)
    const remainingTime = ref(0)
    const isPaused = ref(false)
    const isSubmitting = ref(false)
    const showSubmitDialog = ref(false)
    const timer = ref(null)
    
    // 计算属性
    const currentQuestion = computed(() => {
      return questions.value[currentQuestionIndex.value] || {}
    })
    
    const answeredCount = computed(() => {
      return answers.value.filter(answer => answer && answer.length > 0).length
    })
    
    const timeProgress = computed(() => {
      if (exam.value.duration <= 0) return 0
      return Math.round(((exam.value.duration - remainingTime.value) / exam.value.duration) * 100)
    })
    
    // 方法
    const loadExam = async () => {
      try {
        const examId = route.params.id
        const response = await examApi.getExam(examId)
        exam.value = response.data
        
        // getExam已经返回了questions数组，直接使用
        questions.value = response.data.questions || []
        
        // 初始化答案数组
        answers.value = new Array(questions.value.length).fill('')
        
        // 开始计时
        startTimer()
        
        // 检查是否已有考试记录
        await checkExamRecord()
      } catch (error) {
        ElMessage.error('加载考试失败')
        console.error('Load exam error:', error)
        router.push('/user/exams')
      }
    }
    
    const checkExamRecord = async () => {
      try {
        // TODO: 检查是否已有考试记录
        // const response = await examApi.getExamRecord(exam.value.id)
        // if (response.data && response.data.status === 'submitted') {
        //   ElMessage.warning('您已经参加过此考试')
        //   router.push(`/user/exam-result/${exam.value.id}`)
        // }
      } catch (error) {
        console.error('Check exam record error:', error)
      }
    }
    
    const startTimer = () => {
      remainingTime.value = exam.value.duration * 60 // 转换为秒
      
      timer.value = setInterval(() => {
        if (!isPaused.value && remainingTime.value > 0) {
          remainingTime.value--
          
          // 时间不足提醒
          if (remainingTime.value === 300) { // 5分钟
            ElMessage.warning('考试还剩5分钟，请抓紧时间答题')
          } else if (remainingTime.value === 60) { // 1分钟
            ElMessage.error('考试还剩1分钟，请尽快提交')
          }
        } else if (remainingTime.value <= 0) {
          // 时间到，自动提交
          autoSubmit()
        }
      }, 1000)
    }
    
    const pauseExam = () => {
      isPaused.value = !isPaused.value
      ElMessage.info(isPaused.value ? '考试已暂停' : '考试已恢复')
    }
    
    const saveAnswer = () => {
      // TODO: 保存答案到后端
      // examApi.saveAnswer(exam.value.id, {
      //   question_id: currentQuestion.value.id,
      //   answer: answers.value[currentQuestionIndex.value]
      // })
    }
    
    const previousQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--
      }
    }
    
    const nextQuestion = () => {
      if (currentQuestionIndex.value < questions.value.length - 1) {
        currentQuestionIndex.value++
      }
    }
    
    const goToQuestion = (index) => {
      currentQuestionIndex.value = index
    }
    
    const submitExam = () => {
      showSubmitDialog.value = true
    }
    
    const confirmSubmit = async () => {
      try {
        isSubmitting.value = true
        showSubmitDialog.value = false
        
        // 提交考试
        const submitData = {
          answers: answers.value,
          submit_time: new Date().toISOString()
        }
        
        await examApi.submitExam(exam.value.id, submitData)
        
        ElMessage.success('考试提交成功')
        router.push(`/user/exam-result/${exam.value.id}`)
      } catch (error) {
        ElMessage.error('提交考试失败')
        console.error('Submit exam error:', error)
      } finally {
        isSubmitting.value = false
      }
    }
    
    const autoSubmit = async () => {
      try {
        await ElMessageBox.confirm(
          '考试时间已到，系统将自动提交您的答案',
          '时间到',
          {
            confirmButtonText: '确定',
            showCancelButton: false,
            type: 'warning'
          }
        )
        
        await confirmSubmit()
      } catch (error) {
        // 用户点击确定，继续提交
        await confirmSubmit()
      }
    }
    
    // 工具方法
    const formatTime = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      
      if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`
      }
    }
    
    const getTimerColor = (percentage) => {
      if (percentage >= 90) return '#f56c6c'
      if (percentage >= 70) return '#e6a23c'
      return '#67c23a'
    }
    
    const getTypeLabel = (type) => {
      const labels = {
        single: '单选题',
        multiple: '多选题',
        judge: '判断题',
        fill: '填空题',
        essay: '简答题'
      }
      return labels[type] || type
    }
    
    const getTypeTagType = (type) => {
      const types = {
        single: 'primary',
        multiple: 'success',
        judge: 'warning',
        fill: 'info',
        essay: 'danger'
      }
      return types[type] || 'default'
    }
    
    // 生命周期
    onMounted(() => {
      loadExam()
    })
    
    onUnmounted(() => {
      if (timer.value) {
        clearInterval(timer.value)
      }
    })
    
    return {
      exam,
      questions,
      answers,
      markedQuestions,
      currentQuestionIndex,
      remainingTime,
      isPaused,
      isSubmitting,
      showSubmitDialog,
      currentQuestion,
      answeredCount,
      timeProgress,
      pauseExam,
      saveAnswer,
      previousQuestion,
      nextQuestion,
      goToQuestion,
      submitExam,
      confirmSubmit,
      formatTime,
      getTimerColor,
      getTypeLabel,
      getTypeTagType,
      formatDuration
    }
  }
}
</script>

<style scoped>
.exam-taking {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #fff;
  border-bottom: 1px solid #ebeef5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left h1 {
  margin: 0 0 5px 0;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
}

.exam-info {
  color: #909399;
  font-size: 14px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.timer-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.timer-display {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 18px;
  font-weight: 600;
  color: #e6a23c;
}

.timer-text {
  font-family: 'Courier New', monospace;
}

.timer-progress {
  width: 200px;
}

.exam-actions {
  display: flex;
  gap: 10px;
}

.exam-content {
  flex: 1;
  display: flex;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
}

.content-left {
  flex: 2;
  display: flex;
  flex-direction: column;
}

.content-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-area {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  overflow-y: auto;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.question-nav {
  display: flex;
  align-items: center;
  gap: 15px;
}

.question-counter {
  color: #606266;
  font-weight: 500;
}

.question-type {
  display: flex;
  align-items: center;
  gap: 10px;
}

.question-points {
  color: #e6a23c;
  font-weight: 500;
}

.question-content {
  line-height: 1.6;
}

.question-title h3 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 18px;
  font-weight: 500;
}

.question-description {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.question-description p {
  margin: 0;
  color: #606266;
}

.question-options {
  margin-top: 20px;
}

.option-item {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.option-item:hover {
  background-color: #f5f7fa;
}

.answer-sheet {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
}

.sheet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.sheet-header h4 {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.sheet-stats {
  color: #909399;
  font-size: 14px;
}

.question-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-bottom: 15px;
}

.question-item {
  width: 40px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.question-item:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.item-current {
  border-color: #409eff;
  background-color: #409eff;
  color: #fff;
}

.item-answered {
  border-color: #67c23a;
  background-color: #67c23a;
  color: #fff;
}

.item-marked {
  border-color: #e6a23c;
  background-color: #e6a23c;
  color: #fff;
}

.sheet-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #606266;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.legend-color.current {
  background-color: #409eff;
}

.legend-color.answered {
  background-color: #67c23a;
}

.legend-color.marked {
  background-color: #e6a23c;
}

.legend-color.unanswered {
  background-color: #e4e7ed;
}

.exam-info-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
}

.info-header h4 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-label {
  color: #606266;
}

.info-value {
  color: #303133;
  font-weight: 500;
}

.submit-content {
  padding: 20px 0;
}

.submit-warning {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fef0e6;
  border-radius: 6px;
  border-left: 4px solid #e6a23c;
  color: #e6a23c;
}

.submit-stats {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-label {
  color: #606266;
}

.stat-value {
  color: #303133;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .exam-content {
    flex-direction: column;
    padding: 15px;
  }
  
  .content-right {
    order: -1;
  }
  
  .question-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .header-right {
    flex-direction: column;
    gap: 10px;
  }
  
  .timer-progress {
    width: 150px;
  }
}
</style>
