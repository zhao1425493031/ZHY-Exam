<template>
  <div class="exam-template">
    <div class="template-header">
      <div class="header-title">
        <h2>考试模板管理</h2>
        <p>创建和管理考试模板，提高组卷效率</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          创建模板
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-card>
        <el-form :model="searchForm" inline>
          <el-form-item label="关键词">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索模板名称"
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
          <el-form-item label="难度">
            <el-select
              v-model="searchForm.difficulty_level"
              placeholder="选择难度"
              clearable
              style="width: 120px"
            >
              <el-option label="初级" value="beginner" />
              <el-option label="中级" value="intermediate" />
              <el-option label="高级" value="advanced" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select
              v-model="searchForm.status"
              placeholder="选择状态"
              clearable
              style="width: 120px"
            >
              <el-option label="草稿" value="draft" />
              <el-option label="已发布" value="published" />
              <el-option label="已归档" value="archived" />
            </el-select>
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

    <!-- 模板列表 -->
    <div class="template-list">
      <el-card>
        <div class="list-header">
          <div class="list-title">
            <span>模板列表</span>
            <el-tag v-if="selectedTemplates.length > 0" type="info">
              已选择 {{ selectedTemplates.length }} 个模板
            </el-tag>
          </div>
          <div class="list-actions" v-if="selectedTemplates.length > 0">
            <el-button size="small" @click="batchUpdateStatus('published')">
              批量发布
            </el-button>
            <el-button size="small" @click="batchUpdateStatus('archived')">
              批量归档
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete">
              批量删除
            </el-button>
          </div>
        </div>

        <el-table
          :data="templates"
          :loading="loading"
          @selection-change="handleSelectionChange"
          row-key="id"
          stripe
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="模板名称" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="template-title">
                <span>{{ row.name }}</span>
                <div class="template-meta">
                  <el-tag :type="getStatusTagType(row.status)" size="small">
                    {{ getStatusLabel(row.status) }}
                  </el-tag>
                  <el-tag :type="getDifficultyTagType(row.difficulty_level)" size="small">
                    {{ getDifficultyLabel(row.difficulty_level) }}
                  </el-tag>
                  <span class="usage-count">使用{{ row.usage_count || 0 }}次</span>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="subject_id" label="科目" width="120">
            <template #default="{ row }">
              {{ getSubjectName(row.subject_id) }}
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
          <el-table-column prop="estimated_hours" label="预计时长" width="100">
            <template #default="{ row }">
              {{ row.estimated_hours || 0 }}小时
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewTemplate(row)">
                查看
              </el-button>
              <el-button size="small" type="primary" @click="editTemplate(row)">
                编辑
              </el-button>
              <el-dropdown @command="(command) => handleAction(command, row)">
                <el-button size="small">
                  更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="use">使用模板</el-dropdown-item>
                    <el-dropdown-item command="duplicate">复制</el-dropdown-item>
                    <el-dropdown-item command="toggle-status">
                      {{ row.status === 'published' ? '取消发布' : '发布' }}
                    </el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
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

    <!-- 创建/编辑模板对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingTemplate ? '编辑模板' : '创建模板'"
      width="80%"
      :close-on-click-modal="false"
    >
      <TemplateForm
        v-if="showCreateDialog"
        :template="editingTemplate"
        :subjects="subjects"
        @submit="handleSubmit"
        @cancel="showCreateDialog = false"
      />
    </el-dialog>

    <!-- 查看模板对话框 -->
    <el-dialog
      v-model="showViewDialog"
      title="模板详情"
      width="60%"
    >
      <TemplateView
        v-if="showViewDialog && viewingTemplate"
        :template="viewingTemplate"
        :subjects="subjects"
      />
    </el-dialog>

    <!-- 使用模板对话框 -->
    <el-dialog
      v-model="showUseDialog"
      title="使用模板创建考试"
      width="60%"
    >
      <TemplateUse
        v-if="showUseDialog && usingTemplate"
        :template="usingTemplate"
        :subjects="subjects"
        @submit="handleUseTemplate"
        @cancel="showUseDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh, ArrowDown } from '@element-plus/icons-vue'
