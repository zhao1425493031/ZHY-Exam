<template>
  <div class="statistics-analysis">
    <div class="page-header">
      <h1>统计分析</h1>
      <div class="header-info">
        <el-tag type="info">数据分析和统计</el-tag>
        <el-button type="primary" @click="exportStatistics" v-if="isAdmin">
          <el-icon><Download /></el-icon>
          导出统计
        </el-button>
      </div>
    </div>

    <!-- 仪表盘统计 -->
    <div class="dashboard-stats">
      <el-card>
        <div class="stats-header">
          <h3>仪表盘统计</h3>
          <div class="stats-actions">
            <el-button size="small" @click="loadDashboardStats">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
        
        <div class="stats-content" v-if="dashboardStats">
          <!-- 概览统计 -->
          <div class="overview-stats">
            <el-row :gutter="20">
              <el-col :span="6" v-for="(stat, key) in dashboardStats.overview" :key="key">
                <div class="stat-card">
                  <div class="stat-icon">
                    <el-icon :color="getStatColor(key)">
                      <component :is="getStatIcon(key)" />
                    </el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ stat }}</div>
                    <div class="stat-label">{{ getStatLabel(key) }}</div>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
          
          <!-- 图表区域 -->
          <div class="charts-section">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="chart-card">
                  <h4>科目统计</h4>
                  <div ref="subjectChartRef" class="chart-container"></div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="chart-card">
                  <h4>成绩分布</h4>
                  <div ref="scoreChartRef" class="chart-container"></div>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 详细统计 -->
    <div class="detailed-stats">
      <el-card>
        <div class="stats-tabs">
          <el-tabs v-model="activeTab" @tab-change="handleTabChange">
            <el-tab-pane label="考试统计" name="exam">
              <div class="tab-content">
                <div class="filter-section">
                  <el-form :model="examFilter" inline>
                    <el-form-item label="开始日期">
                      <el-date-picker
                        v-model="examFilter.start_date"
                        type="date"
                        placeholder="选择开始日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                      />
                    </el-form-item>
                    <el-form-item label="结束日期">
                      <el-date-picker
                        v-model="examFilter.end_date"
                        type="date"
                        placeholder="选择结束日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                      />
                    </el-form-item>
                    <el-form-item label="科目">
                      <el-select v-model="examFilter.subject_id" placeholder="选择科目" clearable>
                        <el-option
                          v-for="subject in subjects"
                          :key="subject.id"
                          :label="subject.name"
                          :value="subject.id"
                        />
                      </el-select>
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="loadExamStatistics">
                        <el-icon><Search /></el-icon>
                        查询
                      </el-button>
                    </el-form-item>
                  </el-form>
                </div>
                
                <div class="stats-results" v-if="examStatistics">
                  <div class="result-summary">
                    <el-row :gutter="20">
                      <el-col :span="8">
                        <div class="summary-item">
                          <div class="summary-value">{{ examStatistics.overview.total_exams }}</div>
                          <div class="summary-label">总考试数</div>
                        </div>
                      </el-col>
                      <el-col :span="8">
                        <div class="summary-item">
                          <div class="summary-value">{{ examStatistics.overview.completed_exams }}</div>
                          <div class="summary-label">完成考试数</div>
                        </div>
                      </el-col>
                      <el-col :span="8">
                        <div class="summary-item">
                          <div class="summary-value">{{ examStatistics.overview.avg_score }}</div>
                          <div class="summary-label">平均分</div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                  
                  <div class="score-distribution">
                    <h4>成绩分布</h4>
                    <el-table :data="examStatistics.score_distribution" stripe>
                      <el-table-column prop="label" label="等级" width="100" />
                      <el-table-column prop="range" label="分数范围" width="120" />
                      <el-table-column prop="count" label="人数" width="100" />
                      <el-table-column prop="percentage" label="占比" width="100">
                        <template #default="{ row }">
                          {{ row.percentage }}%
                        </template>
                      </el-table-column>
                      <el-table-column label="比例" width="200">
                        <template #default="{ row }">
                          <el-progress
                            :percentage="row.percentage"
                            :color="getScoreColor(row.label)"
                            :show-text="false"
                          />
                        </template>
                      </el-table-column>
                    </el-table>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="用户行为" name="user" v-if="isAdmin">
              <div class="tab-content">
                <div class="filter-section">
                  <el-form :model="userFilter" inline>
                    <el-form-item label="开始日期">
                      <el-date-picker
                        v-model="userFilter.start_date"
                        type="date"
                        placeholder="选择开始日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                      />
                    </el-form-item>
                    <el-form-item label="结束日期">
                      <el-date-picker
                        v-model="userFilter.end_date"
                        type="date"
                        placeholder="选择结束日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                      />
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="loadUserBehaviorStatistics">
                        <el-icon><Search /></el-icon>
                        查询
                      </el-button>
                    </el-form-item>
                  </el-form>
                </div>
                
                <div class="stats-results" v-if="userBehaviorStatistics">
                  <div class="result-summary">
                    <el-row :gutter="20">
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ userBehaviorStatistics.overview.total_users }}</div>
                          <div class="summary-label">总用户数</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ userBehaviorStatistics.overview.active_users }}</div>
                          <div class="summary-label">活跃用户数</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ userBehaviorStatistics.overview.admin_users }}</div>
                          <div class="summary-label">管理员数</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ userBehaviorStatistics.overview.regular_users }}</div>
                          <div class="summary-label">普通用户数</div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="试题分析" name="question" v-if="isAdmin">
              <div class="tab-content">
                <div class="filter-section">
                  <el-form :model="questionFilter" inline>
                    <el-form-item label="科目">
                      <el-select v-model="questionFilter.subject_id" placeholder="选择科目" clearable>
                        <el-option
                          v-for="subject in subjects"
                          :key="subject.id"
                          :label="subject.name"
                          :value="subject.id"
                        />
                      </el-select>
                    </el-form-item>
                    <el-form-item label="题型">
                      <el-select v-model="questionFilter.type" placeholder="选择题型" clearable>
                        <el-option label="单选题" value="single" />
                        <el-option label="多选题" value="multiple" />
                        <el-option label="判断题" value="judge" />
                        <el-option label="填空题" value="fill" />
                        <el-option label="简答题" value="essay" />
                      </el-select>
                    </el-form-item>
                    <el-form-item label="难度">
                      <el-select v-model="questionFilter.difficulty" placeholder="选择难度" clearable>
                        <el-option label="简单" value="easy" />
                        <el-option label="中等" value="medium" />
                        <el-option label="困难" value="hard" />
                      </el-select>
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="loadQuestionAnalysis">
                        <el-icon><Search /></el-icon>
                        查询
                      </el-button>
                    </el-form-item>
                  </el-form>
                </div>
                
                <div class="stats-results" v-if="questionAnalysis">
                  <div class="result-summary">
                    <el-row :gutter="20">
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ questionAnalysis.overview.total_questions }}</div>
                          <div class="summary-label">总试题数</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ questionAnalysis.overview.published_questions }}</div>
                          <div class="summary-label">已发布试题数</div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                  
                  <div class="question-stats">
                    <el-row :gutter="20">
                      <el-col :span="12">
                        <h4>题型分布</h4>
                        <el-table :data="questionAnalysis.type_statistics" stripe>
                          <el-table-column prop="type" label="题型" />
                          <el-table-column prop="count" label="数量" />
                        </el-table>
                      </el-col>
                      <el-col :span="12">
                        <h4>难度分布</h4>
                        <el-table :data="questionAnalysis.difficulty_statistics" stripe>
                          <el-table-column prop="difficulty" label="难度" />
                          <el-table-column prop="count" label="数量" />
                        </el-table>
                      </el-col>
                    </el-row>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="个人统计" name="personal" v-if="!isAdmin">
              <div class="tab-content">
                <div class="personal-stats" v-if="personalStats">
                  <div class="personal-overview">
                    <h4>个人概览</h4>
                    <el-row :gutter="20">
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ personalStats.overview.total_exams }}</div>
                          <div class="summary-label">总考试数</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ personalStats.overview.avg_score }}</div>
                          <div class="summary-label">平均分</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ personalStats.overview.max_score }}</div>
                          <div class="summary-label">最高分</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="summary-item">
                          <div class="summary-value">{{ personalStats.overview.wrong_answers_count }}</div>
                          <div class="summary-label">错题数</div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                  
                  <div class="personal-subjects">
                    <h4>科目表现</h4>
                    <el-table :data="personalStats.subject_performance" stripe>
                      <el-table-column prop="name" label="科目名称" />
                      <el-table-column prop="exam_count" label="考试次数" />
                      <el-table-column prop="avg_score" label="平均分" />
                      <el-table-column prop="max_score" label="最高分" />
                    </el-table>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Download, Refresh, Search, User, Book, QuestionFilled, Document, Trophy, Target, TrendCharts
} from '@element-plus/icons-vue'
import { statisticsApi } from '@/api/statistics'
import { subjectApi } from '@/api/subjects'
import { useAuthStore } from '@/stores/auth'
import * as echarts from 'echarts'

