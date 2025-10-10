<template>
  <div class="question-view">
    <div class="question-header">
      <div class="question-meta">
        <el-tag :type="getTypeTagType(question.type)" size="small">
          {{ getTypeLabel(question.type) }}
        </el-tag>
        <el-tag :type="getDifficultyTagType(question.difficulty)" size="small">
          {{ getDifficultyLabel(question.difficulty) }}
        </el-tag>
        <el-tag :type="getStatusTagType(question.status)" size="small">
          {{ getStatusLabel(question.status) }}
        </el-tag>
        <span class="points">{{ question.points }}分</span>
      </div>
      <div class="subject-info">
        科目：{{ getSubjectName(question.subject_id) }}
      </div>
    </div>

    <div class="question-content">
      <div class="question-title">
        <h3>{{ question.title }}</h3>
      </div>

      <div v-if="question.content" class="question-body">
        <p>{{ question.content }}</p>
      </div>

      <!-- 选项 -->
      <div v-if="showOptions" class="question-options">
        <div
          v-for="(option, index) in question.options"
          :key="index"
          class="option-item"
          :class="{ 'correct-option': isCorrectOption(index) }"
        >
          <span class="option-label">{{ option.label }}.</span>
          <span class="option-text">{{ option.text }}</span>
          <el-icon v-if="isCorrectOption(index)" class="correct-icon">
            <Check />
          </el-icon>
        </div>
      </div>

      <!-- 判断题选项 -->
      <div v-if="question.type === 'judge'" class="judge-options">
        <div class="judge-option" :class="{ 'correct-option': question.answer === 'true' }">
          <span class="option-label">A.</span>
          <span class="option-text">正确</span>
          <el-icon v-if="question.answer === 'true'" class="correct-icon">
            <Check />
          </el-icon>
        </div>
        <div class="judge-option" :class="{ 'correct-option': question.answer === 'false' }">
          <span class="option-label">B.</span>
          <span class="option-text">错误</span>
          <el-icon v-if="question.answer === 'false'" class="correct-icon">
            <Check />
          </el-icon>
        </div>
      </div>

      <!-- 填空题答案 -->
      <div v-if="question.type === 'fill'" class="answer-section">
        <h4>参考答案：</h4>
        <div class="answer-content">{{ question.answer }}</div>
      </div>

      <!-- 简答题答案 -->
      <div v-if="question.type === 'essay'" class="answer-section">
        <h4>参考答案：</h4>
        <div class="answer-content">{{ question.answer }}</div>
      </div>

      <!-- 解析说明 -->
      <div v-if="question.explanation" class="explanation-section">
        <h4>解析说明：</h4>
        <div class="explanation-content">{{ question.explanation }}</div>
      </div>

      <!-- 标签 -->
      <div v-if="question.tags && question.tags.length > 0" class="tags-section">
        <h4>标签：</h4>
        <div class="tags">
          <el-tag
            v-for="tag in question.tags"
            :key="tag"
            size="small"
            style="margin-right: 8px; margin-bottom: 8px"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>

      <!-- 创建信息 -->
      <div class="create-info">
        <el-divider />
        <div class="info-row">
          <span class="info-label">创建时间：</span>
          <span class="info-value">{{ formatDate(question.created_at) }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">更新时间：</span>
          <span class="info-value">{{ formatDate(question.updated_at) }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">创建者ID：</span>
          <span class="info-value">{{ question.created_by }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { Check } from '@element-plus/icons-vue'
import { formatDate } from '@/utils/format'

export default {
  name: 'QuestionView',
  components: {
    Check
  },
  props: {
    question: {
      type: Object,
      required: true
    },
    subjects: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    // 计算属性
    const showOptions = computed(() => {
      return ['single', 'multiple'].includes(props.question.type)
    })

    const getSubjectName = computed(() => {
      return (subjectId) => {
        const subject = props.subjects.find(s => s.id === subjectId)
        return subject ? subject.name : '未知科目'
      }
    })

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

    const getDifficultyLabel = (difficulty) => {
      const labels = {
        easy: '简单',
        medium: '中等',
        hard: '困难'
      }
      return labels[difficulty] || difficulty
    }

    const getDifficultyTagType = (difficulty) => {
      const types = {
        easy: 'success',
        medium: 'warning',
        hard: 'danger'
      }
      return types[difficulty] || 'default'
    }

    const getStatusLabel = (status) => {
      const labels = {
        draft: '草稿',
        published: '已发布',
        archived: '已归档'
      }
      return labels[status] || status
    }

    const getStatusTagType = (status) => {
      const types = {
        draft: 'info',
        published: 'success',
        archived: 'warning'
      }
      return types[status] || 'default'
    }

    const isCorrectOption = (index) => {
      if (props.question.type === 'single') {
        return parseInt(props.question.answer) === index
      } else if (props.question.type === 'multiple') {
        const correctAnswers = props.question.answer.split(',').map(a => parseInt(a))
        return correctAnswers.includes(index)
      }
      return false
    }

    return {
      showOptions,
      getSubjectName,
      getTypeLabel,
      getTypeTagType,
      getDifficultyLabel,
      getDifficultyTagType,
      getStatusLabel,
      getStatusTagType,
      isCorrectOption,
      formatDate
    }
  }
}
</script>

<style scoped>
.question-view {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.points {
  font-weight: 500;
  color: #409eff;
}

.subject-info {
  color: #606266;
  font-size: 14px;
}

.question-content {
  line-height: 1.6;
}

.question-title h3 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 500;
}

.question-body {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.question-body p {
  margin: 0;
  color: #606266;
}

.question-options,
.judge-options {
  margin-bottom: 20px;
}

.option-item,
.judge-option {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  margin-bottom: 8px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s;
}

.option-item:hover,
.judge-option:hover {
  background-color: #ecf5ff;
  border-color: #b3d8ff;
}

.correct-option {
  background-color: #f0f9ff !important;
  border-color: #67c23a !important;
  color: #67c23a;
}

.option-label {
  font-weight: 500;
  margin-right: 10px;
  min-width: 20px;
}

.option-text {
  flex: 1;
}

.correct-icon {
  margin-left: 10px;
  font-size: 16px;
}

.answer-section,
.explanation-section,
.tags-section {
  margin-bottom: 20px;
}

.answer-section h4,
.explanation-section h4,
.tags-section h4 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

.answer-content,
.explanation-content {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #67c23a;
  color: #606266;
  white-space: pre-wrap;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.create-info {
  margin-top: 30px;
}

.info-row {
  display: flex;
  margin-bottom: 8px;
}

.info-label {
  font-weight: 500;
  color: #606266;
  min-width: 100px;
}

.info-value {
  color: #303133;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .question-view {
    padding: 15px;
  }
  
  .question-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .question-meta {
    flex-wrap: wrap;
  }
}
</style>
