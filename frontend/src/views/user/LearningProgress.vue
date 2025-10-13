<template>
  <div class="modern-learning-progress">
    <!-- 页面内容 -->
    <div class="page-content">
      <div class="content-container">
        <!-- 页面标题 -->
        <div class="modern-header">
          <div class="header-content">
            <div class="header-left">
              <div class="page-title">
                <div class="title-icon">
                  <el-icon><TrendCharts /></el-icon>
                </div>
                <div class="title-text">
                  <h1>学习进度</h1>
                  <p>跟踪学习进度和成就</p>
                </div>
              </div>
            </div>
            <div class="header-right">
              <el-button @click="goBackToPersonalCenter" class="back-btn">
                <el-icon><ArrowLeft /></el-icon>
                <span>返回个人中心</span>
              </el-button>
            </div>
          </div>
        </div>

        <!-- 统计概览 -->
        <div class="statistics-section">
          <div class="stats-card">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-icon">
                    <el-icon color="#409eff"><Document /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ overview.learning_stats?.total_exams || 0 }}</div>
                    <div class="stat-label">总考试次数</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-icon">
                    <el-icon color="#67c23a"><Trophy /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ overview.learning_stats?.average_score || 0 }}</div>
                    <div class="stat-label">平均分数</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-icon">
                    <el-icon color="#e6a23c"><TrendCharts /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ overview.learning_stats?.study_intensity || 0 }}%</div>
                    <div class="stat-label">学习强度</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-icon">
                    <el-icon color="#f56c6c"><Warning /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ overview.learning_stats?.review_rate || 0 }}%</div>
                    <div class="stat-label">复习率</div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
          </div>
        </div>

      <!-- 学习进度图表 -->
      <div class="table-section">
        <div class="table-card">
          <div class="table-header">
            <div class="table-title">
              <h3>学习进度趋势</h3>
              <p>跟踪您的学习进度变化</p>
            </div>
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
          <div class="table-container">
            <div ref="progressChart" class="chart-container"></div>
          </div>
        </div>
      </div>

      <!-- 学习成就 -->
      <div class="table-section">
        <div class="table-card">
          <div class="table-header">
            <div class="table-title">
              <h3>学习成就</h3>
              <p>已获得 {{ unlockedAchievements.length }} / {{ achievements.length }} 个成就</p>
            </div>
          </div>
          <div class="table-container">
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
          </div>
        </div>
      </div>

      <!-- 学习建议 -->
      <div class="table-section">
        <div class="table-card">
          <div class="table-header">
            <div class="table-title">
              <h3>学习建议</h3>
              <p>个性化学习建议和指导</p>
            </div>
            <div class="list-actions">
              <el-button size="small" @click="refreshRecommendations">
                <el-icon><Refresh /></el-icon>
                刷新建议
              </el-button>
            </div>
          </div>
          <div class="table-container">
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
          </div>
        </div>
      </div>

      <!-- 学习目标 -->
      <div class="table-section">
        <div class="table-card">
          <div class="table-header">
            <div class="table-title">
              <h3>学习目标</h3>
              <p>设置和管理您的学习目标</p>
            </div>
            <div class="list-actions">
              <el-button size="small" type="primary" @click="showCreateGoalDialog = true">
                <el-icon><Plus /></el-icon>
                新建目标
              </el-button>
            </div>
          </div>
          <div class="table-container">
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
          </div>
        </div>
      </div>

      <!-- 学习报告 -->
      <div class="table-section">
        <div class="table-card">
          <div class="table-header">
            <div class="table-title">
              <h3>学习报告</h3>
              <p>生成详细的学习分析报告</p>
            </div>
            <div class="list-actions">
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
          <div class="table-container">
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
                      <span class="stat-value">{{ learningReport.summary.wrong_questions }}</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">学习时长:</span>
                      <span class="stat-value">{{ learningReport.summary.study_hours }}小时</span>
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
          </div>
        </div>
      </div>
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
          <el-date-picker v-model="goalForm.target_date" type="date" placeholder="选择目标日期" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateGoalDialog = false">取消</el-button>
        <el-button type="primary" @click="createGoal">确定</el-button>
      </template>
    </el-dialog>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  TrendCharts,
  Document,
  Trophy,
  Warning,
  Medal,
  Star,
  Reading,
  Fire,
  Refresh,
  Plus,
  ArrowLeft
} from '@element-plus/icons-vue'
import { learningProgressApi } from '@/api/learning_progress'
import * as echarts from 'echarts'

