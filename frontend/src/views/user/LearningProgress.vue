<template>
  <div class="learning-progress">
    <div class="page-header">
      <h1>学习进度</h1>
      <div class="header-info">
        <el-tag type="info">学习天数: {{ overview.learning_stats?.learning_days || 0 }} 天</el-tag>
      </div>
    </div>

    <!-- 学习概览 -->
    <div class="overview-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon">
                <el-icon color="#409eff"><Document /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-value">{{ overview.learning_stats?.total_exams || 0 }}</div>
                <div class="card-label">总考试次数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon">
                <el-icon color="#67c23a"><Trophy /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-value">{{ overview.learning_stats?.average_score || 0 }}</div>
                <div class="card-label">平均分数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon">
                <el-icon color="#e6a23c"><TrendCharts /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-value">{{ overview.learning_stats?.study_intensity || 0 }}%</div>
                <div class="card-label">学习强度</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon">
                <el-icon color="#f56c6c"><Warning /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-value">{{ overview.learning_stats?.review_rate || 0 }}%</div>
                <div class="card-label">复习率</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 学习进度图表 -->
    <div class="progress-chart">
      <el-card>
        <div class="chart-header">
          <h3>学习进度趋势</h3>
          <div class="chart-controls">
            <el-select v-model="progressPeriod" @change="updateProgressChart" style="width: 120px">
              <el-option label="最近7天" value="7d" />
              <el-option label="最近30天" value="30d" />
              <el-option label="最近3个月" value="3m" />
              <el-option label="最近1年" value="1y" />
            </el-select>
            <el-select v-model="selectedSubject" @change="updateProgressChart" style="width: 150px" clearable>
              <el-option
                v-for="subject in subjects"
                :key="subject.id"
                :label="subject.name"
                :value="subject.id"
              />
            </el-select>
          </div>
        </div>
        <div class="chart-content">
          <div ref="progressChart" class="chart-container"></div>
        </div>
      </el-card>
    </div>

    <!-- 学习成就 -->
    <div class="achievements-section">
      <el-card>
        <div class="achievements-header">
          <h3>学习成就</h3>
          <div class="achievements-summary">
            <span>已获得 {{ unlockedAchievements.length }} / {{ achievements.length }} 个成就</span>
          </div>
        </div>
        <div class="achievements-content">
          <div class="achievements-grid">
            <div
              v-for="achievement in achievements"
              :key="achievement.id"
              class="achievement-item"
              :class="{ 'achievement-unlocked': achievement.unlocked }"
            >
              <div class="achievement-icon">
                <el-icon v-if="achievement.icon === 'trophy'" color="#e6a23c"><Trophy /></el-icon>
                <el-icon v-else-if="achievement.icon === 'medal'" color="#67c23a"><Medal /></el-icon>
                <el-icon v-else-if="achievement.icon === 'star'" color="#f56c6c"><Star /></el-icon>
                <el-icon v-else-if="achievement.icon === 'book'" color="#409eff"><Reading /></el-icon>
                <el-icon v-else-if="achievement.icon === 'fire'" color="#f56c6c"><Fire /></el-icon>
                <el-icon v-else color="#909399"><Trophy /></el-icon>
              </div>
              <div class="achievement-info">
                <div class="achievement-title">{{ achievement.title }}</div>
                <div class="achievement-description">{{ achievement.description }}</div>
                <div v-if="!achievement.unlocked" class="achievement-progress">
                  <el-progress :percentage="achievement.progress" :show-text="false" />
                  <span class="progress-text">{{ achievement.progress }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 学习建议 -->
    <div class="recommendations-section">
      <el-card>
        <div class="recommendations-header">
          <h3>学习建议</h3>
          <el-button size="small" @click="refreshRecommendations">
            <el-icon><Refresh /></el-icon>
            刷新建议
          </el-button>
        </div>
        <div class="recommendations-content">
          <div v-if="recommendations.length === 0" class="no-recommendations">
            <el-empty description="暂无学习建议" />
          </div>
          <div v-else class="recommendations-list">
            <div
              v-for="recommendation in recommendations"
              :key="recommendation.type"
              class="recommendation-item"
              :class="`priority-${recommendation.priority}`"
            >
              <div class="recommendation-header">
                <div class="recommendation-title">{{ recommendation.title }}</div>
                <el-tag :type="getPriorityTagType(recommendation.priority)" size="small">
                  {{ getPriorityLabel(recommendation.priority) }}
                </el-tag>
              </div>
              <div class="recommendation-description">{{ recommendation.description }}</div>
              <div class="recommendation-action">
                <el-button size="small" type="primary" @click="handleRecommendationAction(recommendation)">
                  {{ recommendation.action }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 学习目标 -->
    <div class="goals-section">
      <el-card>
        <div class="goals-header">
          <h3>学习目标</h3>
          <el-button size="small" type="primary" @click="showCreateGoalDialog = true">
            <el-icon><Plus /></el-icon>
            新建目标
          </el-button>
        </div>
        <div class="goals-content">
          <div v-if="goals.length === 0" class="no-goals">
            <el-empty description="暂无学习目标" />
          </div>
          <div v-else class="goals-list">
            <div
              v-for="goal in goals"
              :key="goal.id"
              class="goal-item"
            >
              <div class="goal-header">
                <div class="goal-title">{{ goal.title }}</div>
                <div class="goal-actions">
                  <el-button size="small" @click="editGoal(goal)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteGoal(goal)">删除</el-button>
                </div>
              </div>
              <div class="goal-description">{{ goal.description }}</div>
              <div class="goal-progress">
                <div class="progress-info">
                  <span>{{ goal.current_value }} / {{ goal.target_value }}</span>
                  <span>{{ goal.progress }}%</span>
                </div>
                <el-progress :percentage="goal.progress" />
              </div>
              <div class="goal-meta">
                <span>目标日期: {{ goal.target_date }}</span>
                <el-tag :type="getGoalStatusType(goal.status)" size="small">
                  {{ getGoalStatusLabel(goal.status) }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 学习报告 -->
    <div class="report-section">
      <el-card>
        <div class="report-header">
          <h3>学习报告</h3>
          <div class="report-controls">
            <el-select v-model="reportPeriod" @change="generateReport" style="width: 120px">
              <el-option label="最近一周" value="week" />
              <el-option label="最近一月" value="month" />
              <el-option label="最近一季" value="quarter" />
              <el-option label="最近一年" value="year" />
            </el-select>
            <el-button size="small" type="primary" @click="generateReport">
              <el-icon><Document /></el-icon>
              生成报告
            </el-button>
          </div>
        </div>
        <div class="report-content">
          <div v-if="!learningReport" class="no-report">
            <el-empty description="请生成学习报告" />
          </div>
          <div v-else class="report-details">
            <div class="report-summary">
              <h4>学习总结</h4>
              <div class="summary-stats">
                <div class="stat-item">
                  <span class="stat-label">考试次数:</span>
                  <span class="stat-value">{{ learningReport.summary.total_exams }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">平均分数:</span>
                  <span class="stat-value">{{ learningReport.summary.average_score }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">错题数量:</span>
                  <span class="stat-value">{{ learningReport.summary.total_wrong_answers }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">复习数量:</span>
                  <span class="stat-value">{{ learningReport.summary.reviewed_wrong_answers }}</span>
                </div>
              </div>
            </div>
            
            <div class="report-analysis">
              <h4>学习分析</h4>
              <div class="analysis-content">
                <div v-if="learningReport.analysis.strengths.length > 0" class="strengths">
                  <h5>优势</h5>
                  <ul>
                    <li v-for="strength in learningReport.analysis.strengths" :key="strength">
                      {{ strength }}
                    </li>
                  </ul>
                </div>
                <div v-if="learningReport.analysis.weaknesses.length > 0" class="weaknesses">
                  <h5>不足</h5>
                  <ul>
                    <li v-for="weakness in learningReport.analysis.weaknesses" :key="weakness">
                      {{ weakness }}
                    </li>
                  </ul>
                </div>
                <div v-if="learningReport.analysis.recommendations.length > 0" class="recommendations">
                  <h5>建议</h5>
                  <ul>
                    <li v-for="recommendation in learningReport.analysis.recommendations" :key="recommendation">
                      {{ recommendation }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 创建目标对话框 -->
    <el-dialog
      v-model="showCreateGoalDialog"
      title="新建学习目标"
      width="500px"
    >
      <el-form :model="goalForm" :rules="goalRules" ref="goalFormRef" label-width="100px">
        <el-form-item label="目标标题" prop="title">
          <el-input v-model="goalForm.title" placeholder="请输入目标标题" />
        </el-form-item>
        <el-form-item label="目标描述" prop="description">
          <el-input v-model="goalForm.description" type="textarea" placeholder="请输入目标描述" />
        </el-form-item>
        <el-form-item label="目标分数" prop="target_score">
          <el-input-number v-model="goalForm.target_score" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="目标日期" prop="target_date">
          <el-date-picker
            v-model="goalForm.target_date"
            type="date"
            placeholder="选择目标日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateGoalDialog = false">取消</el-button>
        <el-button type="primary" @click="createGoal">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document, Trophy, TrendCharts, Warning, Medal, Star, Reading, Fire,
  Refresh, Plus
} from '@element-plus/icons-vue'
import { learningProgressApi } from '@/api/learning_progress'
import { subjectsApi } from '@/api/subjects'
import * as echarts from 'echarts'

export default {
  name: 'LearningProgress',
  components: {
    Document,
    Trophy,
    TrendCharts,
    Warning,
    Medal,
    Star,
    Reading,
    Fire,
    Refresh,
    Plus
  },
  setup() {
    const router = useRouter()
    
    // 响应式数据
    const loading = ref(false)
    const overview = ref({})
    const progressData = ref({})
    const achievements = ref([])
    const recommendations = ref([])
    const goals = ref([])
    const learningReport = ref(null)
    const subjects = ref([])
    const progressChart = ref(null)
    const progressPeriod = ref('30d')
    const selectedSubject = ref('')
    const reportPeriod = ref('month')
    const showCreateGoalDialog = ref(false)
    
    // 目标表单
    const goalForm = reactive({
      title: '',
      description: '',
      target_score: 80,
      target_date: ''
    })
    
    const goalRules = {
      title: [
        { required: true, message: '请输入目标标题', trigger: 'blur' }
      ],
      target_score: [
        { required: true, message: '请输入目标分数', trigger: 'blur' }
      ],
      target_date: [
        { required: true, message: '请选择目标日期', trigger: 'change' }
      ]
    }
    
    // 计算属性
    const unlockedAchievements = computed(() => {
      return achievements.value.filter(a => a.unlocked)
    })
    
    // 方法
    const loadOverview = async () => {
      try {
        const response = await learningProgressApi.getOverview()
        overview.value = response.data
      } catch (error) {
        ElMessage.error('加载学习概览失败')
        console.error('Load overview error:', error)
      }
    }
    
    const loadProgressData = async () => {
      try {
        const params = {
          period: progressPeriod.value,
          subject_id: selectedSubject.value || undefined
        }
        const response = await learningProgressApi.getProgress(params)
        progressData.value = response.data
        await nextTick()
        updateProgressChart()
      } catch (error) {
        ElMessage.error('加载学习进度失败')
        console.error('Load progress error:', error)
      }
    }
    
    const loadAchievements = async () => {
      try {
        const response = await learningProgressApi.getAchievements()
        achievements.value = response.data
      } catch (error) {
        ElMessage.error('加载学习成就失败')
        console.error('Load achievements error:', error)
      }
    }
    
    const loadRecommendations = async () => {
      try {
        const response = await learningProgressApi.getRecommendations()
        recommendations.value = response.data
      } catch (error) {
        ElMessage.error('加载学习建议失败')
        console.error('Load recommendations error:', error)
      }
    }
    
    const loadGoals = async () => {
      try {
        const response = await learningProgressApi.getGoals()
        goals.value = response.data
      } catch (error) {
        ElMessage.error('加载学习目标失败')
        console.error('Load goals error:', error)
      }
    }
    
    const loadSubjects = async () => {
      try {
        const response = await subjectsApi.getSubjects()
        subjects.value = response.data.items || response.data
      } catch (error) {
        console.error('Load subjects error:', error)
      }
    }
    
    const updateProgressChart = () => {
      if (!progressChart.value || !progressData.value.progress_data) return
      
      try {
        const chart = echarts.init(progressChart.value)
        
        const dates = progressData.value.progress_data.map(item => item.date)
        const examCounts = progressData.value.progress_data.map(item => item.exams_count)
        const avgScores = progressData.value.progress_data.map(item => item.average_score)
        
        const option = {
          title: {
            text: '学习进度趋势',
            left: 'center',
            textStyle: {
              fontSize: 16,
              color: '#303133'
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross'
            }
          },
          legend: {
            data: ['考试次数', '平均分数'],
            top: 30
          },
          xAxis: {
            type: 'category',
            data: dates,
            axisLabel: {
              formatter: function(value) {
                return value.split('-').slice(1).join('-')
              }
            }
          },
          yAxis: [
            {
              type: 'value',
              name: '考试次数',
              position: 'left'
            },
            {
              type: 'value',
              name: '平均分数',
              position: 'right',
              min: 0,
              max: 100
            }
          ],
          series: [
            {
              name: '考试次数',
              type: 'bar',
              data: examCounts,
              itemStyle: {
                color: '#409eff'
              }
            },
            {
              name: '平均分数',
              type: 'line',
              yAxisIndex: 1,
              data: avgScores,
              smooth: true,
              lineStyle: {
                color: '#67c23a',
                width: 3
              },
              itemStyle: {
                color: '#67c23a'
              }
            }
          ]
        }
        
        chart.setOption(option)
        
        // 响应式调整
        window.addEventListener('resize', () => {
          chart.resize()
        })
      } catch (error) {
        console.error('Update progress chart error:', error)
      }
    }
    
    const generateReport = async () => {
      try {
        const params = {
          period: reportPeriod.value
        }
        const response = await learningProgressApi.generateReport(params)
        learningReport.value = response.data
      } catch (error) {
        ElMessage.error('生成学习报告失败')
        console.error('Generate report error:', error)
      }
    }
    
    const refreshRecommendations = () => {
      loadRecommendations()
    }
    
    const handleRecommendationAction = (recommendation) => {
      switch (recommendation.action) {
        case '参加考试':
          router.push('/user/exam-list')
          break
        case '复习错题':
          router.push('/user/wrong-answers')
          break
        case '安排考试':
          router.push('/user/exam-list')
          break
        case '加强练习':
          router.push('/user/exam-list')
          break
        default:
          ElMessage.info('功能开发中')
      }
    }
    
    const createGoal = async () => {
      try {
        await learningProgressApi.createGoal(goalForm)
        ElMessage.success('创建学习目标成功')
        showCreateGoalDialog.value = false
        Object.keys(goalForm).forEach(key => {
          goalForm[key] = key === 'target_score' ? 80 : ''
        })
        loadGoals()
      } catch (error) {
        ElMessage.error('创建学习目标失败')
        console.error('Create goal error:', error)
      }
    }
    
    const editGoal = (goal) => {
      // TODO: 实现编辑目标功能
      ElMessage.info('编辑功能开发中')
    }
    
    const deleteGoal = async (goal) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除学习目标"${goal.title}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await learningProgressApi.deleteGoal(goal.id)
        ElMessage.success('删除学习目标成功')
        loadGoals()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除学习目标失败')
          console.error('Delete goal error:', error)
        }
      }
    }
    
    // 工具方法
    const getPriorityTagType = (priority) => {
      const types = {
        high: 'danger',
        medium: 'warning',
        low: 'info'
      }
      return types[priority] || 'default'
    }
    
    const getPriorityLabel = (priority) => {
      const labels = {
        high: '高优先级',
        medium: '中优先级',
        low: '低优先级'
      }
      return labels[priority] || priority
    }
    
    const getGoalStatusType = (status) => {
      const types = {
        active: 'success',
        completed: 'success',
        paused: 'warning',
        cancelled: 'danger'
      }
      return types[status] || 'default'
    }
    
    const getGoalStatusLabel = (status) => {
      const labels = {
        active: '进行中',
        completed: '已完成',
        paused: '已暂停',
        cancelled: '已取消'
      }
      return labels[status] || status
    }
    
    // 生命周期
    onMounted(() => {
      loadSubjects()
      loadOverview()
      loadProgressData()
      loadAchievements()
      loadRecommendations()
      loadGoals()
    })
    
    return {
      loading,
      overview,
      progressData,
      achievements,
      recommendations,
      goals,
      learningReport,
      subjects,
      progressChart,
      progressPeriod,
      selectedSubject,
      reportPeriod,
      showCreateGoalDialog,
      goalForm,
      goalRules,
      unlockedAchievements,
      loadProgressData,
      updateProgressChart,
      generateReport,
      refreshRecommendations,
      handleRecommendationAction,
      createGoal,
      editGoal,
      deleteGoal,
      getPriorityTagType,
      getPriorityLabel,
      getGoalStatusType,
      getGoalStatusLabel
    }
  }
}
</script>

<style scoped>
.learning-progress {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
}

.header-info {
  display: flex;
  gap: 10px;
}

.overview-section {
  margin-bottom: 20px;
}

.overview-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.card-icon {
  font-size: 32px;
}

.card-info {
  flex: 1;
}

.card-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.card-label {
  font-size: 14px;
  color: #909399;
}

.progress-chart {
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.chart-controls {
  display: flex;
  gap: 10px;
}

.chart-content {
  height: 400px;
}

.chart-container {
  width: 100%;
  height: 100%;
}

.achievements-section {
  margin-bottom: 20px;
}

.achievements-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.achievements-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.achievements-summary {
  color: #909399;
  font-size: 14px;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.achievement-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.achievement-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.achievement-unlocked {
  border-color: #67c23a;
  background-color: #f0f9ff;
}

.achievement-icon {
  font-size: 32px;
}

.achievement-info {
  flex: 1;
}

.achievement-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.achievement-description {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.achievement-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-text {
  font-size: 12px;
  color: #909399;
}

.recommendations-section {
  margin-bottom: 20px;
}

.recommendations-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.recommendations-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.recommendation-item {
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #e4e7ed;
}

.priority-high {
  border-left-color: #f56c6c;
  background-color: #fef0f0;
}

.priority-medium {
  border-left-color: #e6a23c;
  background-color: #fef0e6;
}

.priority-low {
  border-left-color: #409eff;
  background-color: #f0f9ff;
}

.recommendation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.recommendation-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.recommendation-description {
  font-size: 14px;
  color: #606266;
  margin-bottom: 15px;
}

.goals-section {
  margin-bottom: 20px;
}

.goals-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.goals-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.goals-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.goal-item {
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.goal-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.goal-actions {
  display: flex;
  gap: 10px;
}

.goal-description {
  font-size: 14px;
  color: #606266;
  margin-bottom: 15px;
}

.goal-progress {
  margin-bottom: 15px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
}

.goal-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #909399;
}

.report-section {
  margin-bottom: 20px;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.report-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.report-controls {
  display: flex;
  gap: 10px;
}

.report-details {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.report-summary h4,
.report-analysis h4 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.stat-label {
  color: #606266;
  font-weight: 500;
}

.stat-value {
  color: #303133;
  font-weight: 600;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.analysis-content h5 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 14px;
}

.analysis-content ul {
  margin: 0;
  padding-left: 20px;
}

.analysis-content li {
  margin-bottom: 5px;
  color: #606266;
}

.strengths h5 {
  color: #67c23a;
}

.weaknesses h5 {
  color: #f56c6c;
}

.recommendations h5 {
  color: #409eff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .learning-progress {
    padding: 15px;
  }
  
  .overview-section .el-col {
    margin-bottom: 15px;
  }
  
  .chart-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .chart-content {
    height: 300px;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-stats {
    grid-template-columns: 1fr;
  }
}
</style>
