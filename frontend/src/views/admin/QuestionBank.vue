<template>
  <div class="question-bank">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>题库管理</span>
          <el-button type="primary" @click="handleAdd">添加题目</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-area">
        <el-form :model="searchForm" inline>
          <el-form-item label="科目">
            <el-select v-model="searchForm.subject_id" placeholder="请选择科目">
              <el-option label="全部" value="" />
              <el-option
                v-for="subject in subjects"
                :key="subject.id"
                :label="subject.name"
                :value="subject.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="题型">
            <el-select v-model="searchForm.type" placeholder="请选择题型">
              <el-option label="全部" value="" />
              <el-option label="单选题" value="single" />
              <el-option label="多选题" value="multiple" />
              <el-option label="判断题" value="judge" />
              <el-option label="填空题" value="fill" />
              <el-option label="简答题" value="essay" />
            </el-select>
          </el-form-item>
          <el-form-item label="难度">
            <el-select v-model="searchForm.difficulty" placeholder="请选择难度">
              <el-option label="全部" value="" />
              <el-option label="简单" value="easy" />
              <el-option label="中等" value="medium" />
              <el-option label="困难" value="hard" />
            </el-select>
          </el-form-item>
          <el-form-item label="关键词">
            <el-input v-model="searchForm.keyword" placeholder="请输入关键词" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 题目表格 -->
      <el-table :data="questions" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="题目" min-width="200" />
        <el-table-column prop="type" label="题型" width="100">
          <template #default="{ row }">
            <el-tag :type="getTypeTagType(row.type)">
              {{ getTypeName(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="difficulty" label="难度" width="100">
          <template #default="{ row }">
            <el-tag :type="getDifficultyTagType(row.difficulty)">
              {{ getDifficultyName(row.difficulty) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="points" label="分值" width="80" />
        <el-table-column prop="subject_name" label="科目" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'published' ? 'success' : 'warning'">
              {{ row.status === 'published' ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="150">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="handleView(row)">查看</el-button>
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
        style="margin-top: 20px; text-align: right;"
      />
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

export default {
  name: 'QuestionBank',
  setup() {
    const questions = ref([])
    const subjects = ref([])
    
    const searchForm = reactive({
      subject_id: '',
      type: '',
      difficulty: '',
      keyword: ''
    })
    
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
    }
    
    const getTypeName = (type) => {
      const typeMap = {
        single: '单选题',
        multiple: '多选题',
        judge: '判断题',
        fill: '填空题',
        essay: '简答题'
      }
      return typeMap[type] || type
    }
    
    const getTypeTagType = (type) => {
      const typeMap = {
        single: 'primary',
        multiple: 'success',
        judge: 'warning',
        fill: 'info',
        essay: 'danger'
      }
      return typeMap[type] || 'primary'
    }
    
    const getDifficultyName = (difficulty) => {
      const difficultyMap = {
        easy: '简单',
        medium: '中等',
        hard: '困难'
      }
      return difficultyMap[difficulty] || difficulty
    }
    
    const getDifficultyTagType = (difficulty) => {
      const difficultyMap = {
        easy: 'success',
        medium: 'warning',
        hard: 'danger'
      }
      return difficultyMap[difficulty] || 'primary'
    }
    
    const loadQuestions = async () => {
      // 模拟数据，实际应该调用API
      questions.value = [
        {
          id: 1,
          title: 'Vue.js是什么？',
          type: 'single',
          difficulty: 'easy',
          points: 5,
          subject_name: 'Vue.js',
          status: 'published',
          created_at: '2024-01-01 10:00:00'
        },
        {
          id: 2,
          title: 'JavaScript的数据类型有哪些？',
          type: 'multiple',
          difficulty: 'medium',
          points: 10,
          subject_name: 'JavaScript',
          status: 'published',
          created_at: '2024-01-02 10:00:00'
        }
      ]
      pagination.total = questions.value.length
    }
    
    const loadSubjects = async () => {
      // 模拟数据，实际应该调用API
      subjects.value = [
        { id: 1, name: 'Vue.js' },
        { id: 2, name: 'JavaScript' },
        { id: 3, name: 'Python' }
      ]
    }
    
    const handleAdd = () => {
      // 跳转到添加题目页面
      ElMessage.info('跳转到添加题目页面')
    }
    
    const handleView = (row) => {
      // 查看题目详情
      ElMessage.info(`查看题目: ${row.title}`)
    }
    
    const handleEdit = (row) => {
      // 编辑题目
      ElMessage.info(`编辑题目: ${row.title}`)
    }
    
    const handleDelete = async (row) => {
      try {
        await ElMessageBox.confirm(
          '确定要删除这个题目吗？',
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        // 实际应该调用删除API
        ElMessage.success('删除成功')
        loadQuestions()
      } catch (error) {
        // 用户取消删除
      }
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadQuestions()
    }
    
    const handleReset = () => {
      Object.assign(searchForm, {
        subject_id: '',
        type: '',
        difficulty: '',
        keyword: ''
      })
      handleSearch()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadQuestions()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadQuestions()
    }
    
    onMounted(() => {
      loadSubjects()
      loadQuestions()
    })
    
    return {
      questions,
      subjects,
      searchForm,
      pagination,
      formatDate,
      getTypeName,
      getTypeTagType,
      getDifficultyName,
      getDifficultyTagType,
      handleAdd,
      handleView,
      handleEdit,
      handleDelete,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange
    }
  }
}
</script>

<style scoped>
.question-bank {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-area {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
}
</style>
