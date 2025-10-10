<template>
  <div class="exam-statistics">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>考试统计</span>
          <el-button type="primary" @click="refreshData">刷新</el-button>
        </div>
      </template>
      
      <div class="statistics-content">
        <!-- 统计卡片 -->
        <el-row :gutter="20" class="stats-cards">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">{{ statistics.totalExams }}</div>
                <div class="stat-label">总考试数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">{{ statistics.totalParticipants }}</div>
                <div class="stat-label">参与人数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">{{ statistics.averageScore }}</div>
                <div class="stat-label">平均分</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">{{ statistics.passRate }}%</div>
                <div class="stat-label">通过率</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- 图表区域 -->
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>成绩分布</span>
              </template>
              <div ref="scoreChart" style="height: 300px;"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>考试趋势</span>
              </template>
              <div ref="trendChart" style="height: 300px;"></div>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- 详细统计表格 -->
        <el-card style="margin-top: 20px;">
          <template #header>
            <span>详细统计</span>
          </template>
          <el-table :data="statistics.details" stripe>
            <el-table-column prop="exam_name" label="考试名称" />
            <el-table-column prop="participant_count" label="参与人数" />
            <el-table-column prop="average_score" label="平均分" />
            <el-table-column prop="pass_rate" label="通过率">
              <template #default="{ row }">
                {{ row.pass_rate }}%
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import dayjs from 'dayjs'

export default {
  name: 'ExamStatistics',
  props: {
    examId: {
      type: [String, Number],
      default: null
    }
  },
  setup(props) {
    const scoreChart = ref()
    const trendChart = ref()
    
    const statistics = reactive({
      totalExams: 0,
      totalParticipants: 0,
      averageScore: 0,
      passRate: 0,
      details: []
    })
    
    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
    }
    
    const refreshData = async () => {
      // 模拟数据，实际应该调用API
      Object.assign(statistics, {
        totalExams: 25,
        totalParticipants: 150,
        averageScore: 78.5,
        passRate: 85.2,
        details: [
          {
            exam_name: 'Vue.js基础考试',
            participant_count: 30,
            average_score: 82.5,
            pass_rate: 90.0,
            created_at: '2024-01-15 10:00:00'
          },
          {
            exam_name: 'JavaScript进阶考试',
            participant_count: 25,
            average_score: 75.2,
            pass_rate: 80.0,
            created_at: '2024-01-20 14:30:00'
          }
        ]
      })
      
      await nextTick()
      initCharts()
    }
    
    const initCharts = () => {
      // 成绩分布图表
      if (scoreChart.value) {
        const scoreChartInstance = echarts.init(scoreChart.value)
        const scoreOption = {
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
                { value: 35, name: '90-100分' },
                { value: 45, name: '80-89分' },
                { value: 30, name: '70-79分' },
                { value: 20, name: '60-69分' },
                { value: 10, name: '60分以下' }
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
        scoreChartInstance.setOption(scoreOption)
      }
      
      // 考试趋势图表
      if (trendChart.value) {
        const trendChartInstance = echarts.init(trendChart.value)
        const trendOption = {
          title: {
            text: '考试趋势',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: ['1月', '2月', '3月', '4月', '5月', '6月']
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '考试次数',
              type: 'line',
              data: [5, 8, 12, 15, 18, 22],
              smooth: true
            },
            {
              name: '参与人数',
              type: 'line',
              data: [30, 45, 60, 75, 90, 110],
              smooth: true
            }
          ]
        }
        trendChartInstance.setOption(trendOption)
      }
    }
    
    onMounted(() => {
      refreshData()
    })
    
    return {
      scoreChart,
      trendChart,
      statistics,
      formatDate,
      refreshData
    }
  }
}
</script>

<style scoped>
.statistics-content {
  padding: 20px;
}

.stats-cards {
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
