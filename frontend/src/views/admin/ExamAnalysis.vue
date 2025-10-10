<template>
  <div class="exam-analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>考试分析</span>
          <el-button type="primary" @click="refreshData">刷新数据</el-button>
        </div>
      </template>
      
      <!-- 考试选择 -->
      <div class="exam-selector">
        <el-form :model="searchForm" inline>
          <el-form-item label="选择考试">
            <el-select v-model="searchForm.exam_id" placeholder="请选择考试" @change="handleExamChange">
              <el-option
                v-for="exam in exams"
                :key="exam.id"
                :label="exam.title"
                :value="exam.id"
              />
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
            <el-button type="primary" @click="handleSearch">分析</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 统计概览 -->
      <div class="overview" v-if="analysisData">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">{{ analysisData.totalParticipants }}</div>
                <div class="stat-label">参与人数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">{{ analysisData.averageScore }}</div>
                <div class="stat-label">平均分</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">{{ analysisData.passRate }}%</div>
                <div class="stat-label">通过率</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">{{ analysisData.completionRate }}%</div>
                <div class="stat-label">完成率</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <!-- 图表分析 -->
      <div class="charts" v-if="analysisData">
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>成绩分布</span>
              </template>
              <div ref="scoreDistributionChart" style="height: 300px;"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>答题时间分布</span>
              </template>
              <div ref="timeDistributionChart" style="height: 300px;"></div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>题目正确率</span>
              </template>
              <div ref="questionAccuracyChart" style="height: 300px;"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>难度分析</span>
              </template>
              <div ref="difficultyChart" style="height: 300px;"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <!-- 详细数据表格 -->
      <el-card style="margin-top: 20px;" v-if="analysisData">
        <template #header>
          <span>详细数据</span>
        </template>
        <el-table :data="analysisData.details" stripe>
          <el-table-column prop="user_name" label="用户名" />
          <el-table-column prop="score" label="得分" />
          <el-table-column prop="duration" label="用时(分钟)" />
          <el-table-column prop="correct_count" label="正确题数" />
          <el-table-column prop="total_count" label="总题数" />
          <el-table-column prop="accuracy" label="正确率">
            <template #default="{ row }">
              {{ row.accuracy }}%
            </template>
          </el-table-column>
          <el-table-column prop="submit_time" label="提交时间">
            <template #default="{ row }">
              {{ formatDate(row.submit_time) }}
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'

export default {
  name: 'ExamAnalysis',
  setup() {
    const scoreDistributionChart = ref()
    const timeDistributionChart = ref()
    const questionAccuracyChart = ref()
    const difficultyChart = ref()
    
    const exams = ref([])
    const analysisData = ref(null)
    
    const searchForm = reactive({
      exam_id: '',
      date_range: []
    })
    
    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
    }
    
    const loadExams = async () => {
      // 模拟数据，实际应该调用API
      exams.value = [
        { id: 1, title: 'Vue.js基础考试' },
        { id: 2, title: 'JavaScript进阶考试' },
        { id: 3, title: 'Python基础考试' }
      ]
    }
    
    const refreshData = async () => {
      if (searchForm.exam_id) {
        await handleSearch()
      }
    }
    
    const handleExamChange = (examId) => {
      if (examId) {
        handleSearch()
      }
    }
    
    const handleSearch = async () => {
      if (!searchForm.exam_id) {
        ElMessage.warning('请先选择考试')
        return
      }
      
      // 模拟分析数据，实际应该调用API
      analysisData.value = {
        totalParticipants: 45,
        averageScore: 78.5,
        passRate: 85.2,
        completionRate: 92.1,
        details: [
          {
            user_name: 'user1',
            score: 85,
            duration: 95,
            correct_count: 17,
            total_count: 20,
            accuracy: 85.0,
            submit_time: '2024-01-15 10:30:00'
          },
          {
            user_name: 'user2',
            score: 92,
            duration: 88,
            correct_count: 18,
            total_count: 20,
            accuracy: 90.0,
            submit_time: '2024-01-15 11:15:00'
          }
        ]
      }
      
      await nextTick()
      initCharts()
    }
    
    const initCharts = () => {
      // 成绩分布图表
      if (scoreDistributionChart.value) {
        const chart = echarts.init(scoreDistributionChart.value)
        const option = {
          title: {
            text: '成绩分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          series: [
            {
              type: 'pie',
              radius: '50%',
              data: [
                { value: 15, name: '90-100分' },
                { value: 20, name: '80-89分' },
                { value: 8, name: '70-79分' },
                { value: 2, name: '60-69分' },
                { value: 0, name: '60分以下' }
              ]
            }
          ]
        }
        chart.setOption(option)
      }
      
      // 答题时间分布图表
      if (timeDistributionChart.value) {
        const chart = echarts.init(timeDistributionChart.value)
        const option = {
          title: {
            text: '答题时间分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: ['0-30分钟', '30-60分钟', '60-90分钟', '90-120分钟', '120分钟以上']
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              type: 'bar',
              data: [5, 15, 20, 4, 1]
            }
          ]
        }
        chart.setOption(option)
      }
      
      // 题目正确率图表
      if (questionAccuracyChart.value) {
        const chart = echarts.init(questionAccuracyChart.value)
        const option = {
          title: {
            text: '题目正确率',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: ['题目1', '题目2', '题目3', '题目4', '题目5']
          },
          yAxis: {
            type: 'value',
            max: 100
          },
          series: [
            {
              type: 'line',
              data: [95, 88, 92, 85, 90],
              smooth: true
            }
          ]
        }
        chart.setOption(option)
      }
      
      // 难度分析图表
      if (difficultyChart.value) {
        const chart = echarts.init(difficultyChart.value)
        const option = {
          title: {
            text: '难度分析',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          series: [
            {
              type: 'pie',
              radius: '50%',
              data: [
                { value: 8, name: '简单' },
                { value: 10, name: '中等' },
                { value: 2, name: '困难' }
              ]
            }
          ]
        }
        chart.setOption(option)
      }
    }
    
    onMounted(() => {
      loadExams()
    })
    
    return {
      scoreDistributionChart,
      timeDistributionChart,
      questionAccuracyChart,
      difficultyChart,
      exams,
      analysisData,
      searchForm,
      formatDate,
      refreshData,
      handleExamChange,
      handleSearch
    }
  }
}
</script>

<style scoped>
.exam-analysis {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.exam-selector {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.overview {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-item {
  padding: 20px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}
</style>
