<template>
  <div class="announcement-management">
    <div class="page-header">
      <h1>系统公告</h1>
      <div class="header-info">
        <el-tag type="info">共 {{ announcements.length }} 条公告</el-tag>
        <el-button type="primary" @click="showCreateDialog = true" v-if="isAdmin">
          <el-icon><Plus /></el-icon>
          新建公告
        </el-button>
      </div>
    </div>

    <!-- 公告统计 -->
    <div class="statistics-section" v-if="isAdmin">
      <el-card>
        <div class="statistics-header">
          <h3>公告统计</h3>
        </div>
        <div class="statistics-content">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon color="#409eff"><Document /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.total_count || 0 }}</div>
                  <div class="stat-label">总公告数</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon color="#67c23a"><Check /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.published_count || 0 }}</div>
                  <div class="stat-label">已发布</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon color="#e6a23c"><Edit /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.draft_count || 0 }}</div>
                  <div class="stat-label">草稿</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon color="#f56c6c"><Warning /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.recent_count || 0 }}</div>
                  <div class="stat-label">最近7天</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-card>
        <el-form :model="searchForm" inline>
          <el-form-item label="关键词">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索公告标题"
              clearable
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item label="类型">
            <el-select
              v-model="searchForm.type"
              placeholder="选择类型"
              clearable
              style="width: 120px"
            >
              <el-option label="系统公告" value="system" />
              <el-option label="考试公告" value="exam" />
              <el-option label="维护公告" value="maintenance" />
            </el-select>
          </el-form-item>
          <el-form-item label="优先级">
            <el-select
              v-model="searchForm.priority"
              placeholder="选择优先级"
              clearable
              style="width: 120px"
            >
              <el-option label="高优先级" value="high" />
              <el-option label="中优先级" value="medium" />
              <el-option label="低优先级" value="low" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态" v-if="isAdmin">
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

    <!-- 公告列表 -->
    <div class="announcements-list">
      <el-card>
        <div class="list-header">
          <div class="list-title">
            <span>公告列表</span>
            <el-tag v-if="selectedAnnouncements.length > 0" type="info">
              已选择 {{ selectedAnnouncements.length }} 条公告
            </el-tag>
          </div>
          <div class="list-actions" v-if="selectedAnnouncements.length > 0 && isAdmin">
            <el-button size="small" type="success" @click="batchPublish">
              <el-icon><Check /></el-icon>
              批量发布
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete">
              <el-icon><Delete /></el-icon>
              批量删除
            </el-button>
          </div>
        </div>

        <el-table
          :data="announcements"
          :loading="loading"
          @selection-change="handleSelectionChange"
          row-key="id"
          stripe
        >
          <el-table-column type="selection" width="55" v-if="isAdmin" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="公告标题" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="announcement-title">
                <span :class="{ 'unread-title': !row.is_published }">{{ row.title }}</span>
                <div class="announcement-meta">
                  <el-tag :type="getTypeTagType(row.type)" size="small">
                    {{ getTypeLabel(row.type) }}
                  </el-tag>
                  <el-tag :type="getPriorityTagType(row.priority)" size="small">
                    {{ getPriorityLabel(row.priority) }}
                  </el-tag>
                  <el-tag :type="getStatusTagType(row.status)" size="small">
                    {{ getStatusLabel(row.status) }}
                  </el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="content" label="公告内容" min-width="250" show-overflow-tooltip />
          <el-table-column prop="view_count" label="查看次数" width="100" />
          <el-table-column prop="publish_time" label="发布时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.publish_time) }}
            </template>
          </el-table-column>
          <el-table-column prop="expire_time" label="过期时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.expire_time) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewAnnouncement(row)">
                查看
              </el-button>
              <el-button size="small" type="success" @click="publishAnnouncement(row)" v-if="isAdmin && row.status === 'draft'">
                发布
              </el-button>
              <el-button size="small" type="warning" @click="unpublishAnnouncement(row)" v-if="isAdmin && row.status === 'published'">
                取消发布
              </el-button>
              <el-dropdown @command="(command) => handleAction(command, row)" v-if="isAdmin">
                <el-button size="small">
                  更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">编辑</el-dropdown-item>
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

    <!-- 公告详情对话框 -->
    <el-dialog
      v-model="showAnnouncementDialog"
      title="公告详情"
      width="60%"
    >
      <div v-if="viewingAnnouncement" class="announcement-detail">
        <div class="detail-header">
          <div class="detail-title">
            <h3>{{ viewingAnnouncement.title }}</h3>
            <div class="detail-meta">
              <el-tag :type="getTypeTagType(viewingAnnouncement.type)" size="small">
                {{ getTypeLabel(viewingAnnouncement.type) }}
              </el-tag>
              <el-tag :type="getPriorityTagType(viewingAnnouncement.priority)" size="small">
                {{ getPriorityLabel(viewingAnnouncement.priority) }}
              </el-tag>
              <el-tag :type="getStatusTagType(viewingAnnouncement.status)" size="small">
                {{ getStatusLabel(viewingAnnouncement.status) }}
              </el-tag>
            </div>
          </div>
          <div class="detail-time">
            <span>发布时间: {{ formatDate(viewingAnnouncement.publish_time) }}</span>
            <span v-if="viewingAnnouncement.expire_time">
              过期时间: {{ formatDate(viewingAnnouncement.expire_time) }}
            </span>
            <span>查看次数: {{ viewingAnnouncement.view_count }}</span>
          </div>
        </div>
        <div class="detail-content">
          <div class="content-text">
            {{ viewingAnnouncement.content }}
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="showAnnouncementDialog = false">关闭</el-button>
        <el-button type="primary" @click="publishAnnouncement(viewingAnnouncement)" v-if="isAdmin && viewingAnnouncement && viewingAnnouncement.status === 'draft'">
          发布公告
        </el-button>
      </template>
    </el-dialog>

    <!-- 创建/编辑公告对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingAnnouncement ? '编辑公告' : '新建公告'"
      width="600px"
    >
      <el-form :model="announcementForm" :rules="announcementRules" ref="announcementFormRef" label-width="100px">
        <el-form-item label="公告标题" prop="title">
          <el-input v-model="announcementForm.title" placeholder="请输入公告标题" />
        </el-form-item>
        <el-form-item label="公告内容" prop="content">
          <el-input v-model="announcementForm.content" type="textarea" :rows="6" placeholder="请输入公告内容" />
        </el-form-item>
        <el-form-item label="公告类型" prop="type">
          <el-select v-model="announcementForm.type" placeholder="选择公告类型">
            <el-option label="系统公告" value="system" />
            <el-option label="考试公告" value="exam" />
            <el-option label="维护公告" value="maintenance" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="announcementForm.priority" placeholder="选择优先级">
            <el-option label="高优先级" value="high" />
            <el-option label="中优先级" value="medium" />
            <el-option label="低优先级" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="过期时间">
          <el-date-picker
            v-model="announcementForm.expire_time"
            type="datetime"
            placeholder="选择过期时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="saveAnnouncement">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Document, Check, Edit, Warning, Search, Refresh, Delete, ArrowDown
} from '@element-plus/icons-vue'
import { announcementApi } from '@/api/announcements'
import { useAuthStore } from '@/stores/auth'
import { formatDate } from '@/utils/format'

