<template>
  <div class="favorites-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><Star /></el-icon>
            我的收藏
          </h1>
          <p class="page-description">管理您收藏的题目，随时复习巩固</p>
        </div>
        <div class="header-actions">
          <el-button @click="goBack" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            返回个人中心
          </el-button>
        </div>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="stats-overview">
      <div class="stat-card" v-for="(stat, index) in statistics" :key="index">
        <div class="stat-icon" :class="stat.type">
          <el-icon><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-content">
          <h3>{{ stat.value }}</h3>
          <p>{{ stat.label }}</p>
          <div class="stat-trend" :class="stat.trend">
            <el-icon><component :is="stat.trendIcon" /></el-icon>
            <span>{{ stat.change }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="content-card">
        <!-- 搜索和筛选 -->
        <div class="search-section">
          <div class="search-left">
            <el-input
              v-model="searchParams.keyword"
              placeholder="搜索题目内容..."
              class="search-input"
              clearable
              @keyup.enter="loadFavorites"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-select
              v-model="searchParams.subject_id"
              placeholder="选择科目"
              class="subject-select"
              clearable
              @change="loadFavorites"
            >
              <el-option
                v-for="subject in subjects"
                :key="subject.id"
                :label="subject.name"
                :value="subject.id"
              />
            </el-select>
            <el-select
              v-model="searchParams.difficulty"
              placeholder="难度"
              class="difficulty-select"
              clearable
              @change="loadFavorites"
            >
              <el-option label="简单" value="easy" />
              <el-option label="中等" value="medium" />
              <el-option label="困难" value="hard" />
            </el-select>
          </div>
          <div class="search-right">
            <el-button @click="loadFavorites" :loading="loading" class="search-btn">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="resetSearch" class="reset-btn">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </div>
        </div>

        <!-- 操作工具栏 -->
        <div class="toolbar">
          <div class="toolbar-left">
            <el-button
              type="danger"
              :disabled="selectedFavorites.length === 0"
              @click="batchRemove"
              class="batch-remove-btn"
            >
              <el-icon><Delete /></el-icon>
              批量取消收藏 ({{ selectedFavorites.length }})
            </el-button>
          </div>
          <div class="toolbar-right">
            <el-button @click="loadFavorites" :loading="loading" class="refresh-btn">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>

        <!-- 收藏列表 -->
        <div class="favorites-table">
          <el-table
            :data="favorites"
            :loading="loading"
            @selection-change="handleSelectionChange"
            row-key="id"
            class="modern-table"
            stripe
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="subject_name" label="科目" width="300" />
            <el-table-column prop="question_title" label="题目" min-width="400">
              <template #default="{ row }">
                <div class="question-content">
                  <div class="question-title" v-html="row.question_title"></div>
                  <div class="question-meta">
                    <el-tag :type="getDifficultyType(row.difficulty)" size="small">
                      {{ getDifficultyText(row.difficulty) }}
                    </el-tag>
                    <el-tag :type="getTypeType(row.type)" size="small">
                      {{ getTypeText(row.type) }}
                    </el-tag>
                    <span class="question-points">{{ row.points || 1 }}分</span>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="收藏时间" width="250">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="300" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button
                    size="small"
                    type="primary"
                    @click="viewQuestion(row)"
                    class="view-btn"
                  >
                    <el-icon><View /></el-icon>
                  </el-button>
                  <el-button
                    size="small"
                    type="warning"
                    @click="removeFavorite(row)"
                    class="remove-btn"
                  >
                    <el-icon><StarFilled /></el-icon>
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 分页 -->
        <div class="pagination-section">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.size"
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
            class="modern-pagination"
          />
        </div>
      </div>
    </div>

    <!-- 题目详情弹窗 -->
    <el-dialog
      v-model="showQuestionDialog"
      title="题目详情"
      width="800px"
      class="question-dialog"
    >
      <QuestionDetail
        v-if="selectedQuestion"
        :question="selectedQuestion"
        :show-answer="true"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Star, ArrowLeft, Search, Refresh, Delete, View, StarFilled, TrendCharts, Clock, Warning, Check
} from '@element-plus/icons-vue'
import QuestionDetail from '@/components/question/QuestionDetail.vue'
import { favoritesApi } from '@/api/favorites'
import { subjectsApi } from '@/api/subjects'
import { formatDate } from '@/utils/format'