export default {
  name: 'LearningProgress',
  components: {
    TrendCharts,
    Document,
    Trophy,
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
    const subjects = ref([])
    const achievements = ref([])
    const recommendations = ref([])
    const goals = ref([])
    const learningReport = ref(null)
    const progressPeriod = ref('7d')
    const selectedSubject = ref(null)
    const reportPeriod = ref('month')
    const showCreateGoalDialog = ref(false)
    const progressChart = ref(null)
    
    // 表单数据
    const goalForm = reactive({
      title: '',
      description: '',
      target_score: 0,
      target_date: ''
    })
    
    const goalRules = {
      title: [{ required: true, message: '请输入目标标题', trigger: 'blur' }],
      target_score: [{ required: true, message: '请输入目标分数', trigger: 'blur' }],
      target_date: [{ required: true, message: '请选择目标日期', trigger: 'change' }]
    }
    
    // 计算属性
    const unlockedAchievements = computed(() => {
      return achievements.value.filter(achievement => achievement.unlocked)
    })
    
    // 方法
    const goBackToPersonalCenter = () => {
      router.push('/user/dashboard')
    }
    
    const loadOverview = async () => {
      try {
        const response = await learningProgressApi.getOverview()
        overview.value = response.data
      } catch (error) {
        console.error('加载概览数据失败:', error)
        // 如果API调用失败，提供默认数据
        overview.value = {
          learning_stats: {
            total_exams: 0,
            average_score: 0,
            study_intensity: 0,
            review_rate: 0
          }
        }
      }
    }
    
    const loadSubjects = async () => {
      try {
        // 使用subjects API而不是learning progress API
        const { subjectsApi } = await import('@/api/subjects')
        const response = await subjectsApi.getSubjects({ status: 'active' })
        subjects.value = response.data.items || []
      } catch (error) {
        console.error('加载科目数据失败:', error)
        subjects.value = []
      }
    }
    
    const loadAchievements = async () => {
      try {
        const response = await learningProgressApi.getAchievements()
        achievements.value = response.data
      } catch (error) {
        console.error('加载成就数据失败:', error)
        // 提供默认成就数据
        achievements.value = [
          {
            id: 'first_exam',
            title: '初试锋芒',
            description: '完成第一次考试',
            icon: 'trophy',
            unlocked: false,
            progress: 0
          },
          {
            id: 'exam_master',
            title: '考试达人',
            description: '完成10次考试',
            icon: 'medal',
            unlocked: false,
            progress: 0
          }
        ]
      }
    }
    
    const loadRecommendations = async () => {
      try {
        const response = await learningProgressApi.getRecommendations()
        recommendations.value = response.data
      } catch (error) {
        console.error('加载建议数据失败:', error)
        // 提供默认建议
        recommendations.value = [
          {
            type: 'motivation',
            title: '开始学习',
            description: '完成第一次考试，开启学习记录',
            priority: 'high',
            action: '参加考试'
          }
        ]
      }
    }
    
    const loadGoals = async () => {
      try {
        const response = await learningProgressApi.getGoals()
        goals.value = response.data
      } catch (error) {
        console.error('加载目标数据失败:', error)
        goals.value = []
      }
    }
    
    const updateProgressChart = async () => {
      try {
        console.log('更新图表 - 时间周期:', progressPeriod.value, '科目:', selectedSubject.value) // 调试日志
        
        const response = await learningProgressApi.getChartData({
          period: progressPeriod.value,
          subject_id: selectedSubject.value
        })
        
        console.log('图表数据响应:', response) // 调试日志
        
        if (response.data) {
          renderProgressChart(response.data)
        } else {
          // 如果没有数据，使用默认数据
          renderProgressChart(getDefaultChartData())
        }
      } catch (error) {
        console.error('更新进度图表失败:', error)
        // 使用默认图表数据
        renderProgressChart(getDefaultChartData())
      }
    }
    
    const getDefaultChartData = () => {
      // 生成最近7天的模拟数据
      const dates = []
      const studyHours = [2.5, 1.8, 3.2, 2.1, 1.5, 2.8, 2.3]
      const examCounts = [1, 0, 2, 1, 0, 2, 1]
      
      const today = new Date()
      for (let i = 6; i >= 0; i--) {
        const date = new Date(today)
        date.setDate(date.getDate() - i)
        const dateStr = date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
        dates.push(dateStr)
      }
      
      return {
        dates: dates,
        studyHours: studyHours,
        examCounts: examCounts
      }
    }
    
    const renderProgressChart = (data) => {
      if (!progressChart.value) return
      
      console.log('渲染图表数据:', data) // 调试日志
      
      const chart = echarts.init(progressChart.value)
      const option = {
        title: {
          text: '学习进度趋势',
          left: 'center',
          textStyle: {
            color: '#2c3e50'
          }
        },
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          borderColor: '#e6e6e6',
          textStyle: {
            color: '#2c3e50'
          }
        },
        legend: {
          top: 30,
          textStyle: {
            color: '#2c3e50'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          top: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: data.dates || [],
          axisLine: {
            lineStyle: {
              color: '#e6e6e6'
            }
          },
          axisLabel: {
            color: '#7f8c8d'
          }
        },
        yAxis: [{
          type: 'value',
          name: '学习时长(小时)',
          position: 'left',
          axisLine: {
            lineStyle: {
              color: '#e6e6e6'
            }
          },
          axisLabel: {
            color: '#7f8c8d'
          }
        }, {
          type: 'value',
          name: '考试次数',
          position: 'right',
          axisLine: {
            lineStyle: {
              color: '#e6e6e6'
            }
          },
          axisLabel: {
            color: '#7f8c8d'
          }
        }],
        series: [{
          name: '学习时长(小时)',
          type: 'line',
          yAxisIndex: 0,
          data: data.studyHours || [],
          smooth: true,
          lineStyle: {
            color: '#667eea',
            width: 3
          },
          itemStyle: {
            color: '#667eea'
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [{
                offset: 0, color: 'rgba(102, 126, 234, 0.3)'
              }, {
                offset: 1, color: 'rgba(102, 126, 234, 0.05)'
              }]
            }
          }
        }, {
          name: '考试次数',
          type: 'bar',
          yAxisIndex: 1,
          data: data.examCounts || [],
          itemStyle: {
            color: '#764ba2',
            borderRadius: [4, 4, 0, 0]
          }
        }]
      }
      
      chart.setOption(option)
      
      // 响应式调整
      const resizeHandler = () => {
        chart.resize()
      }
      window.addEventListener('resize', resizeHandler)
      
      // 清理事件监听器（在组件卸载时）
      return () => {
        window.removeEventListener('resize', resizeHandler)
        chart.dispose()
      }
    }
    
    const generateReport = async () => {
      try {
        const response = await learningProgressApi.generateReport({
          period: reportPeriod.value
        })
        learningReport.value = response.data
        ElMessage.success('学习报告生成成功')
      } catch (error) {
        console.error('生成学习报告失败:', error)
        ElMessage.error('生成学习报告失败')
      }
    }
    
    const refreshRecommendations = async () => {
      await loadRecommendations()
      ElMessage.success('建议已刷新')
    }
    
    const createGoal = async () => {
      try {
        await learningProgressApi.createGoal(goalForm)
        ElMessage.success('目标创建成功')
        showCreateGoalDialog.value = false
        Object.assign(goalForm, {
          title: '',
          description: '',
          target_score: 0,
          target_date: ''
        })
        await loadGoals()
      } catch (error) {
        console.error('创建目标失败:', error)
        ElMessage.error('创建目标失败')
      }
    }
    
    const editGoal = (goal) => {
      Object.assign(goalForm, goal)
      showCreateGoalDialog.value = true
    }
    
    const deleteGoal = async (goal) => {
      try {
        await ElMessageBox.confirm('确定要删除这个目标吗？', '确认删除', {
          type: 'warning'
        })
        await learningProgressApi.deleteGoal(goal.id)
        ElMessage.success('目标删除成功')
        await loadGoals()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除目标失败:', error)
          ElMessage.error('删除目标失败')
        }
      }
    }
    
    const handleRecommendationAction = (recommendation) => {
      ElMessage.info(`执行建议: ${recommendation.action}`)
    }
    
    const getPriorityTagType = (priority) => {
      const types = {
        high: 'danger',
        medium: 'warning',
        low: 'success'
      }
      return types[priority] || 'info'
    }
    
    const getPriorityLabel = (priority) => {
      const labels = {
        high: '高优先级',
        medium: '中优先级',
        low: '低优先级'
      }
      return labels[priority] || '未知'
    }
    
    const getGoalStatusType = (status) => {
      const types = {
        active: 'primary',
        completed: 'success',
        expired: 'danger'
      }
      return types[status] || 'info'
    }
    
    const getGoalStatusLabel = (status) => {
      const labels = {
        active: '进行中',
        completed: '已完成',
        expired: '已过期'
      }
      return labels[status] || '未知'
    }
    
    // 生命周期
    onMounted(async () => {
      loading.value = true
      try {
        await Promise.all([
          loadOverview(),
          loadSubjects(),
          loadAchievements(),
          loadRecommendations(),
          loadGoals()
        ])
        
        await nextTick()
        updateProgressChart()
      } catch (error) {
        console.error('初始化数据失败:', error)
      } finally {
        loading.value = false
      }
    })
    
    return {
      loading,
      overview,
      subjects,
      achievements,
      recommendations,
      goals,
      learningReport,
      progressPeriod,
      selectedSubject,
      reportPeriod,
      showCreateGoalDialog,
      progressChart,
      goalForm,
      goalRules,
      unlockedAchievements,
      goBackToPersonalCenter,
      updateProgressChart,
      generateReport,
      refreshRecommendations,
      createGoal,
      editGoal,
      deleteGoal,
      handleRecommendationAction,
      getPriorityTagType,
      getPriorityLabel,
      getGoalStatusType,
      getGoalStatusLabel,
      ArrowLeft
    }
  }
}
</script>

