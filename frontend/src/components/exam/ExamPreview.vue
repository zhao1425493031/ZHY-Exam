<template>
  <div class="exam-preview">
    <div class="exam-header">
      <div class="exam-title">
        <h2>{{ exam.title }}</h2>
        <div class="exam-meta">
          <el-tag :type="getStatusTagType(exam.status)" size="small">
            {{ getStatusLabel(exam.status) }}
          </el-tag>
          <el-tag :type="getPaperTypeTagType(exam.paper_type)" size="small">
            {{ getPaperTypeLabel(exam.paper_type) }}
          </el-tag>
          <span class="exam-info">
            {{ exam.question_count || 0 }}题 | {{ exam.total_points || 0 }}分 | {{ formatDuration(exam.duration) }}
          </span>
        </div>
      </div>
      <div class="exam-subject">
        科目：{{ getSubjectName(exam.subject_id) }}
      </div>
    </div>

    <div class="exam-content">
      <div v-if="exam.description" class="exam-description">
        <h4>考试描述</h4>
        <p>{{ exam.description }}</p>
      </div>

      <!-- 时间设置 -->
      <div class="time-settings">
        <h4>时间设置</h4>
        <div class="time-grid">
          <div class="time-item">
            <span class="time-label">考试时长：</span>
            <span class="time-value">{{ formatDuration(exam.duration) }}</span>
          </div>
          <div v-if="exam.start_time" class="time-item">
            <span class="time-label">开始时间：</span>
            <span class="time-value">{{ formatDate(exam.start_time) }}</span>
          </div>
          <div v-if="exam.end_time" class="time-item">
            <span class="time-label">结束时间：</span>
            <span class="time-value">{{ formatDate(exam.end_time) }}</span>
          </div>
        </div>
      </div>

      <!-- 组卷配置 -->
      <div class="paper-config">
        <h4>组卷配置</h4>
        
        <!-- 随机组卷 -->
        <div v-if="exam.paper_type === 'random'" class="random-config">
          <div class="config-item">
            <span class="config-label">题目总数：</span>
            <span class="config-value">{{ exam.total_questions }}题</span>
          </div>
          <div class="config-item">
            <span class="config-label">题型选择：</span>
            <span class="config-value">
              <el-tag
                v-for="type in exam.question_types"
                :key="type"
                :type="getTypeTagType(type)"
                size="small"
                style="margin-right: 5px"
              >
                {{ getTypeLabel(type) }}
              </el-tag>
            </span>
          </div>
          <div class="config-item">
            <span class="config-label">难度分布：</span>
            <span class="config-value">
              简单{{ exam.difficulty_distribution?.easy || 0 }}% | 
              中等{{ exam.difficulty_distribution?.medium || 0 }}% | 
              困难{{ exam.difficulty_distribution?.hard || 0 }}%
            </span>
          </div>
        </div>

        <!-- 手动选题 -->
        <div v-if="exam.paper_type === 'manual'" class="manual-config">
          <div class="config-item">
            <span class="config-label">题目数量：</span>
            <span class="config-value">{{ exam.question_count || 0 }}题</span>
          </div>
          <div class="config-item">
            <span class="config-label">总分：</span>
            <span class="config-value">{{ exam.total_points || 0 }}分</span>
          </div>
          <div v-if="selectedQuestions.length > 0" class="question-list">
            <div class="list-header">
              <span>题目列表</span>
              <el-button size="small" @click="showQuestionList = !showQuestionList">
                {{ showQuestionList ? '收起' : '展开' }}
              </el-button>
            </div>
            <div v-if="showQuestionList" class="question-items">
              <div
                v-for="(question, index) in selectedQuestions"
                :key="question.id"
                class="question-item"
              >
                <div class="item-index">{{ index + 1 }}</div>
                <div class="item-content">
                  <div class="item-title">{{ question.title }}</div>
                  <div class="item-meta">
                    <el-tag :type="getTypeTagType(question.type)" size="small">
                      {{ getTypeLabel(question.type) }}
                    </el-tag>
                    <el-tag :type="getDifficultyTagType(question.difficulty)" size="small">
                      {{ getDifficultyLabel(question.difficulty) }}
                    </el-tag>
                    <span class="item-points">{{ question.points }}分</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 模板组卷 -->
        <div v-if="exam.paper_type === 'template'" class="template-config">
          <div class="config-item">
            <span class="config-label">使用模板：</span>
            <span class="config-value">{{ exam.template_name || '未选择模板' }}</span>
          </div>
        </div>
      </div>

      <!-- 考试设置 -->
      <div class="exam-settings">
        <h4>考试设置</h4>
        <div class="settings-grid">
          <div class="setting-item">
            <span class="setting-label">允许重考：</span>
            <el-tag :type="exam.settings?.allow_retake ? 'success' : 'info'" size="small">
              {{ exam.settings?.allow_retake ? '是' : '否' }}
            </el-tag>
          </div>
          <div class="setting-item">
            <span class="setting-label">显示答案：</span>
            <el-tag :type="exam.settings?.show_answer ? 'success' : 'info'" size="small">
              {{ exam.settings?.show_answer ? '是' : '否' }}
            </el-tag>
          </div>
          <div class="setting-item">
            <span class="setting-label">防切屏：</span>
            <el-tag :type="exam.settings?.prevent_switch ? 'success' : 'info'" size="small">
              {{ exam.settings?.prevent_switch ? '是' : '否' }}
            </el-tag>
          </div>
          <div class="setting-item">
            <span class="setting-label">自动提交：</span>
            <el-tag :type="exam.settings?.auto_submit ? 'success' : 'info'" size="small">
              {{ exam.settings?.auto_submit ? '是' : '否' }}
            </el-tag>
          </div>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="exam-statistics">
        <h4>统计信息</h4>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">题目数量：</span>
            <span class="stat-value">{{ exam.question_count || 0 }}题</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">总分：</span>
            <span class="stat-value">{{ exam.total_points || 0 }}分</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">预计时长：</span>
            <span class="stat-value">{{ estimatedDuration }}分钟</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">平均每题：</span>
            <span class="stat-value">{{ averageTimePerQuestion }}分钟</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { formatDate, formatDuration } from '@/utils/format'

