<template>
  <div class="modern-statistics-analysis">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="title-text">
      <h1>统计分析</h1>
              <p>数据分析和统计报告</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="exportStatistics" v-if="isAdmin" class="export-btn" :loading="loading">
          <el-icon><Download /></el-icon>
            <span>导出统计</span>
          </el-button>
          <el-button @click="loadDashboardStats" class="refresh-btn" :loading="loading">
            <el-icon><Refresh /></el-icon>
            <span>刷新数据</span>
          </el-button>
          <el-button @click="$router.push('/admin')" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回控制台</span>
        </el-button>
        </div>
      </div>
    </div>

    <!-- 仪表盘统计概览 -->
    <div class="dashboard-section" v-if="dashboardStats">
      <div class="dashboard-card">
        <div class="dashboard-header">
          <div class="dashboard-title">
            <h3>仪表盘概览</h3>
            <p>系统核心数据统计</p>
          </div>
        </div>
        
        <div class="stats-grid">
          <div 
            v-for="(stat, key) in dashboardStats.overview" 
            :key="key"
            class="stat-card"
          >
                  <div class="stat-icon" :class="getStatType(key)">
                    <el-icon color="white">
                      <component :is="getStatIcon(key)" />
                    </el-icon>
                  </div>
            <div class="stat-content">
                    <div class="stat-value">{{ stat }}</div>
                    <div class="stat-label">{{ getStatLabel(key) }}</div>
                  </div>
                </div>
          </div>
          
          <!-- 图表区域 -->
        <div class="charts-grid" v-if="dashboardStats.subject_statistics">
                <div class="chart-card">
            <div class="chart-header">
                  <h4>科目统计</h4>
              <p>各科目考试数量分布</p>
            </div>
            <div class="chart-content">
                  <div ref="subjectChartRef" class="chart-container"></div>
                </div>
          </div>
          
                <div class="chart-card">
            <div class="chart-header">
                  <h4>成绩分布</h4>
              <p>考试成绩等级分布</p>
            </div>
            <div class="chart-content">
                  <div ref="scoreChartRef" class="chart-container"></div>
                </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 详细统计分析 -->
    <div class="analysis-section">
      <div class="analysis-card">
        <div class="analysis-header">
          <div class="analysis-title">
            <h3>详细分析</h3>
            <p>多维度数据深度分析</p>
          </div>
        </div>
        
        <div class="analysis-tabs">
          <el-tabs v-model="activeTab" @tab-change="handleTabChange" class="modern-tabs">
            <!-- 考试统计 -->
            <el-tab-pane name="exam">
              <template #label>
                <span class="tab-label">
                  <el-icon><DocumentChecked /></el-icon>
                  <span>考试统计</span>
                </span>
              </template>
              
              <div class="tab-content">
                <!-- 筛选区域 -->
                <div class="filter-section">
                  <div class="filter-card">
                    <div class="filter-header">
                      <h4>筛选条件</h4>
                      <p>选择分析条件</p>
                    </div>
                    <div class="filter-form">
                  <el-form :model="examFilter" inline>
                        <el-form-item>
                      <el-date-picker
                        v-model="examFilter.start_date"
                        type="date"
                            placeholder="开始日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                            class="date-picker"
                      />
                    </el-form-item>
                        <el-form-item>
                      <el-date-picker
                        v-model="examFilter.end_date"
                        type="date"
                            placeholder="结束日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                            class="date-picker"
                      />
                    </el-form-item>
                        <el-form-item>
                          <el-select v-model="examFilter.subject_id" placeholder="选择科目" clearable class="search-select">
                        <el-option
                          v-for="subject in subjects"
                          :key="subject.id"
                          :label="subject.name"
                          :value="subject.id"
                        />
                      </el-select>
                    </el-form-item>
                    <el-form-item>
                          <el-button type="primary" @click="loadExamStatistics" class="search-btn" :loading="loading">
                        <el-icon><Search /></el-icon>
                            <span>查询</span>
                          </el-button>
                          <el-button @click="resetExamFilter" class="reset-btn">
                            <el-icon><Refresh /></el-icon>
                            <span>重置</span>
                      </el-button>
                    </el-form-item>
                  </el-form>
                    </div>
                  </div>
                </div>
                
                <!-- 统计结果 -->
                <div class="results-section" v-if="examStatistics">
                  <div class="results-summary">
                    <div class="summary-card">
                      <div class="summary-icon total">
                        <el-icon><DocumentChecked /></el-icon>
                      </div>
                      <div class="summary-content">
                          <div class="summary-value">{{ examStatistics.overview.total_exams }}</div>
                          <div class="summary-label">总考试数</div>
                        </div>
                    </div>
                    
                    <div class="summary-card">
                      <div class="summary-icon completed">
                        <el-icon><Check /></el-icon>
                      </div>
                      <div class="summary-content">
                          <div class="summary-value">{{ examStatistics.overview.completed_exams }}</div>
                          <div class="summary-label">完成考试数</div>
                        </div>
                    </div>
                    
                    <div class="summary-card">
                      <div class="summary-icon average">
                        <el-icon><TrendCharts /></el-icon>
                      </div>
                      <div class="summary-content">
                          <div class="summary-value">{{ examStatistics.overview.avg_score }}</div>
                          <div class="summary-label">平均分</div>
                        </div>
                    </div>
                  </div>
                  
                  <div class="score-distribution-section">
                    <div class="section-header">
                    <h4>成绩分布</h4>
                      <p>各分数段人数分布情况</p>
                    </div>
                    <div class="distribution-table">
                      <el-table :data="examStatistics.score_distribution" stripe class="modern-table">
                        <el-table-column prop="label" label="等级" width="100">
                          <template #default="{ row }">
                            <el-tag :type="getScoreTagType(row.label)" size="small">
                              {{ row.label }}
                            </el-tag>
                          </template>
                        </el-table-column>
                      <el-table-column prop="range" label="分数范围" width="120" />
                      <el-table-column prop="count" label="人数" width="100" />
                      <el-table-column prop="percentage" label="占比" width="100">
                        <template #default="{ row }">
                          {{ row.percentage }}%
                        </template>
                      </el-table-column>
                        <el-table-column label="比例" min-width="200">
                        <template #default="{ row }">
                            <div class="progress-bar">
                              <div 
                                class="progress-fill" 
                                :style="{ 
                                  width: `${row.percentage}%`,
                                  backgroundColor: getScoreColor(row.label)
                                }"
                              ></div>
                            </div>
                        </template>
                      </el-table-column>
                    </el-table>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <!-- 用户行为统计 -->
            <el-tab-pane name="user" v-if="isAdmin">
              <template #label>
                <span class="tab-label">
                  <el-icon><User /></el-icon>
                  <span>用户行为</span>
                </span>
              </template>
              
              <div class="tab-content">
                <div class="filter-section">
                  <div class="filter-card">
                    <div class="filter-header">
                      <h4>筛选条件</h4>
                      <p>选择分析时间范围</p>
                    </div>
                    <div class="filter-form">
                  <el-form :model="userFilter" inline>
                        <el-form-item>
                      <el-date-picker
                        v-model="userFilter.start_date"
                        type="date"
                            placeholder="开始日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                            class="date-picker"
                      />
                    </el-form-item>
                        <el-form-item>
                      <el-date-picker
                        v-model="userFilter.end_date"
                        type="date"
                            placeholder="结束日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                            class="date-picker"
                      />
                    </el-form-item>
                    <el-form-item>
                          <el-button type="primary" @click="loadUserBehaviorStatistics" class="search-btn" :loading="loading">
                        <el-icon><Search /></el-icon>
                            <span>查询</span>
                          </el-button>
                          <el-button @click="resetUserFilter" class="reset-btn">
                            <el-icon><Refresh /></el-icon>
                            <span>重置</span>
                      </el-button>
                    </el-form-item>
                  </el-form>
                    </div>
                  </div>
                </div>
                
                <div class="results-section" v-if="userBehaviorStatistics">
                  <div class="results-summary">
                    <div class="summary-card">
                      <div class="summary-icon total">
                        <el-icon><User /></el-icon>
                      </div>
                      <div class="summary-content">
                          <div class="summary-value">{{ userBehaviorStatistics.overview.total_users }}</div>
                          <div class="summary-label">总用户数</div>
                        </div>
                    </div>
                    
                    <div class="summary-card">
                      <div class="summary-icon active">
                        <el-icon><UserFilled /></el-icon>
                      </div>
                      <div class="summary-content">
                          <div class="summary-value">{{ userBehaviorStatistics.overview.active_users }}</div>
                          <div class="summary-label">活跃用户数</div>
                        </div>
                    </div>
                    
                    <div class="summary-card">
                      <div class="summary-icon admin">
                        <el-icon><Avatar /></el-icon>
                      </div>
                      <div class="summary-content">
                          <div class="summary-value">{{ userBehaviorStatistics.overview.admin_users }}</div>
                          <div class="summary-label">管理员数</div>
                        </div>
                    </div>
                    
                    <div class="summary-card">
                      <div class="summary-icon regular">
                        <el-icon><User /></el-icon>
                      </div>
                      <div class="summary-content">
                          <div class="summary-value">{{ userBehaviorStatistics.overview.regular_users }}</div>
                          <div class="summary-label">普通用户数</div>
                        </div>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <!-- 试题分析 -->
            <el-tab-pane name="question" v-if="isAdmin">
              <template #label>
                <span class="tab-label">
                  <el-icon><QuestionFilled /></el-icon>
                  <span>试题分析</span>
                </span>
              </template>
              
              <div class="tab-content">
                <div class="filter-section">
                  <div class="filter-card">
                    <div class="filter-header">
                      <h4>筛选条件</h4>
                      <p>选择分析维度</p>
                    </div>
                    <div class="filter-form">
                  <el-form :model="questionFilter" inline>
                        <el-form-item>
                          <el-select v-model="questionFilter.subject_id" placeholder="选择科目" clearable class="search-select">
                        <el-option
                          v-for="subject in subjects"
                          :key="subject.id"
                          :label="subject.name"
                          :value="subject.id"
                        />
                      </el-select>
                    </el-form-item>
                        <el-form-item>
                          <el-select v-model="questionFilter.type" placeholder="选择题型" clearable class="search-select">
                        <el-option label="单选题" value="single" />
                        <el-option label="多选题" value="multiple" />
                        <el-option label="判断题" value="judge" />
                        <el-option label="填空题" value="fill" />
                        <el-option label="简答题" value="essay" />
                      </el-select>
                    </el-form-item>
                        <el-form-item>
                          <el-select v-model="questionFilter.difficulty" placeholder="选择难度" clearable class="search-select">
                        <el-option label="简单" value="easy" />
                        <el-option label="中等" value="medium" />
                        <el-option label="困难" value="hard" />
                      </el-select>
                    </el-form-item>
                    <el-form-item>
                          <el-button type="primary" @click="loadQuestionAnalysis" class="search-btn" :loading="loading">
                        <el-icon><Search /></el-icon>
                            <span>查询</span>
                          </el-button>
                          <el-button @click="resetQuestionFilter" class="reset-btn">
                            <el-icon><Refresh /></el-icon>
                            <span>重置</span>
                      </el-button>
                    </el-form-item>
                  </el-form>
                    </div>
                  </div>
                </div>
                
                <div class="results-section" v-if="questionAnalysis">
                  <div class="results-summary">
                    <div class="summary-card">
                      <div class="summary-icon total">
                        <el-icon><QuestionFilled /></el-icon>
                      </div>
                      <div class="summary-content">
                          <div class="summary-value">{{ questionAnalysis.overview.total_questions }}</div>
                          <div class="summary-label">总试题数</div>
                        </div>
                    </div>
                    
                    <div class="summary-card">
                      <div class="summary-icon published">
                        <el-icon><Document /></el-icon>
                      </div>
                      <div class="summary-content">
                          <div class="summary-value">{{ questionAnalysis.overview.published_questions }}</div>
                          <div class="summary-label">已发布试题数</div>
                        </div>
                    </div>
                  </div>
                  
                  <div class="question-stats-grid">
                    <div class="stats-card">
                      <div class="stats-header">
                        <h4>题型分布</h4>
                        <p>各类型题目数量统计</p>
                      </div>
                      <div class="stats-content">
                        <el-table :data="questionAnalysis.type_statistics" stripe class="modern-table">
                          <el-table-column prop="type" label="题型" />
                          <el-table-column prop="count" label="数量" />
                        </el-table>
                      </div>
                    </div>
                    
                    <div class="stats-card">
                      <div class="stats-header">
                        <h4>难度分布</h4>
                        <p>各难度题目数量统计</p>
                      </div>
                      <div class="stats-content">
                        <el-table :data="questionAnalysis.difficulty_statistics" stripe class="modern-table">
                          <el-table-column prop="difficulty" label="难度" />
                          <el-table-column prop="count" label="数量" />
                        </el-table>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <!-- 个人统计 -->
            <el-tab-pane name="personal" v-if="!isAdmin">
              <template #label>
                <span class="tab-label">
                  <el-icon><User /></el-icon>
                  <span>个人统计</span>
                </span>
              </template>
              
              <div class="tab-content">
                <div class="personal-stats-section" v-if="personalStats">
                  <div class="personal-overview">
                    <div class="section-header">
                    <h4>个人概览</h4>
                      <p>个人学习数据统计</p>
                    </div>
                    
                    <div class="results-summary">
                      <div class="summary-card">
                        <div class="summary-icon total">
                          <el-icon><DocumentChecked /></el-icon>
                        </div>
                        <div class="summary-content">
                          <div class="summary-value">{{ personalStats.overview.total_exams }}</div>
                          <div class="summary-label">总考试数</div>
                        </div>
                      </div>
                      
                      <div class="summary-card">
                        <div class="summary-icon average">
                          <el-icon><TrendCharts /></el-icon>
                        </div>
                        <div class="summary-content">
                          <div class="summary-value">{{ personalStats.overview.avg_score }}</div>
                          <div class="summary-label">平均分</div>
                        </div>
                      </div>
                      
                      <div class="summary-card">
                        <div class="summary-icon max">
                          <el-icon><Trophy /></el-icon>
                        </div>
                        <div class="summary-content">
                          <div class="summary-value">{{ personalStats.overview.max_score }}</div>
                          <div class="summary-label">最高分</div>
                        </div>
                      </div>
                      
                      <div class="summary-card">
                        <div class="summary-icon wrong">
                          <el-icon><Warning /></el-icon>
                        </div>
                        <div class="summary-content">
                          <div class="summary-value">{{ personalStats.overview.wrong_answers_count }}</div>
                          <div class="summary-label">错题数</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="personal-subjects">
                    <div class="section-header">
                    <h4>科目表现</h4>
                      <p>各科目学习情况统计</p>
                    </div>
                    <div class="subjects-table">
                      <el-table :data="personalStats.subject_performance" stripe class="modern-table">
                        <el-table-column prop="name" label="科目名称" min-width="150" />
                        <el-table-column prop="exam_count" label="考试次数" width="120" />
                        <el-table-column prop="avg_score" label="平均分" width="120">
                          <template #default="{ row }">
                            <el-tag :type="getScoreTagType(row.avg_score)" size="small">
                              {{ row.avg_score }}分
                            </el-tag>
                          </template>
                        </el-table-column>
                        <el-table-column prop="max_score" label="最高分" width="120">
                          <template #default="{ row }">
                            <el-tag :type="getScoreTagType(row.max_score)" size="small">
                              {{ row.max_score }}分
                            </el-tag>
                          </template>
                        </el-table-column>
                    </el-table>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Download, Refresh, Search, User, Book, QuestionFilled, Document, Trophy, Target, TrendCharts,
  ArrowLeft, DocumentChecked, Check, UserFilled, Avatar, Warning
} from '@element-plus/icons-vue'
import { statisticsApi } from '@/api/statistics'
import { subjectsApi } from '@/api/subjects'
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
    TrendCharts,
    ArrowLeft,
    DocumentChecked,
    Check,
    UserFilled,
    Avatar,
    Warning
  },
  setup() {
    const router = useRouter()
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
        const response = await subjectsApi.getSubjects()
        subjects.value = response.data.items || response.data
      } catch (error) {
        console.error('Load subjects error:', error)
        ElMessage.error('加载科目列表失败')
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

    const getStatType = (key) => {
      const types = {
        total_users: 'users',
        active_users: 'active',
        total_subjects: 'subjects',
        active_subjects: 'subjects',
        total_questions: 'questions',
        published_questions: 'published',
        total_exams: 'exams',
        published_exams: 'published',
        total_exam_records: 'records',
        completed_exams: 'completed',
        avg_score: 'score',
        max_score: 'score',
        wrong_answers_count: 'questions'
      }
      return types[key] || 'users'
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
    
    const getScoreTagType = (score) => {
      if (score >= 90) return 'success'
      if (score >= 80) return ''
      if (score >= 70) return 'warning'
      return 'danger'
    }
    
    // 重置筛选条件方法
    const resetExamFilter = () => {
      examFilter.start_date = ''
      examFilter.end_date = ''
      examFilter.subject_id = null
      examStatistics.value = null
    }
    
    const resetUserFilter = () => {
      userFilter.start_date = ''
      userFilter.end_date = ''
      userBehaviorStatistics.value = null
    }
    
    const resetQuestionFilter = () => {
      questionFilter.subject_id = null
      questionFilter.type = ''
      questionFilter.difficulty = ''
      questionAnalysis.value = null
    }
    
    // 生命周期
    onMounted(() => {
      loadDashboardStats()
      loadSubjects()
    })
    
    return {
      router,
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
      resetExamFilter,
      resetUserFilter,
      resetQuestionFilter,
      getStatIcon,
      getStatColor,
      getStatLabel,
      getStatType,
      getScoreColor,
      getScoreTagType
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-statistics-analysis {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.modern-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 24px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  
  .header-content {
    max-width: 1800px;
    margin: 0 auto;
    padding: 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
    
    .header-left {
      .page-title {
        display: flex;
        align-items: center;
        gap: 16px;
        
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
        
        .title-text {
          h1 {
            color: white;
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 4px 0;
            letter-spacing: -0.5px;
          }
          
          p {
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
  margin: 0;
          }
        }
      }
}

    .header-right {
  display: flex;
      gap: 12px;
      
      .export-btn, .refresh-btn, .back-btn {
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-2px);
        }
      }
      
      .export-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border: none;
        color: white;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
        
        &:hover {
          box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }
      }
      
      .refresh-btn {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border: none;
        color: white;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
        
        &:hover {
          box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        }
      }
      
      .back-btn {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        
        &:hover {
          background: rgba(255, 255, 255, 0.2);
        }
      }
    }
  }
}

