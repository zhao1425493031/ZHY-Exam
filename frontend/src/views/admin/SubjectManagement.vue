<template>
  <div class="modern-subject-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Collection /></el-icon>
            </div>
            <div class="title-text">
              <h1>科目管理</h1>
              <p>管理系统科目和课程设置</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="showCreateDialog = true" class="add-btn">
            <el-icon><Plus /></el-icon>
            <span>添加科目</span>
          </el-button>
          <el-button @click="$router.push('/admin')" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回控制台</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-section">
      <div class="search-card">
        <div class="search-header">
          <h3>搜索和筛选</h3>
          <p>快速查找科目信息</p>
        </div>
        <div class="search-form">
        <el-form :model="searchForm" inline>
            <el-form-item>
              <el-input
                v-model="searchForm.keyword"
                placeholder="请输入科目名称"
                prefix-icon="Search"
                class="search-input"
              />
          </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.status" placeholder="选择状态" class="filter-select">
                <el-option label="全部状态" value="" />
              <el-option label="启用" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>
          </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.category" placeholder="选择分类" class="filter-select">
                <el-option label="全部分类" value="" />
                <el-option
                  v-for="category in categories"
                  :key="category"
                  :label="category"
                  :value="category"
                />
            </el-select>
          </el-form-item>
          <el-form-item>
              <el-button type="primary" @click="handleSearch" class="search-btn">
                <el-icon><Search /></el-icon>
                <span>搜索</span>
              </el-button>
              <el-button @click="handleReset" class="reset-btn">
                <el-icon><Refresh /></el-icon>
                <span>重置</span>
              </el-button>
          </el-form-item>
        </el-form>
      </div>
      </div>
    </div>

    <!-- 科目列表 -->
    <div class="table-section">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>科目列表</h3>
            <p>共 {{ pagination.total }} 个科目</p>
          </div>
          <div class="table-actions">
            <el-button @click="handleExport" class="export-btn" :loading="exportLoading">
              <el-icon><Download /></el-icon>
              <span>导出</span>
            </el-button>
          </div>
        </div>
        
        <div class="table-container">

          <el-table 
            :data="subjects" 
            stripe 
            class="modern-table"
            :loading="loading"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="科目名称" min-width="150" show-overflow-tooltip>
              <template #default="{ row }">
                <div class="user-info">
                  <div class="user-avatar">{{ row.name.charAt(0).toUpperCase() }}</div>
                  <div class="user-details">
                    <div class="username">{{ row.name }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="code" label="科目代码" width="120" />
            <el-table-column prop="category" label="分类" width="120" />
            <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusTagType(row.status)" size="small" class="status-tag">
                  {{ getStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="160">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" type="primary" @click="editSubject(row)" class="action-btn edit-btn">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button size="small" type="warning" @click="toggleSubjectStatus(row)" class="action-btn status-btn">
                    <el-icon><Switch /></el-icon>
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteSubject(row)" class="action-btn delete-btn">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            :current-page="pagination.page"
            :page-size="pagination.size"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
            class="modern-pagination"
          />
        </div>
      </div>
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
import { 
  Plus, Search, Refresh, Download, Collection, 
  Edit, Switch, Delete, ArrowLeft
} from '@element-plus/icons-vue'
import SubjectForm from '@/components/subject/SubjectForm.vue'
import SubjectView from '@/components/subject/SubjectView.vue'
import { subjectsApi } from '@/api/subjects'
import { formatDate } from '@/utils/format'

export default {
  name: 'SubjectManagement',
  components: {
    SubjectForm,
    SubjectView,
    Plus,
    Search,
    Refresh,
    Download,
    Collection,
    Edit,
    Switch,
    Delete,
    ArrowLeft
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const exportLoading = ref(false)
    const subjects = ref([])
    const selectedSubjects = ref([])
    const categories = ref([])
    const stats = reactive({
      total: 0,
      active: 0,
      inactive: 0
    })
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      status: '',
      is_free: '',
      category: ''
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
        
        const response = await subjectsApi.getSubjects(params)
        subjects.value = response.data.items || response.data
        pagination.total = response.data.total || subjects.value.length
      } catch (error) {
        ElMessage.error('加载科目列表失败')
        console.error('Load subjects error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadStats = async () => {
      try {
        const response = await subjectsApi.getSubjectStats()
        Object.assign(stats, response.data)
      } catch (error) {
        console.error('Load stats error:', error)
      }
    }
    
    const loadCategories = async () => {
      try {
        const response = await subjectsApi.getCategories()
        categories.value = response.data || []
      } catch (error) {
        console.error('Load categories error:', error)
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
          await subjectsApi.updateSubject(editingSubject.value.id, subjectData)
          ElMessage.success('科目更新成功')
        } else {
          await subjectsApi.createSubject(subjectData)
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
        await subjectsApi.updateSubjectStatus(subject.id, { status: newStatus })
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
        
        await subjectsApi.createSubject(duplicateData)
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
        
        await subjectsApi.deleteSubject(subject.id)
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
    
    const handleExport = async () => {
      try {
        exportLoading.value = true
        
        const params = {
          status: searchForm.status,
          is_free: searchForm.is_free
        }
        
        // 过滤空值
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await subjectsApi.exportSubjects(params)
        
        // 创建下载链接
        const blob = new Blob([response], { 
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `科目数据_${new Date().toISOString().slice(0, 10)}.xlsx`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        ElMessage.success('导出成功')
      } catch (error) {
        ElMessage.error('导出失败')
        console.error('Export subjects error:', error)
      } finally {
        exportLoading.value = false
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
      loadStats()
      loadCategories()
    })
    
    return {
      loading,
      exportLoading,
      subjects,
      selectedSubjects,
      categories,
      stats,
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
      toggleSubjectStatus,
      deleteSubject,
      handleSubmit,
      handleAction,
      batchUpdateStatus,
      batchDelete,
      handleExport,
      getStatusLabel,
      getStatusTagType,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-subject-management {
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
        gap: 20px;
        
        .title-icon {
          width: 64px;
          height: 64px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.3);
          
          .el-icon {
            font-size: 32px;
            color: white;
          }
        }
        
        .title-text {
          h1 {
            font-size: 32px;
            font-weight: 700;
            color: white;
            margin: 0 0 8px 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          }
          
          p {
            color: rgba(255, 255, 255, 0.8);
            font-size: 16px;
            margin: 0;
            font-weight: 500;
          }
        }
      }
    }
    
    .header-right {
      display: flex;
      gap: 12px;
      
      .add-btn, .back-btn {
        padding: 12px 20px;
        font-weight: 600;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        
        &.el-button--primary {
          background: rgba(255, 255, 255, 0.2);
          border-color: rgba(255, 255, 255, 0.3);
          color: white;
          
          &:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
          }
        }
        
        &:not(.el-button--primary) {
          background: rgba(255, 255, 255, 0.1);
          border-color: rgba(255, 255, 255, 0.2);
          color: white;
          
          &:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
          }
        }
      }
    }
  }
}

.search-section {
  padding: 32px;
  
  .search-card {
    max-width: 1800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    
    .search-header {
      margin-bottom: 24px;
      
      h3 {
        font-size: 20px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0 0 8px 0;
      }
      
      p {
        color: #666;
        font-size: 14px;
        margin: 0;
      }
    }
    
    .search-form {
      .el-form {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        align-items: end;
        
        .el-form-item {
          margin-bottom: 0;
          
          .search-input {
            width: 240px;
            
            :deep(.el-input__wrapper) {
              border-radius: 12px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
          }
          
          .filter-select {
            width: 160px;
            
            :deep(.el-select__wrapper) {
              border-radius: 12px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
          }
          
          .search-btn, .reset-btn {
            padding: 10px 20px;
            border-radius: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            
            &.el-button--primary {
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              border: none;
              
              &:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
              }
            }
            
            &:not(.el-button--primary) {
              background: #f8f9fa;
              border-color: #e9ecef;
              color: #6c757d;
              
              &:hover {
                background: #e9ecef;
                transform: translateY(-2px);
              }
            }
          }
        }
      }
    }
  }
}

.table-section {
  padding: 0 32px 32px;
  
  .table-card {
    max-width: 1800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    
    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      
      .table-title {
        h3 {
          font-size: 20px;
          font-weight: 700;
          color: #1a1a1a;
          margin: 0 0 4px 0;
        }
        
        p {
          color: #666;
          font-size: 14px;
          margin: 0;
        }
      }
      
      .export-btn {
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        background: #f8f9fa;
        border-color: #e9ecef;
        color: #6c757d;
        
        &:hover {
          background: #e9ecef;
          transform: translateY(-2px);
        }
      }
    }
    
    .table-container {
      .modern-table {
        :deep(.el-table__header) {
          th {
            background: #f8f9fa;
            color: #495057;
            font-weight: 600;
            border-bottom: 2px solid #e9ecef;
          }
        }
        
        :deep(.el-table__body) {
          tr {
            &:hover {
              background: rgba(102, 126, 234, 0.05);
            }
          }
        }
        
        .user-info {
          display: flex;
          align-items: center;
          gap: 12px;
          
          .user-avatar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
          }
          
          .username {
            font-weight: 600;
            color: #1a1a1a;
          }
        }
        
        .status-tag {
          border-radius: 8px;
          font-weight: 600;
          padding: 4px 12px;
        }
        
        .action-buttons {
          display: flex;
          gap: 8px;
          
          .el-button {
            border-radius: 8px;
            padding: 6px 12px;
            
            &.edit-btn {
              background: #e3f2fd;
              border-color: #bbdefb;
              color: #1976d2;
              
              &:hover {
                background: #bbdefb;
                transform: translateY(-1px);
              }
            }
            
            &.status-btn {
              &.el-button--warning {
                background: #fff3e0;
                border-color: #ffcc02;
                color: #f57c00;
                
                &:hover {
                  background: #ffcc02;
                  transform: translateY(-1px);
                }
              }
              
              &.el-button--success {
                background: #e8f5e8;
                border-color: #4caf50;
                color: #2e7d32;
                
                &:hover {
                  background: #4caf50;
                  transform: translateY(-1px);
                }
              }
            }
            
            &.delete-btn {
              background: #ffebee;
              border-color: #ffcdd2;
              color: #d32f2f;
              
              &:hover {
                background: #ffcdd2;
                transform: translateY(-1px);
              }
            }
          }
        }
      }
    }
    
    .pagination-wrapper {
      margin-top: 24px;
      display: flex;
      justify-content: center;
      
      .modern-pagination {
        :deep(.el-pagination) {
          .el-pager li {
            border-radius: 8px;
            margin: 0 4px;
            
            &.is-active {
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              color: white;
            }
          }
          
          .btn-prev, .btn-next {
            border-radius: 8px;
            margin: 0 4px;
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .modern-header .header-content {
    flex-direction: column;
    gap: 24px;
    text-align: center;
    padding: 0 16px;
    
    .header-right {
      width: 100%;
      justify-content: center;
    }
  }
  
  .search-section {
    padding: 16px;
    
    .search-card {
      padding: 20px;
      
      .search-form .el-form {
        flex-direction: column;
        align-items: stretch;
        
        .el-form-item {
          width: 100%;
          
          .search-input, .filter-select {
            width: 100%;
          }
        }
      }
    }
  }
  
  .table-section {
    padding: 0 16px 16px;
    
    .table-card {
      padding: 20px;
      
      .table-header {
        flex-direction: column;
        gap: 16px;
        align-items: stretch;
      }
    }
  }
}
</style>