export default {
  name: 'Favorites',
  components: {
    QuestionDetail,
    Star,
    ArrowLeft,
    Search,
    Refresh,
    Delete,
    View,
    StarFilled,
    TrendCharts,
    Clock,
    Warning,
    Check
  },
  setup() {
    const router = useRouter()
    
    // 响应式数据
    const loading = ref(false)
    const favorites = ref([])
    const subjects = ref([])
    const selectedFavorites = ref([])
    const showQuestionDialog = ref(false)
    const selectedQuestion = ref(null)

    // 搜索参数
    const searchParams = reactive({
      keyword: '',
      subject_id: '',
      difficulty: '',
      type: ''
    })

    // 分页参数
    const pagination = reactive({
      page: 1,
      size: 20,
      total: 0
    })

    // 统计数据
    const statistics = ref([
      {
        icon: 'Star',
        label: '收藏总数',
        value: '0',
        change: '0',
        trend: 'neutral',
        trendIcon: 'Minus',
        type: 'total'
      },
      {
        icon: 'TrendCharts',
        label: '本周新增',
        value: '0',
        change: '+0',
        trend: 'positive',
        trendIcon: 'ArrowUp',
        type: 'weekly'
      },
      {
        icon: 'Clock',
        label: '复习次数',
        value: '0',
        change: '0',
        trend: 'neutral',
        trendIcon: 'Minus',
        type: 'review'
      },
      {
        icon: 'Check',
        label: '掌握率',
        value: '0%',
        change: '0%',
        trend: 'positive',
        trendIcon: 'ArrowUp',
        type: 'mastery'
      }
    ])

    // 加载收藏列表
    const loadFavorites = async () => {
      try {
        loading.value = true
        
        const params = {
          page: pagination.page,
          size: pagination.size,
          ...searchParams
        }
        
        // 清理空参数
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await favoritesApi.getFavoriteQuestions(params)
        favorites.value = response.data.items || []
        pagination.total = response.data.total || 0
        
        // 加载统计数据
        await loadStatistics()
      } catch (error) {
        ElMessage.error('加载收藏列表失败')
        console.error('Load favorites error:', error)
      } finally {
        loading.value = false
      }
    }

    // 加载科目列表
    const loadSubjects = async () => {
      try {
        const response = await subjectsApi.getSubjects({ status: 'active' })
        subjects.value = Array.isArray(response.data) ? response.data : (response.data.items || [])
      } catch (error) {
        console.error('Load subjects error:', error)
      }
    }

    // 加载统计数据
    const loadStatistics = async () => {
      try {
        const response = await favoritesApi.getFavoriteStatistics()
        if (response.code === 200) {
          const stats = response.data
          statistics.value[0].value = stats.total_favorites?.toString() || '0'
          statistics.value[1].value = stats.weekly_new?.toString() || '0'
          statistics.value[2].value = stats.review_count?.toString() || '0'
          statistics.value[3].value = `${stats.mastery_rate || 0}%`
        }
      } catch (error) {
        console.error('Load statistics error:', error)
        // 使用本地数据计算
        const totalFavorites = favorites.value.length
        statistics.value[0].value = totalFavorites.toString()
        statistics.value[1].value = '0'
        statistics.value[2].value = '0'
        statistics.value[3].value = '0%'
      }
    }

    // 选择变化
    const handleSelectionChange = (selection) => {
      selectedFavorites.value = selection
    }

    // 分页变化
    const handlePageChange = (page) => {
      pagination.page = page
      loadFavorites()
    }

    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadFavorites()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.assign(searchParams, {
        keyword: '',
        subject_id: '',
        difficulty: '',
        type: ''
      })
      pagination.page = 1
      loadFavorites()
    }

    // 查看题目详情
    const viewQuestion = (favorite) => {
      selectedQuestion.value = favorite
      showQuestionDialog.value = true
    }

    // 取消收藏
    const removeFavorite = async (favorite) => {
      try {
        await ElMessageBox.confirm(
          `确定要取消收藏题目"${favorite.question_title}"吗？`,
          '确认取消收藏',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await favoritesApi.removeFavorite(favorite.question_id)
        ElMessage.success('取消收藏成功')
        await loadFavorites()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('取消收藏失败')
          console.error('Remove favorite error:', error)
        }
      }
    }

    // 批量取消收藏
    const batchRemove = async () => {
      if (selectedFavorites.value.length === 0) {
        ElMessage.warning('请选择要取消收藏的题目')
        return
      }

      try {
        await ElMessageBox.confirm(
          `确定要取消收藏选中的 ${selectedFavorites.value.length} 个题目吗？`,
          '批量取消收藏',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const questionIds = selectedFavorites.value.map(item => item.question_id)
        await favoritesApi.batchRemoveFavorites(questionIds)
        ElMessage.success('批量取消收藏成功')
        await loadFavorites()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量取消收藏失败')
          console.error('Batch remove error:', error)
        }
      }
    }

    // 获取难度类型
    const getDifficultyType = (difficulty) => {
      const typeMap = {
        'easy': 'success',
        'medium': 'warning',
        'hard': 'danger'
      }
      return typeMap[difficulty] || 'info'
    }

    // 获取难度文本
    const getDifficultyText = (difficulty) => {
      const textMap = {
        'easy': '简单',
        'medium': '中等',
        'hard': '困难'
      }
      return textMap[difficulty] || '未知'
    }

    // 获取题型类型
    const getTypeType = (type) => {
      const typeMap = {
        'single': 'primary',
        'multiple': 'success',
        'judge': 'warning',
        'fill': 'info',
        'essay': 'danger'
      }
      return typeMap[type] || 'info'
    }

    // 获取题型文本
    const getTypeText = (type) => {
      const textMap = {
        'single': '单选',
        'multiple': '多选',
        'judge': '判断',
        'fill': '填空',
        'essay': '简答'
      }
      return textMap[type] || '未知'
    }

    // 返回上一页
    const goBack = () => {
      router.go(-1)
    }

    // 组件挂载
    onMounted(async () => {
      await loadSubjects()
      await loadFavorites()
    })

    return {
      loading,
      favorites,
      subjects,
      selectedFavorites,
      showQuestionDialog,
      selectedQuestion,
      searchParams,
      pagination,
      statistics,
      loadFavorites,
      handleSelectionChange,
      handlePageChange,
      handleSizeChange,
      resetSearch,
      viewQuestion,
      removeFavorite,
      batchRemove,
      getDifficultyType,
      getDifficultyText,
      getTypeType,
      getTypeText,
      goBack,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.favorites-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 0;
}

// 页面头部
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 0;
  margin-bottom: 2rem;

  .header-content {
    max-width: 1800px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-left {
      .page-title {
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
        margin: 0 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
      }

      .page-description {
        font-size: 1rem;
        color: #fff;
        opacity: 0.9;
        margin: 0;
      }
    }

    .header-actions {
      .back-btn {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;

        &:hover {
          background: rgba(255, 255, 255, 0.3);
        }
      }
    }
  }
}

