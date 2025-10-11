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
      width="720px"
      :close-on-click-modal="false"
      class="modern-user-dialog"
      @close="handleDialogClose"
    >
      <div class="dialog-content">
        <!-- 用户头像区域 -->
        <div class="user-avatar-section">
          <div class="avatar-container">
            <el-avatar :size="80" class="user-avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <div class="avatar-text">
              <h3>{{ form.id ? '编辑用户信息' : '创建新用户' }}</h3>
              <p>{{ form.id ? '修改用户的基本信息和权限设置' : '填写用户的基本信息创建账户' }}</p>
            </div>
          </div>
        </div>

        <!-- 表单区域 -->
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="120px"
          class="user-form"
        >
          <div class="form-row">
            <el-form-item label="用户名" prop="username" class="form-item-half">
              <el-input 
                v-model="form.username" 
                placeholder="请输入用户名"
                prefix-icon="User"
                clearable
                :disabled="!!form.id"
              />
            </el-form-item>
            
            <el-form-item label="邮箱" prop="email" class="form-item-half">
              <el-input 
                v-model="form.email" 
                placeholder="请输入邮箱地址"
                prefix-icon="Message"
                clearable
              />
            </el-form-item>
          </div>
          
          <div class="form-row">
            <el-form-item label="真实姓名" prop="real_name" class="form-item-half">
              <el-input 
                v-model="form.real_name" 
                placeholder="请输入真实姓名"
                prefix-icon="UserFilled"
                clearable
              />
            </el-form-item>
            
            <el-form-item label="手机号" prop="phone" class="form-item-half">
              <el-input 
                v-model="form.phone" 
                placeholder="请输入手机号"
                prefix-icon="Phone"
                clearable
              />
            </el-form-item>
          </div>
          
          <el-form-item 
            label="密码" 
            prop="password"
            class="password-field"
          >
            <el-input
              v-model="form.password"
              type="password"
              :placeholder="form.id ? '留空则不修改密码' : '请输入密码'"
              prefix-icon="Lock"
              show-password
              clearable
            />
            <div class="password-tip" v-if="form.id">
              <el-icon><InfoFilled /></el-icon>
              <span>留空则不修改密码</span>
            </div>
          </el-form-item>
          
          <div class="form-row">
            <el-form-item label="角色" prop="role" class="form-item-half">
              <el-select v-model="form.role" placeholder="请选择角色" style="width: 100%">
                <el-option 
                  label="管理员" 
                  value="admin"
                >
                  <div class="role-option">
                    <el-icon class="admin-icon"><Crown /></el-icon>
                    <span>管理员</span>
                    <small>拥有所有权限</small>
                  </div>
                </el-option>
                <el-option 
                  label="普通用户" 
                  value="user"
                >
                  <div class="role-option">
                    <el-icon class="user-icon"><User /></el-icon>
                    <span>普通用户</span>
                    <small>基础功能权限</small>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="状态" prop="status" class="form-item-half">
              <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
                <el-option label="正常" value="active">
                  <div class="status-option">
                    <el-icon class="status-active"><CircleCheck /></el-icon>
                    <span>正常</span>
                  </div>
                </el-option>
                <el-option label="禁用" value="inactive">
                  <div class="status-option">
                    <el-icon class="status-inactive"><CircleClose /></el-icon>
                    <span>禁用</span>
                  </div>
                </el-option>
                <el-option label="封禁" value="banned">
                  <div class="status-option">
                    <el-icon class="status-banned"><Warning /></el-icon>
                    <span>封禁</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-form>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false" size="large">
            <el-icon><Close /></el-icon>
            取消
          </el-button>
          <el-button 
            type="primary" 
            @click="handleSubmit" 
            :loading="loading"
            size="large"
          >
            <el-icon v-if="!loading"><Check /></el-icon>
            {{ form.id ? '更新用户' : '创建用户' }}
          </el-button>
        </div>
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
      phone: '',
      password: '',
      role: 'user',
      status: 'active'
    })
    
    // 密码验证函数
    const validatePassword = (rule, value, callback) => {
      if (!form.id && (!value || value.length === 0)) {
        callback(new Error('请输入密码'))
      } else if (value && value.length < 6) {
        callback(new Error('密码长度不能少于6个字符'))
      } else {
        callback()
      }
    }
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在3到20个字符', trigger: 'blur' },
        { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字、下划线', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      password: [
        { validator: validatePassword, trigger: 'blur' }
      ],
      real_name: [
        { max: 50, message: '真实姓名长度不能超过50个字符', trigger: 'blur' }
      ],
      phone: [
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
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
          // 401错误已由请求拦截器处理，会自动显示登录弹窗
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
        // 验证表单
        await formRef.value.validate()
        
        if (form.id) {
          // 更新用户
          const updateData = { ...form }
          delete updateData.id // 移除id字段
          
          // 移除不需要的字段
          delete updateData.avatar_url
          delete updateData.created_at
          delete updateData.updated_at
          
          // 如果密码为空，则不更新密码
          if (!updateData.password || updateData.password.trim() === '') {
            delete updateData.password
          }

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
          
          // 移除不需要的字段
          delete createData.avatar_url
          delete createData.created_at
          delete createData.updated_at
          
          console.log('提交创建用户数据:', createData)
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
        // 错误信息已经在请求拦截器中处理了
        // 这里不需要再次显示错误消息
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

/* 现代化用户对话框样式 */
.modern-user-dialog :deep(.el-dialog) {
  border-radius: 20px;
  overflow: visible;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.modern-user-dialog :deep(.el-dialog__header) {
  background: transparent;
  color: #1f2937;
  padding: 32px 40px 0 40px;
  margin: 0;
  border-bottom: none;
  position: relative;
}

.modern-user-dialog :deep(.el-dialog__header::before) {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
}

.modern-user-dialog :deep(.el-dialog__title) {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.modern-user-dialog :deep(.el-dialog__headerbtn) {
  top: 32px;
  right: 40px;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  transition: all 0.3s ease;
}

.modern-user-dialog :deep(.el-dialog__headerbtn:hover) {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
  transform: scale(1.05);
}

.modern-user-dialog :deep(.el-dialog__close) {
  color: #ef4444;
  font-size: 16px;
  font-weight: 600;
}

.modern-user-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.dialog-content {
  padding: 40px;
  background: rgba(255, 255, 255, 0.5);
}

/* 用户头像区域 */
.user-avatar-section {
  margin-bottom: 40px;
  padding: 32px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 16px;
  border: 1px solid rgba(102, 126, 234, 0.1);
  position: relative;
  overflow: hidden;
}

.user-avatar-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(102,126,234,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(118,75,162,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(102,126,234,0.05)"/><circle cx="10" cy="60" r="0.5" fill="rgba(118,75,162,0.05)"/><circle cx="90" cy="40" r="0.5" fill="rgba(102,126,234,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
  pointer-events: none;
}

.avatar-container {
  display: flex;
  align-items: center;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 36px;
  box-shadow: 
    0 8px 32px rgba(102, 126, 234, 0.3),
    0 0 0 4px rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.avatar-text h3 {
  margin: 0 0 8px 0;
  font-size: 22px;
  font-weight: 700;
  color: #1f2937;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.avatar-text p {
  margin: 0;
  color: #6b7280;
  font-size: 15px;
  line-height: 1.5;
}

/* 表单样式 */
.user-form {
  margin-top: 32px;
}

.form-row {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
}

.form-item-half {
  flex: 1;
}

.password-field {
  margin-bottom: 24px;
}

.password-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding: 12px 16px;
  background: rgba(59, 130, 246, 0.05);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 8px;
  color: #3b82f6;
  font-size: 13px;
  font-weight: 500;
}

.password-tip .el-icon {
  font-size: 16px;
  color: #3b82f6;
}

/* 角色选项样式 */
.role-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}

.role-option .admin-icon {
  color: #f59e0b;
  font-size: 18px;
}

.role-option .user-icon {
  color: #3b82f6;
  font-size: 18px;
}

.role-option span {
  font-weight: 500;
}

.role-option small {
  color: #6b7280;
  margin-left: auto;
}

/* 状态选项样式 */
.status-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-active {
  color: #10b981;
}

.status-inactive {
  color: #6b7280;
}

.status-banned {
  color: #ef4444;
}

/* 对话框底部 */
.modern-user-dialog :deep(.el-dialog__footer) {
  background: rgba(248, 250, 252, 0.8);
  padding: 32px 40px;
  border-top: 1px solid rgba(229, 231, 235, 0.5);
  backdrop-filter: blur(10px);
  position: relative;
}

.modern-user-dialog :deep(.el-dialog__footer::before) {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.dialog-footer .el-button {
  border-radius: 12px;
  font-weight: 600;
  padding: 14px 28px;
  font-size: 14px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  position: relative;
  overflow: hidden;
}

.dialog-footer .el-button:not(.el-button--primary) {
  background: rgba(255, 255, 255, 0.8);
  color: #6b7280;
  border: 1px solid rgba(209, 213, 219, 0.6);
  backdrop-filter: blur(10px);
}

.dialog-footer .el-button:not(.el-button--primary):hover {
  background: rgba(255, 255, 255, 0.9);
  color: #374151;
  border-color: rgba(156, 163, 175, 0.8);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.dialog-footer .el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 
    0 4px 16px rgba(102, 126, 234, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.dialog-footer .el-button--primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.dialog-footer .el-button--primary:hover::before {
  left: 100%;
}

.dialog-footer .el-button--primary:hover {
  background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(102, 126, 234, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* 输入框样式优化 */
.user-form :deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 1px solid rgba(209, 213, 219, 0.6);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.user-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(102, 126, 234, 0.4);
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.user-form :deep(.el-input__wrapper.is-focus) {
  border-color: #667eea;
  box-shadow: 
    0 0 0 3px rgba(102, 126, 234, 0.1),
    0 4px 16px rgba(102, 126, 234, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.user-form :deep(.el-input__inner) {
  color: #1f2937;
  font-weight: 500;
  font-size: 14px;
}

.user-form :deep(.el-input__prefix) {
  color: #9ca3af;
}

.user-form :deep(.el-select .el-input__wrapper) {
  border-radius: 12px;
}

/* 表单项标签样式 */
.user-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #374151;
  font-size: 14px;
  margin-bottom: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .avatar-container {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .dialog-content {
    padding: 24px;
  }
  
  .modern-user-dialog :deep(.el-dialog__header),
  .modern-user-dialog :deep(.el-dialog__footer) {
    padding: 20px 24px;
  }
}
</style>
