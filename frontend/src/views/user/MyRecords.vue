<template>
  <div class="my-records">
    <div class="page-header">
      <h1>我的记录</h1>
      <div class="header-info">
        <el-tag type="info">共 {{ records.length }} 条记录</el-tag>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="statistics-overview">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon color="#409eff"><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ statistics.total_exams }}</div>
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
                <div class="stat-value">{{ statistics.average_score }}</div>
                <div class="stat-label">平均分数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon color="#e6a23c"><Medal /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ statistics.pass_rate }}%</div>
                <div class="stat-label">及格率</div>
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
                <div class="stat-value">{{ statistics.wrong_answers }}</div>
                <div class="stat-label">错题数量</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-card>
        <el-form :model="searchForm" inline>
          <el-form-item label="关键词">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索考试标题"
              clearable
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item label="科目">
            <el-select
              v-model="searchForm.subject_id"
              placeholder="选择科目"
              clearable
              style="width: 200px"
            >
              <el-option
                v-for="subject in subjects"
                :key="subject.id"
                :label="subject.name"
                :value="subject.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select
              v-model="searchForm.status"
              placeholder="选择状态"
              clearable
              style="width: 120px"
            >
              <el-option label="已完成" value="submitted" />
              <el-option label="进行中" value="in_progress" />
              <el-option label="已超时" value="timeout" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item label="时间范围">
            <el-date-picker
              v-model="searchForm.date_range"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="handleReset">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 记录列表 -->
    <div class="records-list">
      <el-card>
        <div class="list-header">
          <div class="list-title">
            <span>考试记录</span>
            <el-tag v-if="selectedRecords.length > 0" type="info">
              已选择 {{ selectedRecords.length }} 条记录
            </el-tag>
          </div>
          <div class="list-actions" v-if="selectedRecords.length > 0">
            <el-button size="small" @click="batchExport">
              <el-icon><Download /></el-icon>
              批量导出
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete">
              <el-icon><Delete /></el-icon>
              批量删除
            </el-button>
          </div>
        </div>

        <el-table
          :data="records"
          :loading="loading"
          @selection-change="handleSelectionChange"
          row-key="id"
          stripe
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="exam_title" label="考试标题" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="exam-title">
                <span>{{ row.exam_title }}</span>
                <div class="exam-meta">
                  <el-tag :type="getStatusTagType(row.status)" size="small">
                    {{ getStatusLabel(row.status) }}
                  </el-tag>
                  <span class="exam-subject">{{ getSubjectName(row.subject_id) }}</span>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="score" label="分数" width="100">
            <template #default="{ row }">
              <div v-if="row.score !== null" class="score-display">
                <span class="score-value" :class="getScoreClass(row.score)">
                  {{ row.score }}
                </span>
                <span class="score-total">/ {{ row.total_points }}</span>
              </div>
              <span v-else class="no-score">-</span>
            </template>
          </el-table-column>
          <el-table-column prop="start_time" label="开始时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.start_time) }}
            </template>
          </el-table-column>
          <el-table-column prop="submit_time" label="提交时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.submit_time) }}
            </template>
          </el-table-column>
          <el-table-column prop="duration" label="用时" width="100">
            <template #default="{ row }">
              {{ formatDuration(row.duration) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewRecord(row)">
                查看
              </el-button>
              <el-button size="small" type="primary" @click="viewResult(row)" v-if="row.status === 'submitted'">
                结果
              </el-button>
              <el-dropdown @command="(command) => handleAction(command, row)">
                <el-button size="small">
                  更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="retake" v-if="canRetake(row)">重新考试</el-dropdown-item>
                    <el-dropdown-item command="export">导出记录</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除记录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            :current-page="pagination.page"
            :page-size="pagination.size"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 成绩趋势图 -->
    <div class="score-trend">
      <el-card>
        <div class="trend-header">
          <h3>成绩趋势</h3>
          <div class="trend-controls">
            <el-select v-model="trendPeriod" @change="updateTrendChart" style="width: 120px">
              <el-option label="最近7天" value="7d" />
              <el-option label="最近30天" value="30d" />
              <el-option label="最近3个月" value="3m" />
              <el-option label="全部" value="all" />
            </el-select>
          </div>
        </div>
        <div class="trend-content">
          <div ref="trendChart" class="chart-container"></div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document, Trophy, Medal, Warning, Search, Refresh, Download, Delete, ArrowDown
} from '@element-plus/icons-vue'
import { examScoringApi } from '@/api/exam_scoring'
import { subjectsApi } from '@/api/subjects'
import { formatDate, formatDuration } from '@/utils/format'
import * as echarts from 'echarts'

export default {
  name: 'MyRecords',
  components: {
    Document,
    Trophy,
    Medal,
    Warning,
    Search,
    Refresh,
    Download,
    Delete,
    ArrowDown
  },
  setup() {
    const router = useRouter()
    
    // 响应式数据
    const loading = ref(false)
    const records = ref([])
    const subjects = ref([])
    const selectedRecords = ref([])
    const trendChart = ref(null)
    const trendPeriod = ref('30d')
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      subject_id: '',
      status: '',
      date_range: []
    })
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 统计数据
    const statistics = reactive({
      total_exams: 0,
      average_score: 0,
      pass_rate: 0,
      wrong_answers: 0
    })
    
    // 计算属性
    const getSubjectName = computed(() => {
      return (subjectId) => {
        const subject = subjects.value.find(s => s.id === subjectId)
        return subject ? subject.name : '未知科目'
      }
    })
    
    // 方法
    const loadRecords = async () => {
      try {
        loading.value = true
        const params = {
          page: pagination.page,
          size: pagination.size,
          ...searchForm
        }
        
        // 处理日期范围
        if (searchForm.date_range && searchForm.date_range.length === 2) {
          params.start_date = searchForm.date_range[0]
          params.end_date = searchForm.date_range[1]
          delete params.date_range
        }
        
        // 过滤空值
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await examScoringApi.getExamRecords(params)
        records.value = response.data.items
        pagination.total = response.data.total
        
        // 计算统计数据
        calculateStatistics()
        
        // 更新趋势图
        await nextTick()
        updateTrendChart()
      } catch (error) {
        ElMessage.error('加载考试记录失败')
        console.error('Load records error:', error)
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
      }
    }
    
    const calculateStatistics = () => {
      const submittedRecords = records.value.filter(r => r.status === 'submitted')
      
      statistics.total_exams = submittedRecords.length
      
      if (submittedRecords.length > 0) {
        const scores = submittedRecords.map(r => r.score).filter(s => s !== null)
        statistics.average_score = scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0
        
        const passCount = scores.filter(s => s >= 60).length
        statistics.pass_rate = scores.length > 0 ? Math.round(passCount / scores.length * 100) : 0
      }
      
      // TODO: 获取错题数量
      statistics.wrong_answers = 0
    }
    
    const updateTrendChart = async () => {
      if (!trendChart.value) return
      
      try {
        const chart = echarts.init(trendChart.value)
        
        // 根据时间范围过滤数据
        let filteredRecords = records.value.filter(r => r.status === 'submitted')
        
        if (trendPeriod.value !== 'all') {
          const now = new Date()
          let days = 30
          
          switch (trendPeriod.value) {
            case '7d':
              days = 7
              break
            case '30d':
              days = 30
              break
            case '3m':
              days = 90
              break
          }
          
          const cutoffDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000)
          filteredRecords = filteredRecords.filter(r => new Date(r.submit_time) >= cutoffDate)
        }
        
        // 按日期分组并计算平均分
        const dateGroups = {}
        filteredRecords.forEach(record => {
          const date = new Date(record.submit_time).toISOString().split('T')[0]
          if (!dateGroups[date]) {
            dateGroups[date] = []
          }
          dateGroups[date].push(record.score)
        })
        
        const dates = Object.keys(dateGroups).sort()
        const scores = dates.map(date => {
          const dayScores = dateGroups[date]
          return Math.round(dayScores.reduce((a, b) => a + b, 0) / dayScores.length)
        })
        
        const option = {
          title: {
            text: '成绩趋势',
            left: 'center',
            textStyle: {
              fontSize: 16,
              color: '#303133'
            }
          },
          tooltip: {
            trigger: 'axis',
            formatter: function(params) {
              const data = params[0]
              return `${data.name}<br/>平均分数: ${data.value}分`
            }
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
          yAxis: {
            type: 'value',
            name: '分数',
            min: 0,
            max: 100
          },
          series: [{
            name: '平均分数',
            type: 'line',
            data: scores,
            smooth: true,
            lineStyle: {
              color: '#409eff',
              width: 3
            },
            itemStyle: {
              color: '#409eff'
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                  offset: 0, color: 'rgba(64, 158, 255, 0.3)'
                }, {
                  offset: 1, color: 'rgba(64, 158, 255, 0.1)'
                }]
              }
            }
          }]
        }
        
        chart.setOption(option)
        
        // 响应式调整
        window.addEventListener('resize', () => {
          chart.resize()
        })
      } catch (error) {
        console.error('Update trend chart error:', error)
      }
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadRecords()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadRecords()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadRecords()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadRecords()
    }
    
    const handleSelectionChange = (selection) => {
      selectedRecords.value = selection
    }
    
    const viewRecord = (record) => {
      router.push(`/user/exam-taking/${record.exam_id}`)
    }
    
    const viewResult = (record) => {
      router.push(`/user/exam-result/${record.id}`)
    }
    
    const handleAction = async (command, record) => {
      switch (command) {
        case 'retake':
          await retakeExam(record)
          break
        case 'export':
          await exportRecord(record)
          break
        case 'delete':
          await deleteRecord(record)
          break
      }
    }
    
    const retakeExam = async (record) => {
      try {
        await ElMessageBox.confirm(
          `确定要重新参加"${record.exam_title}"考试吗？`,
          '确认重新考试',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        router.push(`/user/exam-taking/${record.exam_id}`)
      } catch (error) {
        // 用户取消
      }
    }
    
    const exportRecord = async (record) => {
      try {
        // TODO: 实现导出功能
        ElMessage.success('导出功能开发中')
      } catch (error) {
        ElMessage.error('导出失败')
        console.error('Export record error:', error)
      }
    }
    
    const deleteRecord = async (record) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除"${record.exam_title}"的考试记录吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // TODO: 实现删除功能
        ElMessage.success('删除功能开发中')
        loadRecords()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
          console.error('Delete record error:', error)
        }
      }
    }
    
    const batchExport = async () => {
      try {
        // TODO: 实现批量导出功能
        ElMessage.success('批量导出功能开发中')
      } catch (error) {
        ElMessage.error('批量导出失败')
        console.error('Batch export error:', error)
      }
    }
    
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedRecords.value.length} 条考试记录吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // TODO: 实现批量删除功能
        ElMessage.success('批量删除功能开发中')
        selectedRecords.value = []
        loadRecords()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    const canRetake = (record) => {
      // TODO: 检查是否可以重考
      return record.status === 'submitted'
    }
    
    // 工具方法
    const getStatusLabel = (status) => {
      const labels = {
        in_progress: '进行中',
        submitted: '已完成',
        timeout: '已超时',
        cancelled: '已取消'
      }
      return labels[status] || status
    }
    
    const getStatusTagType = (status) => {
      const types = {
        in_progress: 'primary',
        submitted: 'success',
        timeout: 'warning',
        cancelled: 'danger'
      }
      return types[status] || 'default'
    }
    
    const getScoreClass = (score) => {
      if (score >= 90) return 'score-excellent'
      if (score >= 80) return 'score-good'
      if (score >= 70) return 'score-medium'
      if (score >= 60) return 'score-pass'
      return 'score-fail'
    }
    
    // 生命周期
    onMounted(() => {
      loadSubjects()
      loadRecords()
    })
    
    return {
      loading,
      records,
      subjects,
      selectedRecords,
      trendChart,
      trendPeriod,
      searchForm,
      pagination,
      statistics,
      getSubjectName,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewRecord,
      viewResult,
      handleAction,
      batchExport,
      batchDelete,
      canRetake,
      getStatusLabel,
      getStatusTagType,
      getScoreClass,
      updateTrendChart,
      formatDate,
      formatDuration
    }
  }
}
</script>

