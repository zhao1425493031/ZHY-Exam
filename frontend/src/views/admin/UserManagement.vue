<template>
  <div class="modern-user-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="title-text">
              <h1>用户管理</h1>
              <p>管理系统用户账户和权限</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="handleAdd" class="add-btn">
            <el-icon><Plus /></el-icon>
            <span>添加用户</span>
          </el-button>
          <el-button @click="goBack" class="back-btn">
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
          <p>快速查找用户信息</p>
        </div>
        <div class="search-form">
        <el-form :model="searchForm" inline>
            <el-form-item>
              <el-input
                v-model="searchForm.username"
                placeholder="请输入用户名"
                prefix-icon="Search"
                class="search-input"
              />
          </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.role" placeholder="选择角色" class="filter-select">
                <el-option label="全部角色" value="" />
              <el-option label="管理员" value="admin" />
              <el-option label="普通用户" value="user" />
            </el-select>
          </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.status" placeholder="选择状态" class="filter-select">
                <el-option label="全部状态" value="" />
              <el-option label="正常" value="active" />
              <el-option label="禁用" value="inactive" />
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

    <!-- 用户列表 -->
    <div class="table-section">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>用户列表</h3>
            <p>共 {{ pagination.total }} 个用户</p>
          </div>
          <div class="table-actions">
            <el-button @click="handleExport" class="export-btn">
              <el-icon><Download /></el-icon>
              <span>导出</span>
            </el-button>
          </div>
        </div>
        
        <div class="table-container">
          <el-table 
            :data="users" 
            stripe 
            class="modern-table"
            :loading="loading"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" min-width="120">
              <template #default="{ row }">
                <div class="user-info">
                  <el-avatar :size="32" class="user-avatar">
                    {{ row.username.charAt(0).toUpperCase() }}
                  </el-avatar>
                  <span class="username">{{ row.username }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="email" label="邮箱" min-width="180" />
            <el-table-column prop="real_name" label="真实姓名" min-width="120" />
            <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
                <el-tag 
                  :type="row.role === 'admin' ? 'danger' : 'primary'"
                  class="role-tag"
                >
              {{ row.role === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
                <el-tag 
                  :type="row.status === 'active' ? 'success' : 'danger'"
                  class="status-tag"
                >
              {{ row.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="{ row }">
                <span class="date-text">{{ formatDate(row.created_at) }}</span>
          </template>
        </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" @click="handleEdit(row)" class="edit-btn">
                    <el-icon><Edit /></el-icon>
                  </el-button>
            <el-button 
              size="small" 
              :type="row.status === 'active' ? 'warning' : 'success'"
              @click="handleToggleStatus(row)"
                    class="toggle-btn"
            >
                    <el-icon><Switch /></el-icon>
                  </el-button>
                  <el-button size="small" type="danger" @click="handleDelete(row)" class="delete-btn">
                    <el-icon><Delete /></el-icon>
            </el-button>
                </div>
          </template>
        </el-table-column>
      </el-table>
        </div>
      
      <!-- 分页 -->
        <div class="pagination-container">
      <el-pagination
            :current-page="pagination.page"
            :page-size="pagination.size"
            @update:current-page="pagination.page = $event"
            @update:page-size="pagination.size = $event"
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
    
    <!-- 用户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      class="modern-dialog"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="form.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!form.id">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option label="正常" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="handleDialogClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  User, Plus, ArrowLeft, Search, Refresh, Download, 
  Edit, Switch, Delete 
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import { usersApi } from '@/api/users'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'UserManagement',
  components: {
    User,
    Plus,
    ArrowLeft,
    Search,
    Refresh,
    Download,
    Edit,
    Switch,
    Delete
  },
  setup() {
    const router = useRouter()
    const formRef = ref()
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const loading = ref(false)
    
    const users = ref([])
    const searchForm = reactive({
      username: '',
      role: '',
      status: ''
    })
    
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    const form = reactive({
      id: null,
      username: '',
      email: '',
      real_name: '',
      password: '',
      role: 'user',
      status: 'active'
    })
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ]
    }
    
    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
    }
    
    // 返回控制台
    const goBack = () => {
      router.push('/admin')
    }

    // 导出功能
    const handleExport = async () => {
      try {
        const params = {
          keyword: searchForm.username,
          role: searchForm.role,
          status: searchForm.status
        }
        
        const response = await usersApi.exportUsers(params)
        
        // 创建下载链接
        const blob = new Blob([response], { 
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `用户数据_${dayjs().format('YYYY-MM-DD_HH-mm-ss')}.xlsx`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        ElMessage.success('用户数据导出成功')
      } catch (error) {
        console.error('导出用户数据失败:', error)
        ElMessage.error('导出用户数据失败')
      }
    }

    // 选择变化
    const handleSelectionChange = (selection) => {
      console.log('选中的用户:', selection)
    }
    
    const loadUsers = async () => {
      loading.value = true
      
      // 检查用户认证状态
      const authStore = useAuthStore()
      console.log('当前用户状态:', {
        isLoggedIn: authStore.isLoggedIn,
        userRole: authStore.userRole,
        token: authStore.token ? '存在' : '不存在',
        user: authStore.user
      })
      
      try {
        const params = {
          page: pagination.page,
          size: pagination.size,
          keyword: searchForm.username,
          role: searchForm.role,
          status: searchForm.status
        }
        
        const response = await usersApi.getUsers(params)
        
        if (response.code === 200) {
          users.value = response.data.items || []
          pagination.total = response.data.total || 0
        } else {
          ElMessage.error(response.message || '获取用户列表失败')
        }
      } catch (error) {
        console.error('获取用户列表失败:', error)
        
        // 检查是否是401错误
        if (error.response?.status === 401) {
          ElMessage.error('未授权访问，请确保您已以管理员身份登录')
          // 重定向到登录页面
          router.push('/login')
          return
        }
        
        ElMessage.error('获取用户列表失败')
        // 使用模拟数据作为后备
      users.value = [
        {
          id: 1,
          username: 'admin',
          email: 'admin@example.com',
          real_name: '管理员',
          role: 'admin',
          status: 'active',
          created_at: '2024-01-01 10:00:00'
        },
        {
          id: 2,
          username: 'user1',
          email: 'user1@example.com',
          real_name: '用户1',
          role: 'user',
          status: 'active',
          created_at: '2024-01-02 10:00:00'
        }
      ]
      pagination.total = users.value.length
      } finally {
        loading.value = false
      }
    }
    
    const handleAdd = () => {
      dialogTitle.value = '添加用户'
      Object.assign(form, {
        id: null,
        username: '',
        email: '',
        real_name: '',
        password: '',
        role: 'user',
        status: 'active'
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑用户'
      Object.assign(form, { ...row })
      dialogVisible.value = true
    }
    
    const handleDelete = async (row) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除用户 "${row.username}" 吗？此操作不可恢复！`,
          '确认删除',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const response = await usersApi.deleteUser(row.id)
        if (response.code === 200) {
          ElMessage.success('用户删除成功')
        loadUsers()
        } else {
          ElMessage.error(response.message || '删除用户失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除用户失败:', error)
          ElMessage.error('删除用户失败')
        }
      }
    }
    
    const handleToggleStatus = async (row) => {
      const newStatus = row.status === 'active' ? 'inactive' : 'active'
      const action = newStatus === 'active' ? '启用' : '禁用'
      
      try {
        await ElMessageBox.confirm(
          `确定要${action}用户 "${row.username}" 吗？`,
          `确认${action}`,
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const response = await usersApi.toggleUserStatus(row.id, newStatus)
        if (response.code === 200) {
        row.status = newStatus
          ElMessage.success(`用户 ${row.username} 已${action}`)
        } else {
          ElMessage.error(response.message || `${action}用户失败`)
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error(`${action}用户失败:`, error)
          ElMessage.error(`${action}用户失败`)
        }
      }
    }
    
    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        
        if (form.id) {
          // 更新用户
          const updateData = { ...form }
          delete updateData.id // 移除id字段
          delete updateData.password // 更新时不包含密码
          
          const response = await usersApi.updateUser(form.id, updateData)
          if (response.code === 200) {
            ElMessage.success('用户更新成功')
            dialogVisible.value = false
            loadUsers()
          } else {
            ElMessage.error(response.message || '更新用户失败')
          }
        } else {
          // 创建用户
          const createData = { ...form }
          delete createData.id // 移除id字段
          
          const response = await usersApi.createUser(createData)
          if (response.code === 200 || response.code === 201) {
            ElMessage.success('用户创建成功')
        dialogVisible.value = false
        loadUsers()
          } else {
            ElMessage.error(response.message || '创建用户失败')
          }
        }
      } catch (error) {
        console.error('提交用户表单失败:', error)
        ElMessage.error('操作失败')
      }
    }
    
    const handleDialogClose = () => {
      dialogVisible.value = false
      formRef.value?.resetFields()
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadUsers()
    }
    
    const handleReset = () => {
      Object.assign(searchForm, {
        username: '',
        role: '',
        status: ''
      })
      handleSearch()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadUsers()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadUsers()
    }
    
    onMounted(() => {
      loadUsers()
    })
    
    return {
      formRef,
      dialogVisible,
      dialogTitle,
      users,
      searchForm,
      pagination,
      form,
      rules,
      loading,
      formatDate,
      handleAdd,
      handleEdit,
      handleDelete,
      handleToggleStatus,
      handleSubmit,
      handleDialogClose,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      goBack,
      handleExport,
      handleSelectionChange
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-user-management {
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
    max-width: 1400px;
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
    max-width: 1400px;
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
    max-width: 1400px;
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
        
        .role-tag, .status-tag {
          border-radius: 8px;
          font-weight: 600;
          padding: 4px 12px;
        }
        
        .date-text {
          color: #6c757d;
          font-size: 13px;
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
            
            &.toggle-btn {
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
    
    .pagination-container {
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

.modern-dialog {
  :deep(.el-dialog) {
    border-radius: 20px;
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.2);
  }
  
  :deep(.el-dialog__header) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px 20px 0 0;
    padding: 20px 24px;
    
    .el-dialog__title {
      font-weight: 700;
      font-size: 18px;
    }
  }
  
  :deep(.el-dialog__body) {
    padding: 24px;
  }
  
  :deep(.el-dialog__footer) {
    padding: 16px 24px 24px;
    
    .el-button {
      border-radius: 12px;
      font-weight: 600;
      padding: 10px 24px;
      
      &.el-button--primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
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