import TemplateForm from '@/components/exam/TemplateForm.vue'
import TemplateView from '@/components/exam/TemplateView.vue'
import TemplateUse from '@/components/exam/TemplateUse.vue'
import { subjectApi } from '@/api/subjects'
import { formatDate } from '@/utils/format'

export default {
  name: 'ExamTemplate',
  components: {
    TemplateForm,
    TemplateView,
    TemplateUse,
    Plus,
    Search,
    Refresh,
    ArrowDown
  },
  props: {
    subjects: {
      type: Array,
      default: () => []
    }
  },
  emits: ['success', 'cancel'],
  setup(props, { emit }) {
    // 响应式数据
    const loading = ref(false)
    const templates = ref([])
    const selectedTemplates = ref([])
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      subject_id: '',
      difficulty_level: '',
      status: ''
    })
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 对话框状态
    const showCreateDialog = ref(false)
    const showViewDialog = ref(false)
    const showUseDialog = ref(false)
    const editingTemplate = ref(null)
    const viewingTemplate = ref(null)
    const usingTemplate = ref(null)
    
    // 计算属性
    const getSubjectName = computed(() => {
      return (subjectId) => {
        const subject = props.subjects.find(s => s.id === subjectId)
        return subject ? subject.name : '未知科目'
      }
    })
    
    // 方法
    const loadTemplates = async () => {
      try {
        loading.value = true
        const params = {
          page: pagination.page,
          size: pagination.size,
          ...searchForm
        }
        
        // 过滤空值
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        // TODO: 实现模板API
        // const response = await templateApi.getTemplates(params)
        // templates.value = response.data.items
        // pagination.total = response.data.total
        
        // 模拟数据
        templates.value = []
        pagination.total = 0
      } catch (error) {
        ElMessage.error('加载模板列表失败')
        console.error('Load templates error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadTemplates()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadTemplates()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadTemplates()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadTemplates()
    }
    
    const handleSelectionChange = (selection) => {
      selectedTemplates.value = selection
    }
    
    const viewTemplate = (template) => {
      viewingTemplate.value = template
      showViewDialog.value = true
    }
    
    const editTemplate = (template) => {
      editingTemplate.value = template
      showCreateDialog.value = true
    }
    
    const handleSubmit = async (templateData) => {
      try {
        if (editingTemplate.value) {
          // TODO: 实现更新模板API
          // await templateApi.updateTemplate(editingTemplate.value.id, templateData)
          ElMessage.success('模板更新成功')
        } else {
          // TODO: 实现创建模板API
          // await templateApi.createTemplate(templateData)
          ElMessage.success('模板创建成功')
        }
        
        showCreateDialog.value = false
        editingTemplate.value = null
        loadTemplates()
      } catch (error) {
        ElMessage.error('保存模板失败')
        console.error('Submit template error:', error)
      }
    }
    
    const handleAction = async (command, template) => {
      switch (command) {
        case 'use':
          await useTemplate(template)
          break
        case 'duplicate':
          await duplicateTemplate(template)
          break
        case 'toggle-status':
          await toggleTemplateStatus(template)
          break
        case 'delete':
          await deleteTemplate(template)
          break
      }
    }
    
    const useTemplate = (template) => {
      usingTemplate.value = template
      showUseDialog.value = true
    }
    
    const duplicateTemplate = async (template) => {
      try {
        const duplicateData = { ...template }
        delete duplicateData.id
        delete duplicateData.created_at
        delete duplicateData.updated_at
        duplicateData.name = duplicateData.name + ' (副本)'
        duplicateData.status = 'draft'
        
        // TODO: 实现创建模板API
        // await templateApi.createTemplate(duplicateData)
        ElMessage.success('模板复制成功')
        loadTemplates()
      } catch (error) {
        ElMessage.error('复制模板失败')
        console.error('Duplicate template error:', error)
      }
    }
    
    const toggleTemplateStatus = async (template) => {
      try {
        const newStatus = template.status === 'published' ? 'draft' : 'published'
        // TODO: 实现更新模板状态API
        // await templateApi.updateTemplateStatus(template.id, { status: newStatus })
        ElMessage.success(`模板已${newStatus === 'published' ? '发布' : '取消发布'}`)
        loadTemplates()
      } catch (error) {
        ElMessage.error('更新模板状态失败')
        console.error('Toggle status error:', error)
      }
    }
    
    const deleteTemplate = async (template) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除模板"${template.name}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // TODO: 实现删除模板API
        // await templateApi.deleteTemplate(template.id)
        ElMessage.success('模板删除成功')
        loadTemplates()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除模板失败')
          console.error('Delete template error:', error)
        }
      }
    }
    
    const batchUpdateStatus = async (status) => {
      try {
        const ids = selectedTemplates.value.map(t => t.id)
        // TODO: 实现批量更新状态API
        // await templateApi.batchUpdateStatus({ ids, status })
        ElMessage.success(`批量${status === 'published' ? '发布' : '归档'}成功`)
        selectedTemplates.value = []
        loadTemplates()
      } catch (error) {
        ElMessage.error('批量更新状态失败')
        console.error('Batch update status error:', error)
      }
    }
    
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedTemplates.value.length} 个模板吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const ids = selectedTemplates.value.map(t => t.id)
        // TODO: 实现批量删除API
        // await templateApi.batchDelete({ ids })
        ElMessage.success('批量删除成功')
        selectedTemplates.value = []
        loadTemplates()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    const handleUseTemplate = async (examData) => {
      try {
        // TODO: 实现使用模板创建考试API
        // await examApi.createExamFromTemplate(usingTemplate.value.id, examData)
        ElMessage.success('考试创建成功')
        showUseDialog.value = false
        usingTemplate.value = null
        emit('success')
      } catch (error) {
        ElMessage.error('创建考试失败')
        console.error('Use template error:', error)
      }
    }
    
    // 工具方法
    const getStatusLabel = (status) => {
      const labels = {
        draft: '草稿',
        published: '已发布',
        archived: '已归档'
      }
      return labels[status] || status
    }
    
    const getStatusTagType = (status) => {
      const types = {
        draft: 'info',
        published: 'success',
        archived: 'warning'
      }
      return types[status] || 'default'
    }
    
    const getDifficultyLabel = (difficulty) => {
      const labels = {
        beginner: '初级',
        intermediate: '中级',
        advanced: '高级'
      }
      return labels[difficulty] || difficulty
    }
    
    const getDifficultyTagType = (difficulty) => {
      const types = {
        beginner: 'success',
        intermediate: 'warning',
        advanced: 'danger'
      }
      return types[difficulty] || 'default'
    }
    
    // 生命周期
    onMounted(() => {
      loadTemplates()
    })
    
    return {
      loading,
      templates,
      selectedTemplates,
      searchForm,
      pagination,
      showCreateDialog,
      showViewDialog,
      showUseDialog,
      editingTemplate,
      viewingTemplate,
      usingTemplate,
      getSubjectName,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewTemplate,
      editTemplate,
      handleSubmit,
      handleAction,
      batchUpdateStatus,
      batchDelete,
      handleUseTemplate,
      getStatusLabel,
      getStatusTagType,
      getDifficultyLabel,
      getDifficultyTagType,
      formatDate
    }
  }
}
</script>

<style scoped>
.exam-template {
  padding: 20px;
}

.template-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-title h2 {
  margin: 0 0 5px 0;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.header-title p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.search-section {
  margin-bottom: 20px;
}

.template-list {
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

.template-title {
  line-height: 1.5;
}

.template-meta {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.usage-count {
  color: #909399;
  font-size: 12px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

:deep(.el-table .el-table__row) {
  cursor: pointer;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f7fa;
}
</style>