<style scoped>
.my-records {
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

.statistics-overview {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
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

.search-section {
  margin-bottom: 20px;
}

.records-list {
  margin-bottom: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.list-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 500;
}

.list-actions {
  display: flex;
  gap: 10px;
}

.exam-title {
  line-height: 1.5;
}

.exam-meta {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.exam-subject {
  color: #909399;
  font-size: 12px;
}

.score-display {
  display: flex;
  align-items: baseline;
  gap: 5px;
}

.score-value {
  font-weight: 600;
  font-size: 16px;
}

.score-excellent {
  color: #67c23a;
}

.score-good {
  color: #409eff;
}

.score-medium {
  color: #e6a23c;
}

.score-pass {
  color: #909399;
}

.score-fail {
  color: #f56c6c;
}

.score-total {
  color: #909399;
  font-size: 12px;
}

.no-score {
  color: #c0c4cc;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.score-trend {
  margin-bottom: 20px;
}

.trend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.trend-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.trend-content {
  height: 300px;
}

.chart-container {
  width: 100%;
  height: 100%;
}

:deep(.el-table .el-table__row) {
  cursor: pointer;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f7fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .my-records {
    padding: 15px;
  }
  
  .statistics-overview .el-col {
    margin-bottom: 15px;
  }
  
  .list-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .trend-content {
    height: 250px;
  }
}
</style>
