<template>
  <div class="review-mode">
    <div class="review-header">
      <div class="header-left">
        <h2>错题复习</h2>
        <div class="progress-info">
          <span>第 {{ currentIndex + 1 }} 题 / 共 {{ questions.length }} 题</span>
        </div>
      </div>
      <div class="header-right">
        <div class="progress-bar">
          <el-progress
            :percentage="Math.round((currentIndex + 1) / questions.length * 100)"
            :color="getProgressColor(currentIndex / questions.length)"
          />
        </div>
        <div class="review-actions">
          <el-button @click="handleClose">退出复习</el-button>
          <el-button type="primary" @click="toggleAnswerMode">
            {{ showAnswer ? '隐藏答案' : '显示答案' }}
          </el-button>
        </div>
      </div>
    </div>

    <div class="review-content">
      <div class="question-area">
        <!-- 题目内容 -->
        <div class="question-content">
          <div class="question-header">
            <div class="question-type">
              <el-tag :type="getTypeTagType(currentQuestion.question_type)" size="small">
                {{ getTypeLabel(currentQuestion.question_type) }}
              </el-tag>
              <span class="question-points">{{ currentQuestion.question_points || currentQuestion.points || 1 }}分</span>
            </div>
          </div>
          
          <div class="question-title">
            <h3>{{ currentQuestion.question_title }}</h3>
          </div>
          
          <div v-if="currentQuestion.question_content" class="question-description">
            <p>{{ currentQuestion.question_content }}</p>
          </div>

          <!-- 选项（选择题） -->
          <div v-if="isChoiceQuestion" class="question-options">
            <div
              v-for="(option, index) in currentQuestion.options"
              :key="index"
              class="option-item"
              :class="getOptionClass(index)"
            >
              <div class="option-label">{{ String.fromCharCode(65 + index) }}</div>
              <div class="option-content">{{ option }}</div>
            </div>
          </div>
        </div>

        <!-- 答案区域 -->
        <div v-if="showAnswer" class="answer-area">
          <div class="answer-section">
            <div class="answer-item">
              <div class="answer-label">
                <el-icon color="#f56c6c"><Close /></el-icon>
                我的答案
              </div>
              <div class="answer-value user-answer">
                {{ currentQuestion.user_answer || '未作答' }}
              </div>
            </div>
            <div class="answer-item">
              <div class="answer-label">
                <el-icon color="#67c23a"><Check /></el-icon>
                正确答案
              </div>
              <div class="answer-value correct-answer">
                {{ currentQuestion.correct_answer }}
              </div>
            </div>
          </div>
          
          <div v-if="currentQuestion.explanation" class="explanation-section">
            <div class="explanation-header">
              <h4>题目解析</h4>
            </div>
            <div class="explanation-content">
              <p>{{ currentQuestion.explanation }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 复习控制面板 -->
      <div class="review-panel">
        <div class="panel-section">
          <h4>复习控制</h4>
          <div class="control-buttons">
            <el-button
              v-if="currentIndex > 0"
              @click="previousQuestion"
              :disabled="isSubmitting"
            >
              <el-icon><ArrowLeft /></el-icon>
              上一题
            </el-button>
            <el-button
              v-if="currentIndex < questions.length - 1"
              @click="nextQuestion"
              :disabled="isSubmitting"
            >
              下一题
              <el-icon><ArrowRight /></el-icon>
            </el-button>
            <el-button
              v-if="currentIndex === questions.length - 1"
              type="success"
              @click="completeReview"
              :loading="isSubmitting"
            >
              <el-icon><Check /></el-icon>
              完成复习
            </el-button>
          </div>
        </div>

        <div class="panel-section">
          <h4>复习状态</h4>
          <div class="status-list">
            <div
              v-for="(question, index) in questions"
              :key="question.id"
              class="status-item"
              :class="{
                'status-current': index === currentIndex,
                'status-reviewed': question.is_reviewed,
                'status-pending': !question.is_reviewed
              }"
              @click="goToQuestion(index)"
            >
              {{ index + 1 }}
            </div>
          </div>
        </div>

        <div class="panel-section">
          <h4>复习统计</h4>
          <div class="stats-content">
            <div class="stat-item">
              <span class="stat-label">总题数：</span>
              <span class="stat-value">{{ questions.length }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">已复习：</span>
              <span class="stat-value">{{ reviewedCount }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">复习率：</span>
              <span class="stat-value">{{ reviewRate }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Check, Close, ArrowLeft, ArrowRight
} from '@element-plus/icons-vue'
import { examScoringApi } from '@/api/exam_scoring'

export default {
  name: 'ReviewMode',
  components: {
    Check,
    Close,
    ArrowLeft,
    ArrowRight
  },
  props: {
    questions: {
      type: Array,
      required: true
    }
  },
  emits: ['complete', 'close'],
  setup(props, { emit }) {
    // 响应式数据
    const currentIndex = ref(0)
    const showAnswer = ref(false)
    const isSubmitting = ref(false)
    
    // 计算属性
    const currentQuestion = computed(() => {
      return props.questions[currentIndex.value] || {}
    })
    
    const isChoiceQuestion = computed(() => {
      return ['single', 'multiple'].includes(currentQuestion.value.question_type)
    })
    
    const reviewedCount = computed(() => {
      return props.questions.filter(q => q.is_reviewed).length
    })
    
    const reviewRate = computed(() => {
      return props.questions.length > 0 ? 
        Math.round(reviewedCount.value / props.questions.length * 100) : 0
    })
    
    // 方法
    const getOptionClass = (index) => {
      if (!showAnswer.value) return ''
      
      const optionLetter = String.fromCharCode(65 + index)
      const isUserAnswer = currentQuestion.value.user_answer && 
        currentQuestion.value.user_answer.includes(optionLetter)
      const isCorrectAnswer = currentQuestion.value.correct_answer && 
        currentQuestion.value.correct_answer.includes(optionLetter)
      
      if (isCorrectAnswer) {
        return 'option-correct'
      } else if (isUserAnswer && !isCorrectAnswer) {
        return 'option-wrong'
      }
      return ''
    }
    
    const previousQuestion = () => {
      if (currentIndex.value > 0) {
        currentIndex.value--
        showAnswer.value = false
      }
    }
    
    const nextQuestion = () => {
      if (currentIndex.value < props.questions.length - 1) {
        currentIndex.value++
        showAnswer.value = false
      }
    }
    
    const goToQuestion = (index) => {
      currentIndex.value = index
      showAnswer.value = false
    }
    
    const toggleAnswerMode = () => {
      showAnswer.value = !showAnswer.value
    }
    
    const markAsReviewed = async () => {
      try {
        await examScoringApi.reviewWrongAnswer(currentQuestion.value.id)
        currentQuestion.value.is_reviewed = true
      } catch (error) {
        console.error('Mark as reviewed error:', error)
      }
    }
    
    const completeReview = async () => {
      try {
        isSubmitting.value = true
        
        // 标记当前题目为已复习
        if (!currentQuestion.value.is_reviewed) {
          await markAsReviewed()
        }
        
        ElMessage.success('复习完成！')
        emit('complete')
      } catch (error) {
        ElMessage.error('完成复习失败')
        console.error('Complete review error:', error)
      } finally {
        isSubmitting.value = false
      }
    }
    
    const handleClose = () => {
      emit('close')
    }
    
    // 工具方法
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
    
    const getProgressColor = (rate) => {
      if (rate >= 0.8) return '#67c23a'
      if (rate >= 0.6) return '#409eff'
      if (rate >= 0.4) return '#e6a23c'
      return '#f56c6c'
    }
    
    // 生命周期
    onMounted(() => {
      // 自动标记第一题为已复习
      if (props.questions.length > 0 && !props.questions[0].is_reviewed) {
        markAsReviewed()
      }
    })
    
    return {
      currentIndex,
      showAnswer,
      isSubmitting,
      currentQuestion,
      isChoiceQuestion,
      reviewedCount,
      reviewRate,
      getOptionClass,
      previousQuestion,
      nextQuestion,
      goToQuestion,
      toggleAnswerMode,
      completeReview,
      handleClose,
      getTypeLabel,
      getTypeTagType,
      getProgressColor
    }
  }
}
</script>

<style scoped>
.review-mode {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #fff;
  border-bottom: 1px solid #ebeef5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left h2 {
  margin: 0 0 5px 0;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
}

.progress-info {
  color: #909399;
  font-size: 14px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.progress-bar {
  width: 200px;
}

.review-actions {
  display: flex;
  gap: 10px;
}

.review-content {
  flex: 1;
  display: flex;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
}

.question-area {
  flex: 2;
  display: flex;
  flex-direction: column;
}

.review-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-content {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  padding: 30px;
  overflow-y: auto;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.question-type {
  display: flex;
  align-items: center;
  gap: 15px;
}

.question-points {
  color: #e6a23c;
  font-weight: 600;
  font-size: 16px;
}

.question-title h3 {
  margin: 0 0 20px 0;
  color: #303133;
  font-size: 22px;
  font-weight: 600;
  line-height: 1.5;
}

.question-description {
  margin-bottom: 25px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.question-description p {
  margin: 0;
  color: #606266;
  font-size: 16px;
  line-height: 1.6;
}

.question-options {
  margin-bottom: 25px;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 15px 20px;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s;
}

.option-item:hover {
  background-color: #f5f7fa;
}

.option-correct {
  background-color: #f0f9ff;
  border-color: #67c23a;
  color: #67c23a;
}

.option-wrong {
  background-color: #fef0f0;
  border-color: #f56c6c;
  color: #f56c6c;
}

.option-label {
  width: 35px;
  height: 35px;
  line-height: 35px;
  text-align: center;
  background-color: #409eff;
  color: #fff;
  border-radius: 50%;
  font-weight: 600;
  margin-right: 20px;
}

.option-correct .option-label {
  background-color: #67c23a;
}

.option-wrong .option-label {
  background-color: #f56c6c;
}

.option-content {
  flex: 1;
  font-size: 18px;
  line-height: 1.5;
}

.answer-area {
  margin-top: 25px;
  padding: 25px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.answer-section {
  margin-bottom: 25px;
}

.answer-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 15px;
}

.answer-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  min-width: 100px;
}

.answer-value {
  flex: 1;
  padding: 12px 18px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 16px;
}

.user-answer {
  background-color: #fef0f0;
  color: #f56c6c;
  border: 1px solid #f56c6c;
}

.correct-answer {
  background-color: #f0f9ff;
  color: #67c23a;
  border: 1px solid #67c23a;
}

.explanation-section {
  padding: 20px;
  background-color: #fef0e6;
  border-radius: 8px;
  border-left: 4px solid #e6a23c;
}

.explanation-header h4 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.explanation-content p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}

.panel-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.panel-section h4 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.control-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.status-list {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.status-item {
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

.status-item:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.status-current {
  border-color: #409eff;
  background-color: #409eff;
  color: #fff;
}

.status-reviewed {
  border-color: #67c23a;
  background-color: #67c23a;
  color: #fff;
}

.status-pending {
  border-color: #e6a23c;
  background-color: #e6a23c;
  color: #fff;
}

.stats-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  color: #606266;
  font-weight: 500;
}

.stat-value {
  color: #303133;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .review-content {
    flex-direction: column;
    padding: 15px;
  }
  
  .review-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .header-right {
    flex-direction: column;
    gap: 10px;
  }
  
  .progress-bar {
    width: 100%;
  }
  
  .question-content {
    padding: 20px;
  }
  
  .status-list {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
