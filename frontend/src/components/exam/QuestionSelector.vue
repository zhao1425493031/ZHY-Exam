<template>
  <div class="question-selector">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>选择题目</span>
          <el-button type="primary" @click="handleConfirm">确认选择</el-button>
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
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 题目列表 -->
      <el-table
        :data="questions"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
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
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button size="small" @click="handlePreview(row)">预览</el-button>
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
import { ElMessage } from 'element-plus'

export default {
  name: 'QuestionSelector',
  props: {
    selectedQuestions: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:selected-questions'],
  setup(props, { emit }) {
    const questions = ref([])
    const subjects = ref([])
    const selectedQuestionsList = ref([...props.selectedQuestions])
    
    const searchForm = reactive({
      subject_id: '',
      type: '',
      difficulty: ''
    })
    
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
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
          points: 5
        },
        {
          id: 2,
          title: 'JavaScript的数据类型有哪些？',
          type: 'multiple',
          difficulty: 'medium',
          points: 10
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
    
    const handleSelectionChange = (selection) => {
      selectedQuestionsList.value = selection
    }
    
    const handlePreview = (row) => {
      ElMessage.info(`预览题目: ${row.title}`)
    }
    
    const handleConfirm = () => {
      emit('update:selected-questions', selectedQuestionsList.value)
      ElMessage.success(`已选择 ${selectedQuestionsList.value.length} 道题目`)
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadQuestions()
    }
    
    const handleReset = () => {
      Object.assign(searchForm, {
        subject_id: '',
        type: '',
        difficulty: ''
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
      selectedQuestionsList,
      searchForm,
      pagination,
      getTypeName,
      getTypeTagType,
      getDifficultyName,
      getDifficultyTagType,
      handleSelectionChange,
      handlePreview,
      handleConfirm,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange
    }
  }
}
</script>

<style scoped>
.question-selector {
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