export default {
  name: 'AnnouncementManagement',
  components: {
    Plus,
    Document,
    Check,
    Edit,
    Warning,
    Search,
    Refresh,
    Delete,
    ArrowDown
  },
  setup() {
    const authStore = useAuthStore()
    
    // 响应式数据
    const loading = ref(false)
    const announcements = ref([])
    const selectedAnnouncements = ref([])
    const statistics = ref({})
    const showAnnouncementDialog = ref(false)
    const showCreateDialog = ref(false)
    const viewingAnnouncement = ref(null)
    const editingAnnouncement = ref(null)
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      type: '',
      priority: '',
      status: ''
    })
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 公告表单
    const announcementForm = reactive({
      title: '',
      content: '',
      type: 'system',
      priority: 'medium',
      expire_time: ''
    })
    
    const announcementRules = {
      title: [
        { required: true, message: '请输入公告标题', trigger: 'blur' }
      ],
      content: [
        { required: true, message: '请输入公告内容', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择公告类型', trigger: 'change' }
      ],
      priority: [
        { required: true, message: '请选择优先级', trigger: 'change' }
      ]
    }
    
    // 计算属性
    const isAdmin = computed(() => {
      return authStore.user?.role === 'admin'
    })
    
    // 方法
    const loadAnnouncements = async () => {
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
        
        const response = await announcementApi.getAnnouncements(params)
        announcements.value = response.data.items
        pagination.total = response.data.total
      } catch (error) {
        ElMessage.error('加载公告列表失败')
        console.error('Load announcements error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadStatistics = async () => {
      try {
        const response = await announcementApi.getStatistics()
        statistics.value = response.data
      } catch (error) {
        console.error('Load statistics error:', error)
      }
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadAnnouncements()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadAnnouncements()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadAnnouncements()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadAnnouncements()
    }
    
    const handleSelectionChange = (selection) => {
      selectedAnnouncements.value = selection
    }
    
    const viewAnnouncement = (announcement) => {
      viewingAnnouncement.value = announcement
      showAnnouncementDialog.value = true
    }
    
    const publishAnnouncement = async (announcement) => {
      try {
        await announcementApi.publishAnnouncement(announcement.id)
        ElMessage.success('发布公告成功')
        loadAnnouncements()
        loadStatistics()
      } catch (error) {
        ElMessage.error('发布公告失败')
        console.error('Publish announcement error:', error)
      }
    }
    
    const unpublishAnnouncement = async (announcement) => {
      try {
        await announcementApi.unpublishAnnouncement(announcement.id)
        ElMessage.success('取消发布成功')
        loadAnnouncements()
        loadStatistics()
      } catch (error) {
        ElMessage.error('取消发布失败')
        console.error('Unpublish announcement error:', error)
      }
    }
    
    const handleAction = async (command, announcement) => {
      switch (command) {
        case 'edit':
          await editAnnouncement(announcement)
          break
        case 'delete':
          await deleteAnnouncement(announcement)
          break
      }
    }
    
    const editAnnouncement = (announcement) => {
      editingAnnouncement.value = announcement
      Object.assign(announcementForm, {
        title: announcement.title,
        content: announcement.content,
        type: announcement.type,
        priority: announcement.priority,
        expire_time: announcement.expire_time
      })
      showCreateDialog.value = true
    }
    
    const deleteAnnouncement = async (announcement) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除公告"${announcement.title}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await announcementApi.deleteAnnouncement(announcement.id)
        ElMessage.success('删除公告成功')
        loadAnnouncements()
        loadStatistics()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除公告失败')
          console.error('Delete announcement error:', error)
        }
      }
    }
    
    const batchPublish = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要发布选中的 ${selectedAnnouncements.value.length} 条公告吗？`,
          '确认批量发布',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const announcementIds = selectedAnnouncements.value.map(a => a.id)
        await announcementApi.batchPublish({ announcement_ids: announcementIds })
        
        ElMessage.success('批量发布成功')
        selectedAnnouncements.value = []
        loadAnnouncements()
        loadStatistics()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量发布失败')
          console.error('Batch publish error:', error)
        }
      }
    }
    
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedAnnouncements.value.length} 条公告吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const announcementIds = selectedAnnouncements.value.map(a => a.id)
        await announcementApi.batchDelete({ announcement_ids: announcementIds })
        
        ElMessage.success('批量删除成功')
        selectedAnnouncements.value = []
        loadAnnouncements()
        loadStatistics()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    const saveAnnouncement = async () => {
      try {
        if (editingAnnouncement.value) {
          await announcementApi.updateAnnouncement(editingAnnouncement.value.id, announcementForm)
          ElMessage.success('更新公告成功')
        } else {
          await announcementApi.createAnnouncement(announcementForm)
          ElMessage.success('创建公告成功')
        }
        
        showCreateDialog.value = false
        editingAnnouncement.value = null
        Object.keys(announcementForm).forEach(key => {
          announcementForm[key] = key === 'type' ? 'system' : key === 'priority' ? 'medium' : ''
        })
        loadAnnouncements()
        loadStatistics()
      } catch (error) {
        ElMessage.error('保存公告失败')
        console.error('Save announcement error:', error)
      }
    }
    
    // 工具方法
    const getTypeLabel = (type) => {
      const labels = {
        system: '系统公告',
        exam: '考试公告',
        maintenance: '维护公告'
      }
      return labels[type] || type
    }
    
    const getTypeTagType = (type) => {
      const types = {
        system: 'primary',
        exam: 'success',
        maintenance: 'warning'
      }
      return types[type] || 'default'
    }
    
    const getPriorityLabel = (priority) => {
      const labels = {
        high: '高优先级',
        medium: '中优先级',
        low: '低优先级'
      }
      return labels[priority] || priority
    }
    
    const getPriorityTagType = (priority) => {
      const types = {
        high: 'danger',
        medium: 'warning',
        low: 'success'
      }
      return types[priority] || 'default'
    }
    
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
    
    // 生命周期
    onMounted(() => {
      loadAnnouncements()
      if (isAdmin.value) {
        loadStatistics()
      }
    })
    
    return {
      loading,
      announcements,
      selectedAnnouncements,
      statistics,
      showAnnouncementDialog,
      showCreateDialog,
      viewingAnnouncement,
      editingAnnouncement,
      searchForm,
      pagination,
      announcementForm,
      announcementRules,
      isAdmin,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewAnnouncement,
      publishAnnouncement,
      unpublishAnnouncement,
      handleAction,
      editAnnouncement,
      deleteAnnouncement,
      batchPublish,
      batchDelete,
      saveAnnouncement,
      getTypeLabel,
      getTypeTagType,
      getPriorityLabel,
      getPriorityTagType,
      getStatusLabel,
      getStatusTagType,
      formatDate
    }
  }
}
</script>

<style scoped>
.announcement-management {
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

.header-info {
  display: flex;
  gap: 10px;
}

.statistics-section {
  margin-bottom: 20px;
}

.statistics-header {
  margin-bottom: 20px;
}

.statistics-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.statistics-content {
  padding: 20px 0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-item:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.stat-icon {
  font-size: 24px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.search-section {
  margin-bottom: 20px;
}

.announcements-list {
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

.announcement-title {
  line-height: 1.5;
}

.unread-title {
  font-weight: 600;
  color: #303133;
}

.announcement-meta {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.announcement-detail {
  padding: 20px 0;
}

.detail-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.detail-title h3 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
}

.detail-meta {
  display: flex;
  gap: 10px;
}

.detail-time {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 14px;
  color: #909399;
}

.detail-content {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.content-text {
  color: #606266;
  line-height: 1.6;
  font-size: 16px;
}

:deep(.el-table .el-table__row) {
  cursor: pointer;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f7fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .announcement-management {
    padding: 15px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .statistics-content .el-col {
    margin-bottom: 15px;
  }
  
  .list-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .detail-time {
    flex-direction: row;
    gap: 15px;
  }
}
</style>
