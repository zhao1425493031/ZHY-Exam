<template>
  <div class="question-detail">
    <div class="detail-header">
      <div class="question-type">
        <el-tag :type="getTypeTagType(question.question_type)" size="large">
          {{ getTypeLabel(question.question_type) }}
        </el-tag>
      </div>
      <div class="question-points">
        <span class="points-label">分值：</span>
        <span class="points-value">{{ question.question_points }}分</span>
      </div>
    </div>

    <div class="detail-content">
      <!-- 题目内容 -->
      <div class="question-content">
        <h3>{{ question.question_title }}</h3>
        <div v-if="question.question_content" class="question-description">
          <p>{{ question.question_content }}</p>
        </div>
      </div>

      <!-- 选项（选择题） -->
      <div v-if="isChoiceQuestion" class="question-options">
        <div
          v-for="(option, index) in question.options"
          :key="index"
          class="option-item"
          :class="getOptionClass(index)"
        >
          <div class="option-label">{{ String.fromCharCode(65 + index) }}</div>
          <div class="option-content">{{ option }}</div>
        </div>
      </div>

      <!-- 答案对比 -->
      <div class="answer-comparison">
        <div class="comparison-header">
          <h4>答案对比</h4>
        </div>
        <div class="comparison-content">
          <div class="answer-item">
            <div class="answer-label">
              <el-icon color="#f56c6c"><Close /></el-icon>
              我的答案
            </div>
            <div class="answer-value user-answer">
              {{ userAnswer || '未作答' }}
            </div>
          </div>
          <div class="answer-item">
            <div class="answer-label">
              <el-icon color="#67c23a"><Check /></el-icon>
              正确答案
            </div>
            <div class="answer-value correct-answer">
              {{ correctAnswer }}
            </div>
          </div>
        </div>
      </div>

      <!-- 解析 -->
      <div v-if="explanation" class="question-explanation">
        <div class="explanation-header">
          <h4>题目解析</h4>
        </div>
        <div class="explanation-content">
          <p>{{ explanation }}</p>
        </div>
      </div>

      <!-- 相关统计 -->
      <div class="question-stats">
        <div class="stats-header">
          <h4>相关统计</h4>
        </div>
        <div class="stats-content">
          <div class="stat-item">
            <span class="stat-label">错题时间：</span>
            <span class="stat-value">{{ formatDate(question.created_at) }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">来源考试：</span>
            <span class="stat-value">{{ question.exam_title || '未知考试' }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">复习状态：</span>
            <span class="stat-value">
              <el-tag :type="question.is_reviewed ? 'success' : 'warning'" size="small">
                {{ question.is_reviewed ? '已复习' : '待复习' }}
              </el-tag>
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="detail-footer">
      <div class="footer-actions">
        <el-button @click="handleClose">关闭</el-button>
        <el-button type="primary" @click="handleReview" v-if="!question.is_reviewed">
          <el-icon><Check /></el-icon>
          标记复习
        </el-button>
        <el-button type="success" @click="handleRetake" v-if="question.exam_id">
          <el-icon><Refresh /></el-icon>
          重新考试
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Check, Close, Refresh } from '@element-plus/icons-vue'
import { examScoringApi } from '@/api/exam_scoring'
import { formatDate } from '@/utils/format'

export default {
  name: 'QuestionDetail',
  components: {
    Check,
    Close,
    Refresh
  },
  props: {
    question: {
      type: Object,
      required: true
    },
    userAnswer: {
      type: String,
      default: ''
    },
    correctAnswer: {
      type: String,
      required: true
    },
    explanation: {
      type: String,
      default: ''
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const router = useRouter()
    
    // 计算属性
    const isChoiceQuestion = computed(() => {
      return ['single', 'multiple'].includes(props.question.question_type)
    })
    
    // 方法
    const getOptionClass = (index) => {
      const optionLetter = String.fromCharCode(65 + index)
      const isUserAnswer = props.userAnswer && props.userAnswer.includes(optionLetter)
      const isCorrectAnswer = props.correctAnswer && props.correctAnswer.includes(optionLetter)
      
      if (isCorrectAnswer) {
        return 'option-correct'
      } else if (isUserAnswer && !isCorrectAnswer) {
        return 'option-wrong'
      }
      return ''
    }
    
    const handleClose = () => {
      emit('close')
    }
    
    const handleReview = async () => {
      try {
        await examScoringApi.reviewWrongAnswer(props.question.id)
        ElMessage.success('标记复习成功')
        emit('close')
      } catch (error) {
        ElMessage.error('标记复习失败')
        console.error('Review question error:', error)
      }
    }
    
    const handleRetake = () => {
      if (props.question.exam_id) {
        router.push(`/user/exam-taking/${props.question.exam_id}`)
      } else {
        ElMessage.warning('无法找到来源考试')
      }
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
    
    return {
      isChoiceQuestion,
      getOptionClass,
      handleClose,
      handleReview,
      handleRetake,
      getTypeLabel,
      getTypeTagType,
      formatDate
    }
  }
}
</script>

<style scoped>
.question-detail {
  padding: 20px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.question-points {
  display: flex;
  align-items: center;
  gap: 8px;
}

.points-label {
  color: #606266;
  font-weight: 500;
}

.points-value {
  color: #e6a23c;
  font-weight: 600;
  font-size: 18px;
}

.detail-content {
  margin-bottom: 30px;
}

.question-content {
  margin-bottom: 25px;
}

.question-content h3 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
  line-height: 1.5;
}

.question-description {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.question-description p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}

.question-options {
  margin-bottom: 25px;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  padding: 12px 15px;
  border-radius: 6px;
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
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  background-color: #409eff;
  color: #fff;
  border-radius: 50%;
  font-weight: 600;
  margin-right: 15px;
}

.option-correct .option-label {
  background-color: #67c23a;
}

.option-wrong .option-label {
  background-color: #f56c6c;
}

.option-content {
  flex: 1;
  font-size: 16px;
  line-height: 1.5;
}

.answer-comparison {
  margin-bottom: 25px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.comparison-header h4,
.explanation-header h4,
.stats-header h4 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.comparison-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.answer-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.answer-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  min-width: 100px;
}

.answer-value {
  flex: 1;
  padding: 10px 15px;
  border-radius: 6px;
  font-weight: 500;
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

.question-explanation {
  margin-bottom: 25px;
  padding: 20px;
  background-color: #fef0e6;
  border-radius: 8px;
  border-left: 4px solid #e6a23c;
}

.explanation-content p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}

.question-stats {
  padding: 20px;
  background-color: #f4f4f5;
  border-radius: 8px;
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
  font-weight: 500;
}

.detail-footer {
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.footer-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .question-detail {
    padding: 15px;
  }
  
  .detail-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .comparison-content {
    gap: 10px;
  }
  
  .answer-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .answer-label {
    min-width: auto;
  }
  
  .footer-actions {
    flex-direction: column;
  }
}
</style>