.dashboard-section {
  padding: 32px;
  
  .dashboard-card {
    max-width: 1800px;
    margin: 0 auto;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15), 0 8px 32px rgba(102, 126, 234, 0.1);
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%);
      background-size: 200% 100%;
      animation: shimmer 3s linear infinite;
    }
    
    .dashboard-header {
      margin-bottom: 32px;
      
      .dashboard-title {
        h3 {
          font-size: 24px;
          font-weight: 700;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin: 0 0 8px 0;
          letter-spacing: -0.5px;
        }
        
        p {
          color: #666;
          font-size: 15px;
          margin: 0;
          font-weight: 500;
        }
      }
    }
    
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
      margin-bottom: 40px;

.stat-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.8) 100%);
        border-radius: 20px;
        padding: 28px;
  display: flex;
  align-items: center;
        gap: 20px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        
        &::before {
          content: '';
          position: absolute;
          top: -50%;
          right: -50%;
          width: 200%;
          height: 200%;
          background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
          opacity: 0;
          transition: opacity 0.4s ease;
        }
        
        &:hover {
          transform: translateY(-8px) scale(1.02);
          box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
          border-color: rgba(102, 126, 234, 0.3);
          
          &::before {
            opacity: 1;
}

.stat-icon {
            transform: scale(1.15) rotate(8deg);
            box-shadow: 0 16px 32px rgba(0, 0, 0, 0.25), 0 8px 16px rgba(0, 0, 0, 0.15);
          }
          
          .stat-value {
            transform: scale(1.05);
          }
        }
        
        .stat-icon {
          width: 72px;
          height: 72px;
          border-radius: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
  font-size: 32px;
          flex-shrink: 0;
          box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15), 0 4px 8px rgba(0, 0, 0, 0.1);
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          position: relative;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          
          &::before {
            content: '';
            position: absolute;
            inset: -3px;
            border-radius: 23px;
            padding: 3px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%, #f093fb 100%);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0;
            transition: opacity 0.4s ease;
          }
          
          &::after {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.05) 100%);
            opacity: 0;
            transition: opacity 0.4s ease;
          }
          
          &.users {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          }
          
          &.subjects {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          }
          
          &.exams {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
          }
          
          &.questions {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
          }
          
          &.records {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
          }
          
          &.score {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #333;
          }
          
          &.active {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            color: #333;
          }
          
          &.completed {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            color: #333;
          }
          
          &.published {
            background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
            color: #333;
          }
        }
        
        &:hover .stat-icon {
          &::before {
            opacity: 1;
          }
          
          &::after {
            opacity: 1;
          }
        }
        
        .stat-content {
          flex: 1;

.stat-value {
            font-size: 36px;
            font-weight: 800;
            color: #1a1a1a;
            margin-bottom: 6px;
            letter-spacing: -1.5px;
            transition: all 0.3s ease;
            background: linear-gradient(135deg, #1a1a1a 0%, #4a4a4a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
}

.stat-label {
  font-size: 14px;
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
}
        }
      }
}
    
    .charts-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
      gap: 24px;

