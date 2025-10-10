<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleAdd">添加用户</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-area">
        <el-form :model="searchForm" inline>
          <el-form-item label="用户名">
            <el-input v-model="searchForm.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="searchForm.role" placeholder="请选择角色">
              <el-option label="全部" value="" />
              <el-option label="管理员" value="admin" />
              <el-option label="普通用户" value="user" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态">
              <el-option label="全部" value="" />
              <el-option label="正常" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 用户表格 -->
      <el-table :data="users" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="real_name" label="真实姓名" />
        <el-table-column prop="role" label="角色">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
              {{ row.role === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button 
              size="small" 
              :type="row.status === 'active' ? 'warning' : 'success'"
              @click="handleToggleStatus(row)"
            >
              {{ row.status === 'active' ? '禁用' : '启用' }}
            </el-button>
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
    
    <!-- 用户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
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
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

export default {
  name: 'UserManagement',
  setup() {
    const formRef = ref()
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    
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
    
    const loadUsers = async () => {
      // 模拟数据，实际应该调用API
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
          '确定要删除这个用户吗？',
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        // 实际应该调用删除API
        ElMessage.success('删除成功')
        loadUsers()
      } catch (error) {
        // 用户取消删除
      }
    }
    
    const handleToggleStatus = async (row) => {
      const newStatus = row.status === 'active' ? 'inactive' : 'active'
      const action = newStatus === 'active' ? '启用' : '禁用'
      
      try {
        await ElMessageBox.confirm(
          `确定要${action}这个用户吗？`,
          `确认${action}`,
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        // 实际应该调用API
        row.status = newStatus
        ElMessage.success(`${action}成功`)
      } catch (error) {
        // 用户取消操作
      }
    }
    
    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        // 实际应该调用API
        ElMessage.success(form.id ? '更新成功' : '添加成功')
        dialogVisible.value = false
        loadUsers()
      } catch (error) {
        console.error('表单验证失败:', error)
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
      handleSizeChange
    }
  }
}
</script>

<style scoped>
.user-management {
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
