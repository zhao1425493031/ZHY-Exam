<template>
  <div class="exam-result">
    <div class="result-header">
      <div class="header-left">
        <h1>{{ examResult.exam_title }}</h1>
        <div class="exam-info">
          <span>考试时间：{{ formatDate(examResult.start_time) }} - {{ formatDate(examResult.submit_time) }}</span>
          <span>考试时长：{{ Math.round(examResult.duration) }}分钟</span>
        </div>
      </div>
      <div class="header-right">
        <div class="score-display">
          <div class="score-circle">
            <div class="score-value">{{ Math.round(examResult.total_score || 0) }}</div>
            <div class="score-total">/ {{ Math.round(examResult.total_points || 0) }}</div>
          </div>
          <div class="score-rate">{{ examResult.score_rate }}%</div>
        </div>
      </div>
    </div>

    <div class="result-content">
      <div class="content-left">
        <!-- 成绩概览 -->
        <div class="score-overview">
          <h3>成绩概览</h3>
          <div class="overview-grid">
            <div class="overview-item">
              <div class="item-label">总分</div>
              <div class="item-value">{{ Math.round(examResult.total_score || 0) }} / {{ Math.round(examResult.total_points || 0) }}</div>
            </div>
            <div class="overview-item">
              <div class="item-label">正确题数</div>
              <div class="item-value">{{ examResult.correct_count || 0 }} / {{ examResult.total_questions || 0 }}</div>
            </div>
            <div class="overview-item">
              <div class="item-label">得分率</div>
              <div class="item-value">{{ examResult.score_rate }}%</div>
            </div>
            <div class="overview-item">
              <div class="item-label">考试时长</div>
              <div class="item-value">{{ Math.round(examResult.duration) }}分钟</div>
            </div>
          </div>
        </div>

        <!-- 题目详情 -->
        <div class="question-details">
          <h3>题目详情</h3>
          <div class="details-tabs">
            <el-tabs v-model="activeTab">
              <el-tab-pane label="全部题目" name="all">
                <div class="question-list">
                  <div
                    v-for="(detail, index) in examResult.result_details"
                    :key="detail.question_id"
                    class="question-item"
                    :class="{ 'item-correct': detail.is_correct, 'item-wrong': !detail.is_correct }"
                  >
                    <div class="item-header">
                      <div class="item-number">{{ index + 1 }}</div>
                      <div class="item-type">
                        <el-tag :type="getTypeTagType(detail.question_type)" size="small">
                          {{ getTypeLabel(detail.question_type) }}
                        </el-tag>
                        <span class="item-points">{{ detail.question_points }}分</span>
                      </div>
                      <div class="item-status">
                        <el-tag :type="detail.is_correct ? 'success' : 'danger'" size="small">
                          {{ detail.is_correct ? '正确' : '错误' }}
                        </el-tag>
                      </div>
                    </div>
                    <div class="item-content">
                      <div class="question-title">{{ detail.question_title }}</div>
                      <div class="answer-section">
                        <div class="answer-item">
                          <span class="answer-label">我的答案：</span>
                          <span class="answer-value" :class="{ 'correct': detail.is_correct, 'wrong': !detail.is_correct }">
                            {{ detail.user_answer || '未作答' }}
                          </span>
                        </div>
                        <div class="answer-item">
                          <span class="answer-label">正确答案：</span>
                          <span class="answer-value correct">{{ detail.correct_answer }}</span>
                        </div>
                        <div v-if="detail.explanation" class="explanation">
                          <span class="explanation-label">解析：</span>
                          <span class="explanation-content">{{ detail.explanation }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="错题" name="wrong">
                <div class="question-list">
                  <div
                    v-for="detail in wrongQuestions"
                    :key="detail.question_id"
                    class="question-item item-wrong"
                  >
                    <div class="item-header">
                      <div class="item-number">{{ getQuestionIndex(detail.question_id) }}</div>
                      <div class="item-type">
                        <el-tag :type="getTypeTagType(detail.question_type)" size="small">
                          {{ getTypeLabel(detail.question_type) }}
                        </el-tag>
                        <span class="item-points">{{ detail.question_points }}分</span>
                      </div>
                    </div>
                    <div class="item-content">
                      <div class="question-title">{{ detail.question_title }}</div>
                      <div class="answer-section">
                        <div class="answer-item">
                          <span class="answer-label">我的答案：</span>
                          <span class="answer-value wrong">{{ detail.user_answer || '未作答' }}</span>
                        </div>
                        <div class="answer-item">
                          <span class="answer-label">正确答案：</span>
                          <span class="answer-value correct">{{ detail.correct_answer }}</span>
                        </div>
                        <div v-if="detail.explanation" class="explanation">
                          <span class="explanation-label">解析：</span>
                          <span class="explanation-content">{{ detail.explanation }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>
      </div>

      <div class="content-right">
        <!-- 成绩分析 -->
        <div class="score-analysis">
          <h4>成绩分析</h4>
          <div class="analysis-content">
            <div class="analysis-item">
              <div class="analysis-label">成绩等级</div>
              <div class="analysis-value">
                <el-tag :type="getGradeTagType(examResult.score_rate)" size="large">
                  {{ getGradeLabel(examResult.score_rate) }}
                </el-tag>
              </div>
            </div>
            <div class="analysis-item">
              <div class="analysis-label">答题正确率</div>
              <div class="analysis-value">
                <el-progress
                  :percentage="calculatePercentage(examResult.correct_count, examResult.total_questions)"
                  :color="getProgressColor(calculatePercentage(examResult.correct_count, examResult.total_questions) / 100)"
                />
              </div>
            </div>
            <div class="analysis-item">
              <div class="analysis-label">错题数量</div>
              <div class="analysis-value">{{ (examResult.total_questions || 0) - (examResult.correct_count || 0) }}题</div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button type="primary" @click="reviewWrongAnswers">
            <el-icon><View /></el-icon>
            复习错题
          </el-button>
          <el-button @click="retakeExam" v-if="canRetake">
            <el-icon><Refresh /></el-icon>
            重新考试
          </el-button>
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回列表
          </el-button>
        </div>

        <!-- 学习建议 -->
        <div class="study-suggestions">
          <h4>学习建议</h4>
          <div class="suggestions-content">
            <div v-if="examResult.score_rate >= 90" class="suggestion-item success">
              <el-icon><Trophy /></el-icon>
              <span>成绩优秀！继续保持良好的学习状态。</span>
            </div>
            <div v-else-if="examResult.score_rate >= 80" class="suggestion-item warning">
              <el-icon><Medal /></el-icon>
              <span>成绩良好，建议重点复习错题部分。</span>
            </div>
            <div v-else-if="examResult.score_rate >= 60" class="suggestion-item info">
              <el-icon><InfoFilled /></el-icon>
              <span>成绩及格，建议加强基础知识学习。</span>
            </div>
            <div v-else class="suggestion-item danger">
              <el-icon><Warning /></el-icon>
              <span>成绩不理想，建议系统复习相关知识点。</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { View, Refresh, ArrowLeft, Trophy, Medal, InfoFilled, Warning } from '@element-plus/icons-vue'
import { examScoringApi } from '@/api/exam_scoring'
import { examRecordsApi } from '@/api/exam_records'
import { formatDate } from '@/utils/format'

export default {
  name: 'ExamResult',
  components: {
    View,
    Refresh,
    ArrowLeft,
    Trophy,
    Medal,
    InfoFilled,
    Warning
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    // 响应式数据
    const examResult = ref({})
    const activeTab = ref('all')
    const loading = ref(false)
    
    // 计算属性
    const wrongQuestions = computed(() => {
      return examResult.value.result_details?.filter(detail => !detail.is_correct) || []
    })
    
    const canRetake = computed(() => {
      // TODO: 检查是否可以重考
      return true
    })
    
    // 方法
    const loadExamResult = async () => {
      try {
        loading.value = true
        const examRecordId = route.params.id
        
        // 首先获取考试记录详情
        const recordResponse = await examRecordsApi.getExamRecord(examRecordId)
        if (recordResponse.code === 200) {
          examResult.value = {
            ...recordResponse.data,
            // 设置默认值，防止undefined
            correct_count: recordResponse.data.correct_count || 0,
            total_questions: recordResponse.data.total_count || 0,
            total_score: recordResponse.data.score || 0,
            total_points: recordResponse.data.total_points || 0,
            score_rate: recordResponse.data.score_rate || 0
          }
        } else {
          throw new Error(recordResponse.message || '获取考试记录失败')
        }
        
        // 然后获取考试结果详情
        try {
          const resultResponse = await examScoringApi.getExamResult(examRecordId)
          if (resultResponse.code === 200) {
            console.log('考试结果详情:', resultResponse.data)
            console.log('Duration from API:', resultResponse.data.duration)
            console.log('Start time:', resultResponse.data.start_time)
            console.log('Submit time:', resultResponse.data.submit_time)
            examResult.value = { ...examResult.value, ...resultResponse.data }
            console.log('Final examResult:', examResult.value)
          }
        } catch (resultError) {
          console.warn('获取考试结果详情失败，使用基本信息:', resultError)
          // 如果获取结果详情失败，使用基本信息
        }
      } catch (error) {
        ElMessage.error('加载考试结果失败')
        console.error('Load exam result error:', error)
        router.push('/user/my-records')
      } finally {
        loading.value = false
      }
    }
    
    const getQuestionIndex = (questionId) => {
      const index = examResult.value.result_details?.findIndex(detail => detail.question_id === questionId)
      return index !== -1 ? index + 1 : 0
    }
    
    const reviewWrongAnswers = () => {
      router.push('/user/wrong-answers')
    }
    
    const retakeExam = () => {
      router.push(`/exam/detail/${examResult.value.exam_id}`)
    }
    
    const goBack = () => {
      router.push('/user/exams')
    }
    
    // 工具方法
    const calculatePercentage = (correct, total) => {
      if (!correct || !total || total === 0) {
        return 0
      }
      return Math.round((correct / total) * 100)
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
    
    const getGradeLabel = (scoreRate) => {
      if (scoreRate >= 90) return '优秀'
      if (scoreRate >= 80) return '良好'
      if (scoreRate >= 70) return '中等'
      if (scoreRate >= 60) return '及格'
      return '不及格'
    }
    
    const getGradeTagType = (scoreRate) => {
      if (scoreRate >= 90) return 'success'
      if (scoreRate >= 80) return 'primary'
      if (scoreRate >= 70) return 'warning'
      if (scoreRate >= 60) return 'info'
      return 'danger'
    }
    
    const getProgressColor = (rate) => {
      if (rate >= 0.9) return '#67c23a'
      if (rate >= 0.8) return '#409eff'
      if (rate >= 0.7) return '#e6a23c'
      if (rate >= 0.6) return '#909399'
      return '#f56c6c'
    }
    
    // 生命周期
    onMounted(() => {
      loadExamResult()
    })
    
    return {
      examResult,
      activeTab,
      loading,
      wrongQuestions,
      canRetake,
      getQuestionIndex,
      reviewWrongAnswers,
      retakeExam,
      goBack,
      calculatePercentage,
      getTypeLabel,
      getTypeTagType,
      getGradeLabel,
      getGradeTagType,
      getProgressColor,
      formatDate
    }
  }
}
</script>

<style scoped>
.exam-result {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-left h1 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.exam-info {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 14px;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 20px;
}

.score-circle {
  display: flex;
  align-items: baseline;
  gap: 5px;
}

.score-value {
  font-size: 48px;
  font-weight: 700;
  color: #409eff;
}

.score-total {
  font-size: 24px;
  color: #909399;
}

.score-rate {
  font-size: 20px;
  font-weight: 600;
  color: #e6a23c;
}

.result-content {
  display: flex;
  gap: 20px;
}

.content-left {
  flex: 2;
}

.content-right {
  flex: 1;
}

.score-overview,
.question-details,
.score-analysis,
.action-buttons,
.study-suggestions {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.score-overview h3,
.question-details h3,
.score-analysis h4,
.study-suggestions h4 {
  margin: 0 0 20px 0;
  color: #303133;
  font-size: 18px;
  font-weight: 600;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.overview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.item-label {
  color: #606266;
  font-weight: 500;
}

.item-value {
  color: #303133;
  font-weight: 600;
}

.question-list {
  max-height: 600px;
  overflow-y: auto;
}

.question-item {
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s;
}

.question-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.item-correct {
  border-left: 4px solid #67c23a;
  background-color: #f0f9ff;
}

.item-wrong {
  border-left: 4px solid #f56c6c;
  background-color: #fef0f0;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.item-number {
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  background-color: #409eff;
  color: #fff;
  border-radius: 50%;
  font-weight: 600;
}

.item-type {
  display: flex;
  align-items: center;
  gap: 10px;
}

.item-points {
  color: #e6a23c;
  font-weight: 500;
}

.item-status {
  display: flex;
  align-items: center;
}

.question-title {
  margin-bottom: 15px;
  color: #303133;
  font-weight: 500;
  line-height: 1.6;
}

.answer-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.answer-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.answer-label {
  color: #606266;
  font-weight: 500;
  min-width: 80px;
}

.answer-value {
  flex: 1;
  padding: 8px 12px;
  border-radius: 4px;
  background-color: #f8f9fa;
}

.answer-value.correct {
  background-color: #f0f9ff;
  color: #67c23a;
  border: 1px solid #67c23a;
}

.answer-value.wrong {
  background-color: #fef0f0;
  color: #f56c6c;
  border: 1px solid #f56c6c;
}

.explanation {
  margin-top: 10px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #e6a23c;
}

.explanation-label {
  color: #e6a23c;
  font-weight: 500;
  margin-right: 10px;
}

.explanation-content {
  color: #606266;
  line-height: 1.6;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.analysis-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.analysis-label {
  color: #606266;
  font-weight: 500;
}

.analysis-value {
  color: #303133;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.suggestions-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  border-radius: 6px;
  font-size: 14px;
}

.suggestion-item.success {
  background-color: #f0f9ff;
  color: #67c23a;
  border-left: 4px solid #67c23a;
}

.suggestion-item.warning {
  background-color: #fef0e6;
  color: #e6a23c;
  border-left: 4px solid #e6a23c;
}

.suggestion-item.info {
  background-color: #f4f4f5;
  color: #909399;
  border-left: 4px solid #909399;
}

.suggestion-item.danger {
  background-color: #fef0f0;
  color: #f56c6c;
  border-left: 4px solid #f56c6c;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .result-content {
    flex-direction: column;
  }
  
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .result-header {
    flex-direction: column;
    gap: 20px;
  }
  
  .score-display {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
