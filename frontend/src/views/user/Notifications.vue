<template>
  <div class="notifications">
    <div class="page-header">
      <h1>消息通知</h1>
      <div class="header-info">
        <el-tag type="warning" v-if="unreadCount > 0">
          未读消息: {{ unreadCount }}
        </el-tag>
        <el-tag type="success" v-else>
          暂无未读消息
        </el-tag>
      </div>
    </div>

    <!-- 通知设置 -->
    <div class="notification-settings">
      <el-card>
        <div class="settings-header">
          <h3>通知设置</h3>
          <el-button size="small" @click="showSettingsDialog = true">
            <el-icon><Setting /></el-icon>
            设置
          </el-button>
        </div>
        <div class="settings-content">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="setting-item">
                <el-icon color="#409eff"><Message /></el-icon>
                <span>系统通知</span>
                <el-switch v-model="settings.system_notifications" @change="updateSettings" />
              </div>
            </el-col>
            <el-col :span="6">
              <div class="setting-item">
                <el-icon color="#67c23a"><Document /></el-icon>
                <span>考试通知</span>
                <el-switch v-model="settings.exam_notifications" @change="updateSettings" />
              </div>
            </el-col>
            <el-col :span="6">
              <div class="setting-item">
                <el-icon color="#e6a23c"><Trophy /></el-icon>
                <span>成绩通知</span>
                <el-switch v-model="settings.score_notifications" @change="updateSettings" />
              </div>
            </el-col>
            <el-col :span="6">
              <div class="setting-item">
                <el-icon color="#f56c6c"><Bell /></el-icon>
                <span>公告通知</span>
                <el-switch v-model="settings.announcement_notifications" @change="updateSettings" />
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
              placeholder="搜索通知标题"
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
              <el-option label="系统通知" value="system" />
              <el-option label="考试通知" value="exam" />
              <el-option label="成绩通知" value="score" />
              <el-option label="公告通知" value="announcement" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select
              v-model="searchForm.is_read"
              placeholder="选择状态"
              clearable
              style="width: 120px"
            >
              <el-option label="未读" :value="false" />
              <el-option label="已读" :value="true" />
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

    <!-- 通知列表 -->
    <div class="notifications-list">
      <el-card>
        <div class="list-header">
          <div class="list-title">
            <span>通知列表</span>
            <el-tag v-if="selectedNotifications.length > 0" type="info">
              已选择 {{ selectedNotifications.length }} 条通知
            </el-tag>
          </div>
          <div class="list-actions" v-if="selectedNotifications.length > 0">
            <el-button size="small" type="success" @click="batchMarkAsRead">
              <el-icon><Check /></el-icon>
              批量标记已读
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete">
              <el-icon><Delete /></el-icon>
              批量删除
            </el-button>
          </div>
        </div>

        <el-table
          :data="notifications"
          :loading="loading"
          @selection-change="handleSelectionChange"
          row-key="id"
          stripe
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="通知标题" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="notification-title">
                <span :class="{ 'unread-title': !row.is_read }">{{ row.title }}</span>
                <div class="notification-meta">
                  <el-tag :type="getTypeTagType(row.type)" size="small">
                    {{ getTypeLabel(row.type) }}
                  </el-tag>
                  <el-tag :type="row.is_read ? 'success' : 'warning'" size="small">
                    {{ row.is_read ? '已读' : '未读' }}
                  </el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="content" label="通知内容" min-width="250" show-overflow-tooltip />
          <el-table-column prop="created_at" label="创建时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="read_at" label="阅读时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.read_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewNotification(row)">
                查看
              </el-button>
              <el-button size="small" type="primary" @click="markAsRead(row)" v-if="!row.is_read">
                标记已读
              </el-button>
              <el-dropdown @command="(command) => handleAction(command, row)">
                <el-button size="small">
                  更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="delete">删除通知</el-dropdown-item>
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

    <!-- 通知详情对话框 -->
    <el-dialog
      v-model="showNotificationDialog"
      title="通知详情"
      width="60%"
    >
      <div v-if="viewingNotification" class="notification-detail">
        <div class="detail-header">
          <div class="detail-title">
            <h3>{{ viewingNotification.title }}</h3>
            <div class="detail-meta">
              <el-tag :type="getTypeTagType(viewingNotification.type)" size="small">
                {{ getTypeLabel(viewingNotification.type) }}
              </el-tag>
              <el-tag :type="viewingNotification.is_read ? 'success' : 'warning'" size="small">
                {{ viewingNotification.is_read ? '已读' : '未读' }}
              </el-tag>
            </div>
          </div>
          <div class="detail-time">
            <span>创建时间: {{ formatDate(viewingNotification.created_at) }}</span>
            <span v-if="viewingNotification.read_at">
              阅读时间: {{ formatDate(viewingNotification.read_at) }}
            </span>
          </div>
        </div>
        <div class="detail-content">
          <div class="content-text">
            {{ viewingNotification.content }}
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="showNotificationDialog = false">关闭</el-button>
        <el-button type="primary" @click="markAsRead(viewingNotification)" v-if="viewingNotification && !viewingNotification.is_read">
          标记已读
        </el-button>
      </template>
    </el-dialog>

    <!-- 通知设置对话框 -->
    <el-dialog
      v-model="showSettingsDialog"
      title="通知设置"
      width="500px"
    >
      <el-form :model="settings" label-width="120px">
        <el-form-item label="邮件通知">
          <el-switch v-model="settings.email_notifications" />
        </el-form-item>
        <el-form-item label="系统通知">
          <el-switch v-model="settings.system_notifications" />
        </el-form-item>
        <el-form-item label="考试通知">
          <el-switch v-model="settings.exam_notifications" />
        </el-form-item>
        <el-form-item label="成绩通知">
          <el-switch v-model="settings.score_notifications" />
        </el-form-item>
        <el-form-item label="公告通知">
          <el-switch v-model="settings.announcement_notifications" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSettingsDialog = false">取消</el-button>
        <el-button type="primary" @click="saveSettings">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting, Message, Document, Trophy, Bell, Search, Refresh, Check, Delete, ArrowDown
} from '@element-plus/icons-vue'
import { notificationApi } from '@/api/notifications'
import { formatDate } from '@/utils/format'

