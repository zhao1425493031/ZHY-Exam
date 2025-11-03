<template>
  <div class="modern-user-subject-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Link /></el-icon>
            </div>
            <div class="title-text">
              <h1>用户课程关联管理</h1>
              <p>管理系统用户和课程之间的关联关系</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="handleAdd" class="add-btn">
            <el-icon><Plus /></el-icon>
            <span>添加关联</span>
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
          <p>快速查找用户课程关联信息</p>
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
              <el-input
                v-model="searchForm.subject_name"
                placeholder="请输入课程名称"
                prefix-icon="Search"
                class="search-input"
              />
            </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.status" placeholder="选择状态" class="filter-select">
                <el-option label="全部状态" value="" />
                <el-option label="待承认" value="pending" />
                <el-option label="已承认" value="approved" />
                <el-option label="拒绝" value="rejected" />
                <el-option label="正常" value="active" />
                <el-option label="已过期" value="expired" />
                <el-option label="已取消" value="cancelled" />
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

    <!-- 关联列表 -->
    <div class="table-section">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>关联列表</h3>
            <p>共 {{ total }} 条记录</p>
          </div>
        </div>
        
        <div class="table-container">
          <el-table
            :data="tableData"
            v-loading="loading"
            class="modern-table"
            stripe
          >
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="用户信息" min-width="180">
              <template #default="{ row }">
                <div class="user-info">
                  <div class="user-avatar">{{ row.username.charAt(0).toUpperCase() }}</div>
                  <div class="user-details">
                    <div class="user-name">{{ row.username }}</div>
                    <div class="user-email">{{ row.user_email }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="课程信息" min-width="180">
              <template #default="{ row }">
                <div class="subject-info">
                  <div class="subject-avatar">{{ row.subject_name.charAt(0) }}</div>
                  <div class="subject-details">
                    <div class="subject-name">{{ row.subject_name }}</div>
                    <div class="subject-code">{{ row.subject_code }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="120" align="center" show-overflow-tooltip>
              <template #default="{ row }">
                <el-tag 
                  :type="getStatusType(row?.status || 'pending')" 
                  size="small"
                >
                  {{ getStatusText(row?.status || 'pending') }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="关联类型" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_free ? 'success' : 'warning'">
                  {{ row.is_free ? '免费' : '付费' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="购买时间" width="180">
              <template #default="{ row }">
                <span v-if="row.purchased_at">{{ formatDate(row.purchased_at) }}</span>
                <span v-else class="text-gray">-</span>
              </template>
            </el-table-column>
            <el-table-column label="到期时间" width="180">
              <template #default="{ row }">
                <span v-if="row.expires_at">{{ formatDate(row.expires_at) }}</span>
                <span v-else class="text-gray">永久有效</span>
              </template>
            </el-table-column>
            <el-table-column label="关联时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="300" fixed="right" align="center">
              <template #default="{ row }">
                <div class="action-buttons">
                  <!-- 待承认状态：显示承认和拒绝按钮 -->
                  <template v-if="row?.status === 'pending'">
                    <el-button
                      type="success"
                      size="small"
                      @click="handleApprove(row)"
                    >
                      承认
                    </el-button>
                    <el-button
                      type="danger"
                      size="small"
                      @click="handleReject(row)"
                    >
                      拒绝
                    </el-button>
                  </template>
                  <!-- 已拒绝状态：显示承认按钮 -->
                  <template v-else-if="row?.status === 'rejected'">
                    <el-button
                      type="success"
                      size="small"
                      @click="handleApprove(row)"
                    >
                      承认
                    </el-button>
                  </template>
                  <!-- 已承认状态：显示激活按钮 -->
                  <template v-else-if="row?.status === 'approved'">
                    <el-button
                      type="primary"
                      size="small"
                      @click="handleActivate(row)"
                    >
                      激活
                    </el-button>
                  </template>
                  <!-- 正常状态：显示取消按钮 -->
                  <template v-else-if="row?.status === 'active'">
                    <el-button
                      type="warning"
                      size="small"
                      @click="handleCancel(row)"
                    >
                      取消
                    </el-button>
                  </template>
                  <!-- 其他状态（包括已过期、已取消等）：显示激活和承认按钮 -->
                  <template v-else>
                    <el-button
                      type="primary"
                      size="small"
                      @click="handleActivate(row)"
                    >
                      激活
                    </el-button>
                    <el-button
                      type="success"
                      size="small"
                      @click="handleApprove(row)"
                      v-if="row?.status !== 'expired' && row?.status !== 'cancelled'"
                    >
                      承认
                    </el-button>
                  </template>
                  <!-- 删除按钮 - 始终显示 -->
                  <el-button
                    type="danger"
                    size="small"
                    @click="handleDelete(row)"
                  >
                    删除
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
            v-model:page-size="pagination.per_page"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>

    <!-- 添加关联对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="添加用户课程关联"
      width="500px"
      class="modern-dialog"
    >
      <el-form
        :model="formData"
        :rules="formRules"
        ref="formRef"
        label-width="100px"
      >
        <el-form-item label="选择用户" prop="user_id">
          <el-select
            v-model="formData.user_id"
            placeholder="请选择用户"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="user in users"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            >
              <span>{{ user.username }}</span>
              <span class="text-gray"> ({{ user.email }})</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择课程" prop="subject_id">
          <el-select
            v-model="formData.subject_id"
            placeholder="请选择课程"
            filterable
            style="width: 100%"
            @change="handleSubjectChange"
          >
            <el-option
              v-for="subject in subjects"
              :key="subject.id"
              :label="subject.name"
              :value="subject.id"
            >
              <span>{{ subject.name }}</span>
              <span class="text-gray"> ({{ subject.code }})</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="关联类型">
          <el-tag :type="formData.is_free ? 'success' : 'warning'">
            {{ formData.is_free ? '免费' : '付费' }}
          </el-tag>
          <span class="form-tip">（根据所选课程自动设置）</span>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select
            v-model="formData.status"
            placeholder="请选择状态"
            style="width: 100%"
          >
            <el-option label="待承认" value="pending" />
            <el-option label="已承认" value="approved" />
            <el-option label="拒绝" value="rejected" />
            <el-option label="正常" value="active" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Link, Plus, ArrowLeft, Search, Refresh } from '@element-plus/icons-vue'
import { userSubjectsApi } from '@/api/user_subjects'
import { usersApi } from '@/api/users'
import { subjectsApi } from '@/api/subjects'
import dayjs from 'dayjs'

const router = useRouter()

// 数据
const tableData = ref([])
const users = ref([])
const subjects = ref([])
const total = ref(0)
const loading = ref(false)
const submitting = ref(false)

// 搜索表单
const searchForm = reactive({
  username: '',
  subject_name: '',
  status: ''
})

// 分页
const pagination = reactive({
  page: 1,
  per_page: 10
})

// 对话框
const dialogVisible = ref(false)
const formRef = ref(null)
const formData = reactive({
  user_id: '',
  subject_id: '',
  is_free: true,
  status: 'pending'
})

// 表单验证规则
const formRules = {
  user_id: [{ required: true, message: '请选择用户', trigger: 'change' }],
  subject_id: [{ required: true, message: '请选择课程', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 课程选择变化时，自动设置关联类型
const handleSubjectChange = (subjectId) => {
  if (subjectId) {
    const subject = subjects.value.find(s => s.id === subjectId)
    if (subject) {
      formData.is_free = subject.is_free
      console.log(`课程 ${subject.name} 的关联类型已自动设置为: ${subject.is_free ? '免费' : '付费'}`)
    }
  }
}

// 加载用户和课程列表
const loadUsers = async () => {
  try {
    // 后端限制size最大100，分页加载所有用户
    const allUsers = []
    let page = 1
    const size = 100
    
    while (true) {
      const response = await usersApi.getUsers({ page, size })
      const items = response.data?.items || []
      allUsers.push(...items)
      
      // 如果返回的数据少于size，说明已经是最后一页
      if (items.length < size) {
        break
      }
      page++
    }
    
    users.value = allUsers
    console.log('加载用户列表成功，共', allUsers.length, '个用户')
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载用户列表失败: ' + (error.message || '未知错误'))
    users.value = []
  }
}

const loadSubjects = async () => {
  try {
    // 后端限制size最大100，分页加载所有课程
    const allSubjects = []
    let page = 1
    const size = 100
    
    while (true) {
      const response = await subjectsApi.getSubjects({ page, size })
      const items = response.data?.items || []
      allSubjects.push(...items)
      
      // 如果返回的数据少于size，说明已经是最后一页
      if (items.length < size) {
        break
      }
      page++
    }
    
    subjects.value = allSubjects
    console.log('加载课程列表成功，共', allSubjects.length, '个课程')
  } catch (error) {
    console.error('加载课程列表失败:', error)
    ElMessage.error('加载课程列表失败: ' + (error.message || '未知错误'))
    subjects.value = []
  }
}

// 加载关联列表
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      per_page: pagination.per_page
    }
    
    if (searchForm.username) {
      // 如果需要按用户名搜索，先获取用户ID
      // 这里简化处理，实际应该后端支持用户名搜索
    }
    if (searchForm.subject_name) {
      // 如果需要按课程名搜索，先获取课程ID
      // 这里简化处理，实际应该后端支持课程名搜索
    }
    if (searchForm.status) {
      params.status = searchForm.status
    }

    const response = await userSubjectsApi.adminGetUserSubjects(params)
    tableData.value = response.data.items || []
    total.value = response.data.total || 0
  } catch (error) {
    console.error('加载关联列表失败:', error)
    ElMessage.error('加载关联列表失败')
  } finally {
    loading.value = false
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return dayjs(dateStr).format('YYYY-MM-DD HH:mm:ss')
}

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    active: 'success',
    expired: 'warning',
    cancelled: 'danger'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    pending: '待承认',
    approved: '已承认',
    rejected: '拒绝',
    active: '正常',
    expired: '已过期',
    cancelled: '已取消'
  }
  return statusMap[status] || '未知'
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadData()
}

// 重置
const handleReset = () => {
  searchForm.username = ''
  searchForm.subject_name = ''
  searchForm.status = ''
  pagination.page = 1
  loadData()
}

// 分页改变
const handlePageChange = () => {
  loadData()
}

const handleSizeChange = () => {
  loadData()
}

// 添加关联
const handleAdd = async () => {
  formData.user_id = ''
  formData.subject_id = ''
  formData.is_free = true
  formData.status = 'pending'
  
  // 如果用户列表或课程列表为空，重新加载
  if (users.value.length === 0) {
    await loadUsers()
  }
  if (subjects.value.length === 0) {
    await loadSubjects()
  }
  
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    await userSubjectsApi.adminCreateUserSubject(formData)
    ElMessage.success('添加关联成功')
    dialogVisible.value = false
    loadData()
  } catch (error) {
    if (error.errorFields) return // 表单验证失败
    console.error('添加关联失败:', error)
    ElMessage.error(error.message || '添加关联失败')
  } finally {
    submitting.value = false
  }
}

// 激活
const handleActivate = async (row) => {
  try {
    await userSubjectsApi.adminUpdateUserSubjectStatus(row.id, 'active')
    ElMessage.success('激活成功')
    loadData()
  } catch (error) {
    console.error('激活失败:', error)
    ElMessage.error('激活失败')
  }
}

// 承认
const handleApprove = async (row) => {
  try {
    await userSubjectsApi.adminUpdateUserSubjectStatus(row.id, 'approved')
    ElMessage.success('承认成功')
    loadData()
  } catch (error) {
    console.error('承认失败:', error)
    ElMessage.error('承认失败')
  }
}

// 拒绝
const handleReject = async (row) => {
  try {
    await ElMessageBox.confirm('确定要拒绝该关联吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await userSubjectsApi.adminUpdateUserSubjectStatus(row.id, 'rejected')
    ElMessage.success('已拒绝')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('拒绝失败:', error)
      ElMessage.error('拒绝失败')
    }
  }
}

// 取消
const handleCancel = async (row) => {
  try {
    await ElMessageBox.confirm('确定要取消该关联吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await userSubjectsApi.adminUpdateUserSubjectStatus(row.id, 'cancelled')
    ElMessage.success('取消成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消失败:', error)
      ElMessage.error('取消失败')
    }
  }
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该关联吗？删除后不可恢复！', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await userSubjectsApi.adminDeleteUserSubject(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 返回
const goBack = () => {
  router.push('/admin')
}

// 初始化
onMounted(() => {
  loadUsers()
  loadSubjects()
  loadData()
})
</script>

<style scoped lang="scss">
.modern-user-subject-management {
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
      margin-bottom: 24px;
      
      .table-title {
        display: flex;
        align-items: center;
        gap: 12px;
        
        h3 {
          font-size: 20px;
          font-weight: 700;
          color: #1a1a1a;
          margin: 0;
        }
        
        p {
          color: #666;
          font-size: 14px;
          margin: 0;
        }
        
        .count-tag {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          font-weight: 600;
        }
      }
    }
    
    .modern-table {
      :deep(.el-table__header) {
        th {
          background: #f8fafc;
          color: #475569;
          font-weight: 600;
          font-size: 14px;
        }
      }
      
      :deep(.el-table__body) {
        tr {
          transition: all 0.2s ease;
          
          &:hover {
            background: #f8fafc;
          }
        }
      }
      
      .user-info,
      .subject-info {
        display: flex;
        align-items: center;
        gap: 12px;
        
        .user-avatar,
        .subject-avatar {
          width: 32px;
          height: 32px;
          border-radius: 8px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-weight: 600;
          font-size: 14px;
        }
        
        .user-details,
        .subject-details {
          .user-name,
          .subject-name {
            font-weight: 600;
            color: #1a1a1a;
            font-size: 14px;
          }
          
          .user-email,
          .subject-code {
            font-size: 12px;
            color: #94a3b8;
            margin-top: 2px;
          }
        }
      }
      
      .text-gray {
        color: #94a3b8;
      }
      
      .action-buttons {
        display: flex;
        gap: 8px;
        
        .el-button {
          padding: 6px 12px;
          border-radius: 8px;
          font-weight: 500;
          transition: all 0.2s ease;
          
          &:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
          }
        }
      }
    }
    
    .pagination-section {
      margin-top: 24px;
      display: flex;
      justify-content: flex-end;
      padding-top: 24px;
      border-top: 1px solid #e5e7eb;
      
      :deep(.el-pagination) {
        .el-pagination__sizes {
          .el-select {
            .el-select__wrapper {
              border-radius: 8px;
              box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
          }
        }
        
        .el-pager {
          li {
            border-radius: 8px;
            font-weight: 600;
            
            &.is-active {
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              color: white;
            }
          }
        }
        
        .btn-prev,
        .btn-next {
          border-radius: 8px;
          font-weight: 600;
        }
      }
    }
  }
}

.modern-dialog {
  :deep(.el-dialog__header) {
    padding: 24px 24px 16px;
    border-bottom: 1px solid #e5e7eb;
    
    .el-dialog__title {
      font-size: 20px;
      font-weight: 700;
      color: #1a1a1a;
    }
  }
  
  :deep(.el-dialog__body) {
    padding: 24px;
    
      .el-form-item {
        margin-bottom: 20px;
        
        .el-form-item__label {
          font-weight: 600;
          color: #475569;
        }
        
        .form-tip {
          margin-left: 12px;
          font-size: 12px;
          color: #94a3b8;
          font-style: italic;
        }
      }
  }
  
  :deep(.el-dialog__footer) {
    padding: 16px 24px;
    border-top: 1px solid #e5e7eb;
    
    .dialog-footer {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      
      .el-button {
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
        
        &.el-button--primary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border: none;
          
          &:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
          }
        }
      }
    }
  }
}
</style>