.chart-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.8) 100%);
        border-radius: 20px;
        padding: 28px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        
        &::before {
          content: '';
          position: absolute;
          top: 0;
          left: -100%;
          width: 100%;
          height: 100%;
          background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
          transition: left 0.5s ease;
        }
        
        &:hover {
          transform: translateY(-4px);
          box-shadow: 0 16px 32px rgba(102, 126, 234, 0.15);
          border-color: rgba(102, 126, 234, 0.3);
          
          &::before {
            left: 100%;
          }
        }
        
        .chart-header {
  text-align: center;
          margin-bottom: 24px;
          
          h4 {
            font-size: 20px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 6px 0;
            letter-spacing: -0.3px;
          }
          
          p {
            color: #666;
            font-size: 14px;
            margin: 0;
            font-weight: 500;
          }
}

.chart-container {
          height: 320px;
          border-radius: 16px;
          background: linear-gradient(135deg, rgba(248, 250, 252, 0.8) 0%, rgba(241, 245, 249, 0.8) 100%);
          padding: 16px;
          border: 1px solid rgba(102, 126, 234, 0.1);
          box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
        }
      }
    }
  }
}

@keyframes shimmer {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 200% 0%;
  }
}

.analysis-section {
  padding: 0 32px 32px;
  
  .analysis-card {
    max-width: 1800px;
    margin: 0 auto;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15), 0 8px 32px rgba(102, 126, 234, 0.1);
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%);
      background-size: 200% 100%;
      animation: shimmer 3s linear infinite;
    }
    
    .analysis-header {
      margin-bottom: 32px;
      
      .analysis-title {
        h3 {
          font-size: 24px;
          font-weight: 700;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin: 0 0 8px 0;
          letter-spacing: -0.5px;
        }
        
        p {
          color: #666;
          font-size: 15px;
          margin: 0;
          font-weight: 500;
        }
      }
    }
    
    .analysis-tabs {
      :deep(.el-tabs__header) {
        margin-bottom: 32px;
        background: rgba(248, 250, 252, 0.5);
        border-radius: 16px;
        padding: 8px;
      }
      
      :deep(.el-tabs__nav-wrap) {
        &::after {
          display: none;
        }
      }
      
      :deep(.el-tabs__item) {
        padding: 14px 24px;
        font-weight: 600;
        color: #666;
        border-radius: 12px;
        transition: all 0.3s ease;
        margin: 0 4px;
        
        &:hover {
          color: #667eea;
          background: rgba(102, 126, 234, 0.1);
        }
        
        &.is-active {
          color: white;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
      }
      
      :deep(.el-tabs__active-bar) {
        display: none;
      }
      
      .tab-label {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      
      .tab-content {
.filter-section {
          margin-bottom: 28px;
          
          .filter-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
            border-radius: 18px;
            padding: 28px;
            border: 1px solid rgba(226, 232, 240, 0.5);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            
            &:hover {
              box-shadow: 0 12px 30px rgba(102, 126, 234, 0.1);
              border-color: rgba(102, 126, 234, 0.3);
            }
            
            .filter-header {
              margin-bottom: 20px;
              display: flex;
              align-items: center;
              gap: 12px;
              
              &::before {
                content: '';
                width: 4px;
                height: 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 2px;
              }
              
              h4 {
                font-size: 18px;
                font-weight: 700;
                color: #1a1a1a;
                margin: 0;
                letter-spacing: -0.3px;
              }
              
              p {
                color: #666;
                font-size: 14px;
                margin: 0 0 0 auto;
                font-weight: 500;
              }
            }
            
            .filter-form {
              :deep(.el-form--inline .el-form-item) {
                margin-right: 16px;
                margin-bottom: 0;
              }
              
              :deep(.el-input__wrapper) {
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
                transition: all 0.3s ease;
                
                &:hover {
                  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
                }
                
                &.is-focus {
                  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
                }
              }
              
              .search-select, .date-picker {
                min-width: 220px;
              }
              
              .search-btn, .reset-btn {
                padding: 11px 24px;
                border-radius: 12px;
  font-weight: 600;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                
                &:hover {
                  transform: translateY(-2px);
                }
              }
              
              .search-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                color: white;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                
                &:hover {
                  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                }
                
                &:active {
                  transform: translateY(0);
                }
              }
              
              .reset-btn {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                color: #6c757d;
                
                &:hover {
                  background: #e9ecef;
                  border-color: #dee2e6;
                }
              }
            }
          }
        }
        
        .results-section {
          .results-summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 28px;
            
            .summary-card {
              background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
              border-radius: 18px;
              padding: 24px;
              display: flex;
              align-items: center;
              gap: 16px;
              border: 1px solid rgba(226, 232, 240, 0.5);
              transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
              position: relative;
              overflow: hidden;
              
              &::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle at top right, rgba(102, 126, 234, 0.05) 0%, transparent 60%);
                opacity: 0;
                transition: opacity 0.4s ease;
              }
              
              &:hover {
                transform: translateY(-4px) scale(1.02);
                box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15);
                border-color: rgba(102, 126, 234, 0.3);
                
                &::before {
                  opacity: 1;
                }
                
                .summary-icon {
                  transform: scale(1.1);
                }
              }
              
              .summary-icon {
                width: 56px;
                height: 56px;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                flex-shrink: 0;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                
                &.total {
                  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                  color: white;
                }
                
                &.completed {
                  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                  color: white;
                }
                
                &.average {
                  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                  color: white;
                }
                
                &.active {
                  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
                  color: white;
                }
                
                &.admin {
                  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                  color: white;
                }
                
                &.regular {
                  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
                  color: white;
                }
                
                &.published {
                  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
                  color: white;
                }
                
                &.max {
                  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                  color: white;
                }
                
                &.wrong {
                  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                  color: white;
                }
              }
              
              .summary-content {
                flex: 1;
                
                .summary-value {
                  font-size: 32px;
                  font-weight: 800;
                  color: #1a1a1a;
                  margin-bottom: 6px;
                  letter-spacing: -1.5px;
                  background: linear-gradient(135deg, #1a1a1a 0%, #4a4a4a 100%);
                  -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent;
                  background-clip: text;
}

.summary-label {
                  font-size: 13px;
                  color: #666;
                  font-weight: 600;
                  text-transform: uppercase;
                  letter-spacing: 0.8px;
                }
              }
            }
          }
          
          .score-distribution-section, .personal-overview, .personal-subjects {
            margin-top: 28px;
            
            .section-header {
              margin-bottom: 20px;
              padding-left: 16px;
              border-left: 4px solid transparent;
              border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) 1;
              
              h4 {
                font-size: 20px;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0 0 6px 0;
                letter-spacing: -0.3px;
              }
              
              p {
                color: #666;
  font-size: 14px;
                margin: 0;
                font-weight: 500;
              }
            }
            
            .distribution-table, .subjects-table {
              background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
              border-radius: 16px;
              padding: 20px;
              border: 1px solid rgba(226, 232, 240, 0.5);
              box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
              
              :deep(.el-table) {
                background: transparent;
                
                .el-table__header th {
                  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                  color: #495057;
                  font-weight: 700;
                  border-bottom: 2px solid rgba(102, 126, 234, 0.1);
                  text-transform: uppercase;
                  letter-spacing: 0.5px;
                  font-size: 13px;
                }
                
                .el-table__body tr {
                  transition: all 0.3s ease;
                  
                  &:hover {
                    background: rgba(102, 126, 234, 0.08);
                    transform: scale(1.01);
                  }
                }
                
                .el-table__body td {
                  font-weight: 500;
                }
              }
              
              .progress-bar {
                width: 100%;
                height: 10px;
                background: rgba(0, 0, 0, 0.08);
                border-radius: 5px;
                overflow: hidden;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
                
                .progress-fill {
                  height: 100%;
                  border-radius: 5px;
                  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                  position: relative;
                  overflow: hidden;
                  
                  &::after {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
                    animation: progressShimmer 2s infinite;
                  }
                }
              }
            }
          }
          
          .question-stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
            
            .stats-card {
              background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
              border-radius: 18px;
              padding: 28px;
              border: 1px solid rgba(226, 232, 240, 0.5);
              transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
              position: relative;
              overflow: hidden;
              
              &::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle at bottom left, rgba(102, 126, 234, 0.05) 0%, transparent 60%);
                opacity: 0;
                transition: opacity 0.4s ease;
              }
              
              &:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15);
                border-color: rgba(102, 126, 234, 0.3);
                
                &::before {
                  opacity: 1;
                }
              }
              
              .stats-header {
                margin-bottom: 20px;
                padding-bottom: 16px;
                border-bottom: 2px solid rgba(102, 126, 234, 0.1);
                
                h4 {
                  font-size: 18px;
                  font-weight: 700;
                  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent;
                  background-clip: text;
                  margin: 0 0 4px 0;
                  letter-spacing: -0.3px;
                }
                
                p {
                  color: #666;
                  font-size: 13px;
                  margin: 0;
                  font-weight: 500;
                }
              }
            }
          }
        }
      }
    }
  }
}

@keyframes progressShimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .modern-header .header-content,
  .dashboard-section,
  .analysis-section {
    padding-left: 20px;
    padding-right: 20px;
  }
  
  .charts-grid,
  .question-stats-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .modern-header .header-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .stats-grid,
  .results-summary {
    grid-template-columns: 1fr;
  }
  
  .filter-form {
    :deep(.el-form--inline) {
      display: flex;
      flex-direction: column;
      
      .el-form-item {
        width: 100%;
        margin-right: 0;
        margin-bottom: 16px;
      }
      
      .search-select, .date-picker {
        width: 100%;
      }
      
      .search-btn, .reset-btn {
        width: 100%;
      }
    }
  }
  
  .dashboard-card, .analysis-card {
    padding: 20px;
  }
}
</style>
