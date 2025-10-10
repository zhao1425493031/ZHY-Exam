<template>
  <div class="subject-management">
    <div class="page-header">
      <h1>科目管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新增科目
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
              placeholder="搜索科目名称"
              clearable
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item label="状态">
            <el-select
              v-model="searchForm.status"
              placeholder="选择状态"
              clearable
              style="width: 120px"
            >
              <el-option label="启用" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>
          </el-form-item>
          <el-form-item label="收费类型">
            <el-select
              v-model="searchForm.is_free"
              placeholder="选择收费类型"
              clearable
              style="width: 120px"
            >
              <el-option label="免费" :value="true" />
              <el-option label="收费" :value="false" />
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

    <!-- 科目列表 -->
    <div class="table-section">
      <el-card>
        <div class="table-header">
          <div class="table-title">
            <span>科目列表</span>
            <el-tag v-if="selectedSubjects.length > 0" type="info">
              已选择 {{ selectedSubjects.length }} 个科目
            </el-tag>
          </div>
          <div class="table-actions" v-if="selectedSubjects.length > 0">
            <el-button size="small" @click="batchUpdateStatus('active')">
              批量启用
            </el-button>
            <el-button size="small" @click="batchUpdateStatus('inactive')">
              批量禁用
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete">
              批量删除
            </el-button>
          </div>
        </div>

        <el-table
          :data="subjects"
          :loading="loading"
          @selection-change="handleSelectionChange"
          row-key="id"
          stripe
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="科目名称" min-width="150" />
          <el-table-column prop="code" label="科目代码" width="120" />
          <el-table-column prop="category" label="分类" width="120" />
          <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
          <el-table-column label="收费设置" width="120">
            <template #default="{ row }">
              <el-tag :type="row.is_free ? 'success' : 'warning'" size="small">
                {{ row.is_free ? '免费' : '收费' }}
              </el-tag>
              <div v-if="!row.is_free" class="price-info">
                <span class="price">¥{{ row.price }}</span>
                <span v-if="row.original_price > row.price" class="original-price">
                  ¥{{ row.original_price }}
                </span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusTagType(row.status)" size="small">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewSubject(row)">
                查看
              </el-button>
              <el-button size="small" type="primary" @click="editSubject(row)">
                编辑
              </el-button>
              <el-dropdown @command="(command) => handleAction(command, row)">
                <el-button size="small">
                  更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="toggle-status">
                      {{ row.status === 'active' ? '禁用' : '启用' }}
                    </el-dropdown-item>
                    <el-dropdown-item command="duplicate">复制</el-dropdown-item>
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

    <!-- 创建/编辑科目对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingSubject ? '编辑科目' : '新增科目'"
      width="60%"
      :close-on-click-modal="false"
    >
      <SubjectForm
        v-if="showCreateDialog"
        :subject="editingSubject"
        @submit="handleSubmit"
        @cancel="showCreateDialog = false"
      />
    </el-dialog>

    <!-- 查看科目对话框 -->
    <el-dialog
      v-model="showViewDialog"
      title="科目详情"
      width="50%"
    >
      <SubjectView
        v-if="showViewDialog && viewingSubject"
        :subject="viewingSubject"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh, ArrowDown } from '@element-plus/icons-vue'
import SubjectForm from '@/components/subject/SubjectForm.vue'
import SubjectView from '@/components/subject/SubjectView.vue'
import { subjectApi } from '@/api/subjects'
import { formatDate } from '@/utils/format'