// 统计概览
.stats-overview {
  max-width: 1800px;
  margin: 0 auto 2rem auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;

  .stat-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    gap: 1.5rem;

    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: white;

      &.total {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }

      &.weekly {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      }

      &.review {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }

      &.mastery {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
      }
    }

    .stat-content {
      flex: 1;

      h3 {
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        color: #333;
      }

      p {
        font-size: 1rem;
        color: #666;
        margin: 0 0 0.5rem 0;
      }

      .stat-trend {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        font-size: 0.9rem;

        &.positive {
          color: #67c23a;
        }

        &.negative {
          color: #f56c6c;
        }

        &.neutral {
          color: #909399;
        }
      }
    }
  }
}

// 主要内容区域
.main-content {
  max-width: 1800px;
  margin: 0 auto;
  padding: 0 20px;

  .content-card {
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    overflow: hidden;
  }
}

// 搜索区域
.search-section {
  padding: 2rem;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;

  .search-left {
    display: flex;
    gap: 1rem;
    flex: 1;

    .search-input {
      flex: 1;
      max-width: 300px;
    }

    .subject-select,
    .difficulty-select {
      width: 150px;
    }
  }

  .search-right {
    display: flex;
    gap: 0.5rem;
  }
}

// 工具栏
.toolbar {
  padding: 1rem 2rem;
  background: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .toolbar-left,
  .toolbar-right {
    display: flex;
    gap: 0.5rem;
  }
}

// 表格样式
.favorites-table {
  .modern-table {
    :deep(.el-table__header) {
      background: #f8f9fa;
      
      th {
        background: #f8f9fa;
        border-bottom: 1px solid #e9ecef;
        font-weight: 600;
        color: #495057;
      }
    }

    :deep(.el-table__body) {
      tr {
        &:hover {
          background: #f8f9fa;
        }
      }
    }
  }

  .question-content {
    .question-title {
      font-size: 14px;
      line-height: 1.5;
      margin-bottom: 8px;
      color: #333;
    }

    .question-meta {
      display: flex;
      gap: 8px;
      align-items: center;

      .question-points {
        font-size: 12px;
        color: #666;
        background: #f0f0f0;
        padding: 2px 6px;
        border-radius: 4px;
      }
    }
  }

  .action-buttons {
    display: flex;
    gap: 0.5rem;

    .view-btn,
    .remove-btn {
      border-radius: 8px;
      padding: 8px;
      min-width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .view-btn {
      background: #e3f2fd;
      border-color: #bbdefb;
      color: #1976d2;

      &:hover {
        background: #bbdefb;
        transform: translateY(-1px);
      }
    }

    .remove-btn {
      background: #fff3e0;
      border-color: #ffcc02;
      color: #f57c00;

      &:hover {
        background: #ffcc02;
        transform: translateY(-1px);
      }
    }
  }
}

// 分页
.pagination-section {
  padding: 2rem;
  display: flex;
  justify-content: center;
  border-top: 1px solid #f0f0f0;

  .modern-pagination {
    :deep(.el-pagination) {
      .el-pager li {
        border-radius: 8px;
        margin: 0 2px;

        &.is-active {
          background: #667eea;
          color: white;
        }
      }

      .btn-prev,
      .btn-next {
        border-radius: 8px;
      }
    }
  }
}

// 题目详情弹窗
.question-dialog {
  :deep(.el-dialog) {
    border-radius: 16px;
    overflow: hidden;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .page-header .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .search-section {
    flex-direction: column;
    gap: 1rem;

    .search-left {
      flex-direction: column;
      width: 100%;

      .search-input,
      .subject-select,
      .difficulty-select {
        max-width: none;
        width: 100%;
      }
    }
  }

  .toolbar {
    flex-direction: column;
    gap: 1rem;
  }

  .stats-overview {
    grid-template-columns: 1fr;
  }
}
</style>