export default {
  name: 'Notifications',
  components: {
    Setting,
    Message,
    Document,
    Trophy,
    Bell,
    Search,
    Refresh,
    Check,
    Delete,
    ArrowDown
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const notifications = ref([])
    const selectedNotifications = ref([])
    const unreadCount = ref(0)
    const showNotificationDialog = ref(false)
    const showSettingsDialog = ref(false)
    const viewingNotification = ref(null)
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      type: '',
      is_read: ''
    })
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 通知设置
    const settings = reactive({
      email_notifications: true,
      system_notifications: true,
      exam_notifications: true,
      score_notifications: true,
      announcement_notifications: true
    })
    
    // 方法
    const loadNotifications = async () => {
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
        
        const response = await notificationApi.getNotifications(params)
        notifications.value = response.data.items
        pagination.total = response.data.total
      } catch (error) {
        ElMessage.error('加载通知列表失败')
        console.error('Load notifications error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadUnreadCount = async () => {
      try {
        const response = await notificationApi.getUnreadCount()
        unreadCount.value = response.data.unread_count
      } catch (error) {
        console.error('Load unread count error:', error)
      }
    }
    
    const loadSettings = async () => {
      try {
        const response = await notificationApi.getNotificationSettings()
        Object.assign(settings, response.data)
      } catch (error) {
        console.error('Load settings error:', error)
      }
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadNotifications()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadNotifications()
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadNotifications()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadNotifications()
    }
    
    const handleSelectionChange = (selection) => {
      selectedNotifications.value = selection
    }
    
    const viewNotification = (notification) => {
      viewingNotification.value = notification
      showNotificationDialog.value = true
    }
    
    const markAsRead = async (notification) => {
      try {
        await notificationApi.markAsRead(notification.id)
        notification.is_read = true
        notification.read_at = new Date().toISOString()
        ElMessage.success('标记已读成功')
        loadUnreadCount()
      } catch (error) {
        ElMessage.error('标记已读失败')
        console.error('Mark as read error:', error)
      }
    }
    
    const handleAction = async (command, notification) => {
      switch (command) {
        case 'delete':
          await deleteNotification(notification)
          break
      }
    }
    
    const deleteNotification = async (notification) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除通知"${notification.title}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await notificationApi.deleteNotification(notification.id)
        ElMessage.success('删除通知成功')
        loadNotifications()
        loadUnreadCount()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除通知失败')
          console.error('Delete notification error:', error)
        }
      }
    }
    
    const batchMarkAsRead = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要标记选中的 ${selectedNotifications.value.length} 条通知为已读吗？`,
          '确认批量标记',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const notificationIds = selectedNotifications.value.map(n => n.id)
        await notificationApi.batchMarkAsRead({ notification_ids: notificationIds })
        
        ElMessage.success('批量标记已读成功')
        selectedNotifications.value = []
        loadNotifications()
        loadUnreadCount()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量标记已读失败')
          console.error('Batch mark as read error:', error)
        }
      }
    }
    
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedNotifications.value.length} 条通知吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const notificationIds = selectedNotifications.value.map(n => n.id)
        await notificationApi.batchDelete({ notification_ids: notificationIds })
        
        ElMessage.success('批量删除成功')
        selectedNotifications.value = []
        loadNotifications()
        loadUnreadCount()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    const updateSettings = async () => {
      try {
        await notificationApi.updateNotificationSettings(settings)
        ElMessage.success('设置更新成功')
      } catch (error) {
        ElMessage.error('设置更新失败')
        console.error('Update settings error:', error)
      }
    }
    
    const saveSettings = async () => {
      try {
        await notificationApi.updateNotificationSettings(settings)
        ElMessage.success('设置保存成功')
        showSettingsDialog.value = false
      } catch (error) {
        ElMessage.error('设置保存失败')
        console.error('Save settings error:', error)
      }
    }
    
    // 工具方法
    const getTypeLabel = (type) => {
      const labels = {
        system: '系统通知',
        exam: '考试通知',
        score: '成绩通知',
        announcement: '公告通知'
      }
      return labels[type] || type
    }
    
    const getTypeTagType = (type) => {
      const types = {
        system: 'primary',
        exam: 'success',
        score: 'warning',
        announcement: 'danger'
      }
      return types[type] || 'default'
    }
    
    // 生命周期
    onMounted(() => {
      loadNotifications()
      loadUnreadCount()
      loadSettings()
    })
    
    return {
      loading,
      notifications,
      selectedNotifications,
      unreadCount,
      showNotificationDialog,
      showSettingsDialog,
      viewingNotification,
      searchForm,
      pagination,
      settings,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewNotification,
      markAsRead,
      handleAction,
      batchMarkAsRead,
      batchDelete,
      updateSettings,
      saveSettings,
      getTypeLabel,
      getTypeTagType,
      formatDate
    }
  }
}
</script>

<style scoped>
.notifications {
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

.notification-settings {
  margin-bottom: 20px;
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.settings-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.settings-content {
  padding: 20px 0;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.setting-item:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.setting-item .el-icon {
  font-size: 20px;
}

.setting-item span {
  flex: 1;
  font-weight: 500;
}

.search-section {
  margin-bottom: 20px;
}

.notifications-list {
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

.notification-title {
  line-height: 1.5;
}

.unread-title {
  font-weight: 600;
  color: #303133;
}

.notification-meta {
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

.notification-detail {
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
  .notifications {
    padding: 15px;
  }
  
  .settings-content .el-col {
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