export default {
  name: 'SubjectManagement',
  components: {
    SubjectForm,
    SubjectView,
    Plus,
    Search,
    Refresh,
    ArrowDown
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const subjects = ref([])
    const selectedSubjects = ref([])
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      status: '',
      is_free: ''
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
    const editingSubject = ref(null)
    const viewingSubject = ref(null)
    
    // 方法
    const loadSubjects = async () => {
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
        
        const response = await subjectApi.getSubjects(params)
        subjects.value = response.data.items || response.data
        pagination.total = response.data.total || subjects.value.length
      } catch (error) {
        ElMessage.error('加载科目列表失败')
        console.error('Load subjects error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadSubjects()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadSubjects()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadSubjects()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadSubjects()
    }
    
    const handleSelectionChange = (selection) => {
      selectedSubjects.value = selection
    }
    
    const viewSubject = (subject) => {
      viewingSubject.value = subject
      showViewDialog.value = true
    }
    
    const editSubject = (subject) => {
      editingSubject.value = subject
      showCreateDialog.value = true
    }
    
    const handleSubmit = async (subjectData) => {
      try {
        if (editingSubject.value) {
          await subjectApi.updateSubject(editingSubject.value.id, subjectData)
          ElMessage.success('科目更新成功')
        } else {
          await subjectApi.createSubject(subjectData)
          ElMessage.success('科目创建成功')
        }
        
        showCreateDialog.value = false
        editingSubject.value = null
        loadSubjects()
      } catch (error) {
        ElMessage.error('保存科目失败')
        console.error('Submit subject error:', error)
      }
    }
    
    const handleAction = async (command, subject) => {
      switch (command) {
        case 'toggle-status':
          await toggleSubjectStatus(subject)
          break
        case 'duplicate':
          await duplicateSubject(subject)
          break
        case 'delete':
          await deleteSubject(subject)
          break
      }
    }
    
    const toggleSubjectStatus = async (subject) => {
      try {
        const newStatus = subject.status === 'active' ? 'inactive' : 'active'
        await subjectApi.updateSubjectStatus(subject.id, { status: newStatus })
        ElMessage.success(`科目已${newStatus === 'active' ? '启用' : '禁用'}`)
        loadSubjects()
      } catch (error) {
        ElMessage.error('更新科目状态失败')
        console.error('Toggle status error:', error)
      }
    }
    
    const duplicateSubject = async (subject) => {
      try {
        const duplicateData = { ...subject }
        delete duplicateData.id
        delete duplicateData.created_at
        delete duplicateData.updated_at
        duplicateData.name = duplicateData.name + ' (副本)'
        duplicateData.code = duplicateData.code + '_copy'
        
        await subjectApi.createSubject(duplicateData)
        ElMessage.success('科目复制成功')
        loadSubjects()
      } catch (error) {
        ElMessage.error('复制科目失败')
        console.error('Duplicate subject error:', error)
      }
    }
    
    const deleteSubject = async (subject) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除科目"${subject.name}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await subjectApi.deleteSubject(subject.id)
        ElMessage.success('科目删除成功')
        loadSubjects()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除科目失败')
          console.error('Delete subject error:', error)
        }
      }
    }
    
    const batchUpdateStatus = async (status) => {
      try {
        const ids = selectedSubjects.value.map(s => s.id)
        // TODO: 实现批量更新状态API
        ElMessage.success(`批量${status === 'active' ? '启用' : '禁用'}成功`)
        selectedSubjects.value = []
        loadSubjects()
      } catch (error) {
        ElMessage.error('批量更新状态失败')
        console.error('Batch update status error:', error)
      }
    }
    
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedSubjects.value.length} 个科目吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // TODO: 实现批量删除API
        ElMessage.success('批量删除成功')
        selectedSubjects.value = []
        loadSubjects()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    // 工具方法
    const getStatusLabel = (status) => {
      const labels = {
        active: '启用',
        inactive: '禁用'
      }
      return labels[status] || status
    }
    
    const getStatusTagType = (status) => {
      const types = {
        active: 'success',
        inactive: 'danger'
      }
      return types[status] || 'default'
    }
    
    // 生命周期
    onMounted(() => {
      loadSubjects()
    })
    
    return {
      loading,
      subjects,
      selectedSubjects,
      searchForm,
      pagination,
      showCreateDialog,
      showViewDialog,
      editingSubject,
      viewingSubject,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewSubject,
      editSubject,
      handleSubmit,
      handleAction,
      batchUpdateStatus,
      batchDelete,
      getStatusLabel,
      getStatusTagType,
      formatDate
    }
  }
}
</script>

<style scoped>
.subject-management {
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

.header-actions {
  display: flex;
  gap: 10px;
}

.search-section {
  margin-bottom: 20px;
}

.table-section {
  margin-bottom: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 500;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.price-info {
  margin-top: 4px;
  font-size: 12px;
}

.price {
  color: #e6a23c;
  font-weight: 500;
}

.original-price {
  color: #909399;
  text-decoration: line-through;
  margin-left: 5px;
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