export default {
  name: 'ExamPreview',
  props: {
    exam: {
      type: Object,
      required: true
    },
    subjects: {
      type: Array,
      default: () => []
    },
    selectedQuestions: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const showQuestionList = ref(false)

    // 计算属性
    const getSubjectName = computed(() => {
      return (subjectId) => {
        const subject = props.subjects.find(s => s.id === subjectId)
        return subject ? subject.name : '未知科目'
      }
    })

    const estimatedDuration = computed(() => {
      if (props.exam.paper_type === 'manual' && props.selectedQuestions.length > 0) {
        return props.selectedQuestions.reduce((total, q) => {
          const timePerQuestion = {
            single: 2,
            multiple: 3,
            judge: 1,
            fill: 5,
            essay: 10
          }
          return total + (timePerQuestion[q.type] || 3)
        }, 0)
      } else if (props.exam.paper_type === 'random') {
        const timePerQuestion = {
          single: 2,
          multiple: 3,
          judge: 1,
          fill: 5,
          essay: 10
        }
        return props.exam.question_types?.reduce((total, type) => {
          const count = Math.ceil(props.exam.total_questions * (props.exam.difficulty_distribution?.[type] || 0) / 100)
          return total + (count * (timePerQuestion[type] || 3))
        }, 0) || props.exam.duration
      }
      return props.exam.duration
    })

    const averageTimePerQuestion = computed(() => {
      const questionCount = props.exam.question_count || props.exam.total_questions || 1
      return Math.round(estimatedDuration.value / questionCount * 10) / 10
    })

    // 工具方法
    const getStatusLabel = (status) => {
      const labels = {
        draft: '草稿',
        published: '已发布',
        ongoing: '进行中',
        finished: '已结束',
        cancelled: '已取消'
      }
      return labels[status] || status
    }

    const getStatusTagType = (status) => {
      const types = {
        draft: 'info',
        published: 'success',
        ongoing: 'primary',
        finished: 'warning',
        cancelled: 'danger'
      }
      return types[status] || 'default'
    }

    const getPaperTypeLabel = (type) => {
      const labels = {
        random: '随机组卷',
        manual: '手动选题',
        template: '模板组卷'
      }
      return labels[type] || type
    }

    const getPaperTypeTagType = (type) => {
      const types = {
        random: 'primary',
        manual: 'success',
        template: 'warning'
      }
      return types[type] || 'default'
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

    return {
      showQuestionList,
      getSubjectName,
      estimatedDuration,
      averageTimePerQuestion,
      getStatusLabel,
      getStatusTagType,
      getPaperTypeLabel,
      getPaperTypeTagType,
      getTypeLabel,
      getTypeTagType,
      getDifficultyLabel,
      getDifficultyTagType,
      formatDate,
      formatDuration
    }
  }
}
</script>

<style scoped>
.exam-preview {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.exam-title h2 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.exam-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.exam-info {
  color: #909399;
  font-size: 14px;
}

.exam-subject {
  color: #606266;
  font-size: 14px;
}

.exam-content {
  line-height: 1.6;
}

.exam-content h4 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 500;
}

.exam-description {
  margin-bottom: 25px;
}

.exam-description p {
  margin: 0;
  color: #606266;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.time-settings,
.paper-config,
.exam-settings,
.exam-statistics {
  margin-bottom: 25px;
}

.time-grid,
.settings-grid,
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.time-item,
.setting-item,
.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
}

.time-label,
.setting-label,
.stat-label {
  color: #606266;
  font-weight: 500;
}

.time-value,
.stat-value {
  color: #303133;
}

.random-config,
.manual-config,
.template-config {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #67c23a;
}

.config-item {
  margin-bottom: 10px;
}

.config-item:last-child {
  margin-bottom: 0;
}

.config-label {
  color: #606266;
  font-weight: 500;
  margin-right: 10px;
}

.config-value {
  color: #303133;
}

.question-list {
  margin-top: 15px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e4e7ed;
}

.question-items {
  max-height: 300px;
  overflow-y: auto;
}

.question-item {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 8px;
  background-color: #fff;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
}

.question-item:last-child {
  margin-bottom: 0;
}

.item-index {
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  background-color: #409eff;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 500;
  margin-right: 10px;
}

.item-content {
  flex: 1;
}

.item-title {
  margin-bottom: 6px;
  color: #303133;
  font-weight: 500;
  font-size: 14px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-points {
  color: #e6a23c;
  font-weight: 500;
  font-size: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .exam-preview {
    padding: 15px;
  }
  
  .exam-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .time-grid,
  .settings-grid,
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