<style scoped>
.modern-learning-progress {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.page-content {
  max-width: 1800px;
  margin: 0 auto;
}

.content-container {
  width: 100%;
}

/* 页面标题 */
.modern-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 24px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1800px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left .page-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title-icon {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  backdrop-filter: blur(10px);
}

.title-text h1 {
  color: white;
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 4px 0;
  letter-spacing: -0.5px;
}

.title-text p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin: 0;
  font-weight: 500;
}

.header-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.back-btn {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 12px;
  padding: 12px 24px;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* 统计卡片 */
.statistics-section {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.stats-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stat-card {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  margin-bottom: 1rem;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.stat-content:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border-color: rgba(102, 126, 234, 0.3);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #7f8c8d;
  font-weight: 500;
}

.table-section {
  margin-bottom: 2rem;
}

.table-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(102, 126, 234, 0.1);
}

.table-title h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.table-title p {
  margin: 8px 0 0 0;
  color: #7f8c8d;
  font-size: 14px;
}

.list-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.chart-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.table-container {
  min-height: 200px;
}

.chart-container {
  height: 400px;
  width: 100%;
}

.achievements-content {
  padding: 20px 0;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.achievement-item {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.achievement-item.achievement-unlocked {
  border-color: #67c23a;
  background: rgba(103, 194, 58, 0.1);
}

.achievement-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
  font-size: 24px;
}

.achievement-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.achievement-description {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 15px;
}

.achievement-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-text {
  font-size: 12px;
  color: #7f8c8d;
  font-weight: 600;
}

.recommendations-content {
  padding: 20px 0;
}

.no-recommendations,
.no-goals,
.no-report {
  text-align: center;
  padding: 40px 0;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.recommendation-item {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
  border-left: 4px solid #e6a23c;
  transition: all 0.3s ease;
}

.recommendation-item.priority-high {
  border-left-color: #f56c6c;
}

.recommendation-item.priority-medium {
  border-left-color: #e6a23c;
}

.recommendation-item.priority-low {
  border-left-color: #67c23a;
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
  color: #2c3e50;
}

.recommendation-description {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 15px;
  line-height: 1.6;
}

.recommendation-action {
  text-align: right;
}

.goals-content {
  padding: 20px 0;
}

.goals-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.goal-item {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid rgba(102, 126, 234, 0.1);
  transition: all 0.3s ease;
}

.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.goal-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.goal-actions {
  display: flex;
  gap: 8px;
}

.goal-description {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 15px;
  line-height: 1.6;
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
  color: #7f8c8d;
}

.goal-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #7f8c8d;
}

.report-content {
  padding: 20px 0;
}

.report-details {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.report-summary {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
}

.report-summary h4 {
  margin: 0 0 20px 0;
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 12px;
}

.stat-item .stat-label {
  color: #7f8c8d;
  font-weight: 500;
}

.stat-item .stat-value {
  font-weight: 600;
  color: #2c3e50;
  font-size: 16px;
}

.report-analysis {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
}

.report-analysis h4 {
  margin: 0 0 20px 0;
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.strengths,
.weaknesses,
.recommendations {
  padding: 15px;
  border-radius: 12px;
}

.strengths {
  background: rgba(103, 194, 58, 0.1);
  border-left: 4px solid #67c23a;
}

.weaknesses {
  background: rgba(245, 108, 108, 0.1);
  border-left: 4px solid #f56c6c;
}

.recommendations {
  background: rgba(230, 162, 60, 0.1);
  border-left: 4px solid #e6a23c;
}

.strengths h5,
.weaknesses h5,
.recommendations h5 {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.strengths ul,
.weaknesses ul,
.recommendations ul {
  margin: 0;
  padding-left: 20px;
}

.strengths li,
.weaknesses li,
.recommendations li {
  color: #7f8c8d;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 5px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .header-content {
    max-width: 100%;
    padding-left: 16px;
    padding-right: 16px;
  }
}

@media (max-width: 768px) {
  .learning-progress {
    padding: 1rem;
  }
  
  .modern-header {
    padding: 16px 0;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .header-right {
    align-self: flex-end;
  }
  
  .title-text h1 {
    font-size: 24px;
  }
  
  .stats-card,
  .table-card {
    padding: 1rem;
  }
  
  .table-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-stats {
    grid-template-columns: 1fr;
  }
}
</style>