export default {
  name: 'StatisticsAnalysis',
  components: {
    Download,
    Refresh,
    Search,
    User,
    Book,
    QuestionFilled,
    Document,
    Trophy,
    Target,
    TrendCharts
  },
  setup() {
    const authStore = useAuthStore()
    
    // 响应式数据
    const loading = ref(false)
    const dashboardStats = ref(null)
    const examStatistics = ref(null)
    const userBehaviorStatistics = ref(null)
    const questionAnalysis = ref(null)
    const personalStats = ref(null)
    const subjects = ref([])
    const activeTab = ref('exam')
    const subjectChartRef = ref(null)
    const scoreChartRef = ref(null)
    
    // 筛选条件
    const examFilter = reactive({
      start_date: '',
      end_date: '',
      subject_id: null
    })
    
    const userFilter = reactive({
      start_date: '',
      end_date: ''
    })
    
    const questionFilter = reactive({
      subject_id: null,
      type: '',
      difficulty: ''
    })
    
    // 计算属性
    const isAdmin = computed(() => {
      return authStore.user?.role === 'admin'
    })
    
    // 方法
    const loadDashboardStats = async () => {
      try {
        loading.value = true
        const response = await statisticsApi.getDashboardStatistics()
        dashboardStats.value = response.data
        
        // 等待DOM更新后初始化图表
        await nextTick()
        initCharts()
      } catch (error) {
        ElMessage.error('加载仪表盘统计失败')
        console.error('Load dashboard stats error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadSubjects = async () => {
      try {
        const response = await subjectApi.getSubjects()
        subjects.value = response.data.items
      } catch (error) {
        console.error('Load subjects error:', error)
      }
    }
    
    const loadExamStatistics = async () => {
      try {
        loading.value = true
        const params = {
          start_date: examFilter.start_date,
          end_date: examFilter.end_date,
          subject_id: examFilter.subject_id
        }
        
        // 过滤空值
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await statisticsApi.getExamStatistics(params)
        examStatistics.value = response.data
      } catch (error) {
        ElMessage.error('加载考试统计失败')
        console.error('Load exam statistics error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadUserBehaviorStatistics = async () => {
      try {
        loading.value = true
        const params = {
          start_date: userFilter.start_date,
          end_date: userFilter.end_date
        }
        
        // 过滤空值
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await statisticsApi.getUserBehaviorStatistics(params)
        userBehaviorStatistics.value = response.data
      } catch (error) {
        ElMessage.error('加载用户行为统计失败')
        console.error('Load user behavior statistics error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadQuestionAnalysis = async () => {
      try {
        loading.value = true
        const params = {
          subject_id: questionFilter.subject_id,
          type: questionFilter.type,
          difficulty: questionFilter.difficulty
        }
        
        // 过滤空值
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await statisticsApi.getQuestionAnalysis(params)
        questionAnalysis.value = response.data
      } catch (error) {
        ElMessage.error('加载试题分析失败')
        console.error('Load question analysis error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadPersonalStats = async () => {
      try {
        loading.value = true
        const response = await statisticsApi.getLearningProgressStatistics()
        personalStats.value = response.data
      } catch (error) {
        ElMessage.error('加载个人统计失败')
        console.error('Load personal stats error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const handleTabChange = (tabName) => {
      activeTab.value = tabName
      
      // 根据标签页加载相应数据
      switch (tabName) {
        case 'exam':
          if (!examStatistics.value) {
            loadExamStatistics()
          }
          break
        case 'user':
          if (!userBehaviorStatistics.value) {
            loadUserBehaviorStatistics()
          }
          break
        case 'question':
          if (!questionAnalysis.value) {
            loadQuestionAnalysis()
          }
          break
        case 'personal':
          if (!personalStats.value) {
            loadPersonalStats()
          }
          break
      }
    }
    
    const exportStatistics = async () => {
      try {
        const response = await statisticsApi.exportStatistics()
        const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = '统计数据.json'
        link.click()
        window.URL.revokeObjectURL(url)
        ElMessage.success('导出统计数据成功')
      } catch (error) {
        ElMessage.error('导出统计数据失败')
        console.error('Export statistics error:', error)
      }
    }
    
    const initCharts = () => {
      if (!dashboardStats.value) return
      
      // 初始化科目统计图表
      if (subjectChartRef.value && dashboardStats.value.subject_statistics) {
        const subjectChart = echarts.init(subjectChartRef.value)
        const subjectData = dashboardStats.value.subject_statistics.map(item => ({
          name: item.name,
          value: item.exam_count
        }))
        
        const subjectOption = {
          title: {
            text: '科目考试统计',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          series: [{
            type: 'pie',
            radius: '50%',
            data: subjectData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }]
        }
        
        subjectChart.setOption(subjectOption)
      }
      
      // 初始化成绩分布图表
      if (scoreChartRef.value && examStatistics.value?.score_distribution) {
        const scoreChart = echarts.init(scoreChartRef.value)
        const scoreData = examStatistics.value.score_distribution.map(item => ({
          name: item.label,
          value: item.count
        }))
        
        const scoreOption = {
          title: {
            text: '成绩分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          series: [{
            type: 'pie',
            radius: '50%',
            data: scoreData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }]
        }
        
        scoreChart.setOption(scoreOption)
      }
    }
    
    // 工具方法
    const getStatIcon = (key) => {
      const icons = {
        total_users: 'User',
        active_users: 'User',
        total_subjects: 'Book',
        active_subjects: 'Book',
        total_questions: 'QuestionFilled',
        published_questions: 'QuestionFilled',
        total_exams: 'Document',
        published_exams: 'Document',
        total_exam_records: 'Document',
        completed_exams: 'Document',
        avg_score: 'Trophy',
        max_score: 'Trophy',
        wrong_answers_count: 'Target'
      }
      return icons[key] || 'Document'
    }
    
    const getStatColor = (key) => {
      const colors = {
        total_users: '#409eff',
        active_users: '#67c23a',
        total_subjects: '#e6a23c',
        active_subjects: '#67c23a',
        total_questions: '#f56c6c',
        published_questions: '#67c23a',
        total_exams: '#909399',
        published_exams: '#67c23a',
        total_exam_records: '#409eff',
        completed_exams: '#67c23a',
        avg_score: '#e6a23c',
        max_score: '#f56c6c',
        wrong_answers_count: '#f56c6c'
      }
      return colors[key] || '#909399'
    }
    
    const getStatLabel = (key) => {
      const labels = {
        total_users: '总用户数',
        active_users: '活跃用户数',
        total_subjects: '总科目数',
        active_subjects: '活跃科目数',
        total_questions: '总试题数',
        published_questions: '已发布试题数',
        total_exams: '总考试数',
        published_exams: '已发布考试数',
        total_exam_records: '总考试记录数',
        completed_exams: '已完成考试数',
        avg_score: '平均分',
        max_score: '最高分',
        wrong_answers_count: '错题数'
      }
      return labels[key] || key
    }
    
    const getScoreColor = (label) => {
      const colors = {
        '不及格': '#f56c6c',
        '及格': '#e6a23c',
        '中等': '#409eff',
        '良好': '#67c23a',
        '优秀': '#67c23a'
      }
      return colors[label] || '#909399'
    }
    
    // 生命周期
    onMounted(() => {
      loadDashboardStats()
      loadSubjects()
    })
    
    return {
      loading,
      dashboardStats,
      examStatistics,
      userBehaviorStatistics,
      questionAnalysis,
      personalStats,
      subjects,
      activeTab,
      subjectChartRef,
      scoreChartRef,
      examFilter,
      userFilter,
      questionFilter,
      isAdmin,
      loadDashboardStats,
      loadExamStatistics,
      loadUserBehaviorStatistics,
      loadQuestionAnalysis,
      loadPersonalStats,
      handleTabChange,
      exportStatistics,
      getStatIcon,
      getStatColor,
      getStatLabel,
      getScoreColor
    }
  }
}
</script>

<style scoped>
.statistics-analysis {
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

.dashboard-stats,
.detailed-stats {
  margin-bottom: 20px;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.stats-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.stats-content {
  padding: 20px 0;
}

.overview-stats {
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-card:hover {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 32px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.charts-section {
  margin-top: 30px;
}

.chart-card {
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.chart-card h4 {
  margin: 0 0 20px 0;
  color: #303133;
  text-align: center;
}

.chart-container {
  height: 300px;
}

.tab-content {
  padding: 20px 0;
}

.filter-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stats-results {
  padding: 20px 0;
}

.result-summary {
  margin-bottom: 30px;
}

.summary-item {
  text-align: center;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.summary-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.summary-label {
  font-size: 14px;
  color: #909399;
}

.score-distribution,
.question-stats {
  margin-top: 30px;
}

.score-distribution h4,
.question-stats h4 {
  margin: 0 0 20px 0;
  color: #303133;
}

.personal-stats {
  padding: 20px 0;
}

.personal-overview,
.personal-subjects {
  margin-bottom: 30px;
}

.personal-overview h4,
.personal-subjects h4 {
  margin: 0 0 20px 0;
  color: #303133;
}

:deep(.el-table .el-table__row) {
  cursor: pointer;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f7fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .statistics-analysis {
    padding: 15px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .overview-stats .el-col {
    margin-bottom: 15px;
  }
  
  .charts-section .el-col {
    margin-bottom: 20px;
  }
  
  .result-summary .el-col {
    margin-bottom: 15px;
  }
  
  .filter-section {
    padding: 15px;
  }
}
</style>
