<template>
  <div class="modern-notifications-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Bell /></el-icon>
            </div>
            <div class="title-text">
              <h1>消息通知</h1>
              <p>管理和查看您的系统通知消息</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button @click="goBackToPersonalCenter" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回个人中心</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 通知设置区域 -->
    <div class="search-section">
      <div class="search-card">
        <div class="search-header">
          <h3>通知设置</h3>
          <p>管理您的通知偏好设置</p>
        </div>
        <div class="settings-content">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="setting-item">
                <div class="setting-icon">
                  <el-icon color="#409eff"><Message /></el-icon>
                </div>
                <div class="setting-text">
                  <span>系统通知</span>
                  <el-switch v-model="settings.system_notifications" @change="updateSettings" />
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="setting-item">
                <div class="setting-icon">
                  <el-icon color="#67c23a"><Document /></el-icon>
                </div>
                <div class="setting-text">
                  <span>考试通知</span>
                  <el-switch v-model="settings.exam_notifications" @change="updateSettings" />
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="setting-item">
                <div class="setting-icon">
                  <el-icon color="#e6a23c"><Trophy /></el-icon>
                </div>
                <div class="setting-text">
                  <span>成绩通知</span>
                  <el-switch v-model="settings.score_notifications" @change="updateSettings" />
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="setting-item">
                <div class="setting-icon">
                  <el-icon color="#f56c6c"><Bell /></el-icon>
                </div>
                <div class="setting-text">
                  <span>公告通知</span>
                  <el-switch v-model="settings.announcement_notifications" @change="updateSettings" />
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-section">
      <div class="search-card">
        <div class="search-header">
          <h3>搜索和筛选</h3>
          <p>快速查找通知信息</p>
        </div>
        <div class="search-form">
          <el-form :model="searchForm" inline>
            <el-form-item>
              <el-input
                v-model="searchForm.keyword"
                placeholder="请输入通知标题"
                prefix-icon="Search"
                class="search-input"
                clearable
              />
            </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.type" placeholder="选择类型" class="filter-select" clearable>
                <el-option label="全部类型" value="" />
                <el-option label="系统通知" value="system" />
                <el-option label="考试通知" value="exam" />
                <el-option label="成绩通知" value="score" />
                <el-option label="公告通知" value="announcement" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-select v-model="searchForm.is_read" placeholder="选择状态" class="filter-select" clearable>
                <el-option label="全部状态" value="" />
                <el-option label="未读" :value="false" />
                <el-option label="已读" :value="true" />
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

    <!-- 通知列表 -->
    <div class="table-section">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>通知列表</h3>
            <p>共 {{ pagination.total }} 条通知</p>
          </div>
          <div class="table-actions">
            <el-button 
              type="primary" 
              @click="batchMarkAsRead" 
              :disabled="selectedNotifications.length === 0"
              class="action-btn"
            >
              <el-icon><Check /></el-icon>
              <span>批量已读</span>
            </el-button>
            <el-button 
              type="danger" 
              @click="batchDelete" 
              :disabled="selectedNotifications.length === 0"
              class="action-btn"
            >
              <el-icon><Delete /></el-icon>
              <span>批量删除</span>
            </el-button>
          </div>
        </div>
        
        <div class="table-container">
          <el-table 
            :data="notifications" 
            stripe 
            class="modern-table"
            :loading="loading"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="title" label="通知标题" min-width="250">
              <template #default="{ row }">
                <div class="notification-info">
                  <div class="notification-title-wrapper">
                    <span :class="{ 'unread-title': !row.is_read }">{{ row.title }}</span>
                  </div>
                  <div class="notification-tags">
                    <el-tag :type="getTypeTagType(row.type)" size="small" class="type-tag">
                      {{ getTypeLabel(row.type) }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="content" label="通知内容" min-width="300" show-overflow-tooltip />
            <el-table-column prop="is_read" label="状态" width="100">
              <template #default="{ row }">
                <el-tag 
                  :type="row.is_read ? 'success' : 'warning'"
                  class="status-tag"
                >
                  {{ row.is_read ? '已读' : '未读' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="160">
              <template #default="{ row }">
                <span class="date-text">{{ formatDate(row.created_at) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="240" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" @click="viewNotification(row)" class="view-btn">
                    <el-icon><View /></el-icon>
                  </el-button>
                  <el-button 
                    size="small" 
                    type="primary" 
                    @click="markAsRead(row)" 
                    v-if="!row.is_read"
                    class="read-btn"
                  >
                    <el-icon><Check /></el-icon>
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteNotification(row)" class="delete-btn">
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

    <!-- 通知详情对话框 -->
    <el-dialog
      v-model="showNotificationDialog"
      title="通知详情"
      width="720px"
      :close-on-click-modal="false"
      class="modern-notification-dialog"
    >
      <div v-if="viewingNotification" class="dialog-content">
        <div class="notification-detail-header">
          <div class="detail-icon">
            <el-icon><Bell /></el-icon>
          </div>
          <div class="detail-title-section">
            <h3>{{ viewingNotification.title }}</h3>
            <div class="detail-tags">
              <el-tag :type="getTypeTagType(viewingNotification.type)" size="small">
                {{ getTypeLabel(viewingNotification.type) }}
              </el-tag>
              <el-tag :type="viewingNotification.is_read ? 'success' : 'warning'" size="small">
                {{ viewingNotification.is_read ? '已读' : '未读' }}
              </el-tag>
            </div>
          </div>
        </div>
        
        <div class="notification-detail-content">
          <div class="detail-time-info">
            <div class="time-item">
              <span class="time-label">创建时间：</span>
              <span class="time-value">{{ formatDate(viewingNotification.created_at) }}</span>
            </div>
            <div class="time-item" v-if="viewingNotification.read_at">
              <span class="time-label">阅读时间：</span>
              <span class="time-value">{{ formatDate(viewingNotification.read_at) }}</span>
            </div>
          </div>
          
          <div class="content-section">
            <h4>通知内容</h4>
            <div class="content-text">
              {{ viewingNotification.content }}
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showNotificationDialog = false" size="large">
            <el-icon><Close /></el-icon>
            关闭
          </el-button>
          <el-button 
            type="primary" 
            @click="markAsRead(viewingNotification)" 
            v-if="viewingNotification && !viewingNotification.is_read"
            size="large"
          >
            <el-icon><Check /></el-icon>
            标记已读
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
  Message, Document, Trophy, Bell, Search, Refresh, Check, Delete, ArrowLeft, View, Close
} from '@element-plus/icons-vue'
import { notificationApi } from '@/api/notifications'
import { formatDate } from '@/utils/format'

export default {
  name: 'Notifications',
  components: {
    Message,
    Document,
    Trophy,
    Bell,
    Search,
    Refresh,
    Check,
    Delete,
    View,
    Close
  },
  setup() {
    const router = useRouter()
    
    // 响应式数据
    const loading = ref(false)
    const notifications = ref([])
    const selectedNotifications = ref([])
    const showNotificationDialog = ref(false)
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
      system_notifications: true,
      exam_notifications: true,
      score_notifications: true,
      announcement_notifications: true
    })
    
    // 返回个人中心
    const goBackToPersonalCenter = () => {
      router.push('/user/dashboard')
    }
    
    // 加载通知列表
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
    
    // 加载通知设置
    const loadSettings = async () => {
      try {
        const response = await notificationApi.getNotificationSettings()
        Object.assign(settings, response.data)
      } catch (error) {
        console.error('Load settings error:', error)
      }
    }
    
    // 搜索
    const handleSearch = () => {
      pagination.page = 1
      loadNotifications()
    }
    
    // 重置
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.page = 1
      loadNotifications()
    }
    
    // 分页变化
    const handlePageChange = (page) => {
      pagination.page = page
      loadNotifications()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadNotifications()
    }
    
    // 选择变化
    const handleSelectionChange = (selection) => {
      selectedNotifications.value = selection
    }
    
    // 查看通知
    const viewNotification = (notification) => {
      viewingNotification.value = notification
      showNotificationDialog.value = true
      
      // 如果是未读通知，自动标记为已读
      if (!notification.is_read) {
        markAsRead(notification)
      }
    }
    
    // 标记已读
    const markAsRead = async (notification) => {
      try {
        await notificationApi.markAsRead(notification.id)
        notification.is_read = true
        notification.read_at = new Date().toISOString()
        ElMessage.success('标记已读成功')
        
        // 如果对话框打开，关闭它
        if (showNotificationDialog.value) {
          showNotificationDialog.value = false
        }
      } catch (error) {
        ElMessage.error('标记已读失败')
        console.error('Mark as read error:', error)
      }
    }
    
    // 删除通知
    const deleteNotification = async (notification) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除通知"${notification.title}"吗？此操作不可恢复！`,
          '确认删除',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await notificationApi.deleteNotification(notification.id)
        ElMessage.success('删除通知成功')
        loadNotifications()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除通知失败')
          console.error('Delete notification error:', error)
        }
      }
    }
    
    // 批量标记已读
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
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量标记已读失败')
          console.error('Batch mark as read error:', error)
        }
      }
    }
    
    // 批量删除
    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedNotifications.value.length} 条通知吗？此操作不可恢复！`,
          '确认批量删除',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const notificationIds = selectedNotifications.value.map(n => n.id)
        await notificationApi.batchDelete({ notification_ids: notificationIds })
        
        ElMessage.success('批量删除成功')
        selectedNotifications.value = []
        loadNotifications()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
          console.error('Batch delete error:', error)
        }
      }
    }
    
    // 更新设置
    const updateSettings = async () => {
      try {
        await notificationApi.updateNotificationSettings(settings)
        ElMessage.success('设置更新成功')
      } catch (error) {
        ElMessage.error('设置更新失败')
        console.error('Update settings error:', error)
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
      loadSettings()
    })
    
    return {
      loading,
      notifications,
      selectedNotifications,
      showNotificationDialog,
      viewingNotification,
      searchForm,
      pagination,
      settings,
      goBackToPersonalCenter,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleSelectionChange,
      viewNotification,
      markAsRead,
      deleteNotification,
      batchMarkAsRead,
      batchDelete,
      updateSettings,
      getTypeLabel,
      getTypeTagType,
      formatDate,
      ArrowLeft
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-notifications-management {
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
      
      .back-btn {
        padding: 12px 20px;
        font-weight: 600;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
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

.search-section {
  padding: 32px;
  
  .search-card {
    max-width: 1800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    margin-bottom: 32px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
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
    
    .settings-content {
      .setting-item {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 16px;
        padding: 24px;
        display: flex;
        align-items: center;
        gap: 20px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        
        &::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
          opacity: 0;
          transition: opacity 0.3s ease;
        }
        
        &:hover {
          border-color: #667eea;
          transform: translateY(-4px);
          box-shadow: 0 12px 32px rgba(102, 126, 234, 0.15);
          
          &::before {
            opacity: 1;
          }
          
          .setting-icon {
            transform: scale(1.1);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
          }
        }
        
        .setting-icon {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
          font-size: 22px;
          position: relative;
          z-index: 1;
          transition: all 0.3s ease;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }
        
        .setting-text {
          flex: 1;
          display: flex;
          justify-content: space-between;
          align-items: center;
          position: relative;
          z-index: 1;
          
          span {
            font-weight: 700;
            color: #1a1a1a;
            font-size: 15px;
            letter-spacing: 0.5px;
          }
          
          :deep(.el-switch) {
            --el-switch-on-color: #667eea;
            --el-switch-off-color: #e9ecef;
            
            .el-switch__core {
              border-radius: 20px;
              height: 24px;
              min-width: 48px;
              border: 2px solid transparent;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            
            .el-switch__action {
              width: 20px;
              height: 20px;
              border-radius: 50%;
              box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
            }
          }
        }
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
      
      .table-actions {
        display: flex;
        gap: 12px;
        
        .action-btn {
          padding: 10px 20px;
          border-radius: 12px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 6px;
          
          &.el-button--primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            
            &:hover:not(:disabled) {
              transform: translateY(-2px);
              box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            }
          }
          
          &.el-button--danger {
            background: #fee;
            border-color: #fcc;
            color: #d32f2f;
            
            &:hover:not(:disabled) {
              background: #fcc;
              transform: translateY(-2px);
            }
          }
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
        
        .notification-info {
          .notification-title-wrapper {
            margin-bottom: 8px;
            
            .unread-title {
              font-weight: 700;
              color: #1a1a1a;
            }
          }
          
          .notification-tags {
            display: flex;
            gap: 8px;
            
            .type-tag {
              border-radius: 8px;
              font-weight: 600;
              padding: 4px 12px;
            }
          }
        }
        
        .status-tag {
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
            
            &.view-btn {
              background: #e3f2fd;
              border-color: #bbdefb;
              color: #1976d2;
              
              &:hover {
                background: #bbdefb;
                transform: translateY(-1px);
              }
            }
            
            &.read-btn {
              background: #e8f5e9;
              border-color: #c8e6c9;
              color: #4caf50;
              
              &:hover {
                background: #c8e6c9;
                transform: translateY(-1px);
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

/* 通知详情对话框 */
.modern-notification-dialog :deep(.el-dialog) {
  border-radius: 20px;
  overflow: visible;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.modern-notification-dialog :deep(.el-dialog__header) {
  background: transparent;
  color: #1f2937;
  padding: 32px 40px 0 40px;
  margin: 0;
  border-bottom: none;
}

.modern-notification-dialog :deep(.el-dialog__title) {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.modern-notification-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.dialog-content {
  padding: 40px;
  background: rgba(255, 255, 255, 0.5);
}

.notification-detail-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;
  padding: 24px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 16px;
  border: 1px solid rgba(102, 126, 234, 0.1);
  
  .detail-icon {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 28px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  }
  
  .detail-title-section {
    flex: 1;
    
    h3 {
      margin: 0 0 12px 0;
      font-size: 20px;
      font-weight: 700;
      color: #1f2937;
    }
    
    .detail-tags {
      display: flex;
      gap: 10px;
    }
  }
}

.notification-detail-content {
  .detail-time-info {
    display: flex;
    gap: 32px;
    margin-bottom: 24px;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 12px;
    
    .time-item {
      display: flex;
      gap: 8px;
      
      .time-label {
        color: #6b7280;
        font-weight: 600;
      }
      
      .time-value {
        color: #1f2937;
      }
    }
  }
  
  .content-section {
    h4 {
      margin: 0 0 16px 0;
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
    }
    
    .content-text {
      padding: 20px;
      background: #f8f9fa;
      border-radius: 12px;
      border-left: 4px solid #667eea;
      line-height: 1.8;
      color: #374151;
      font-size: 15px;
    }
  }
}

.modern-notification-dialog :deep(.el-dialog__footer) {
  background: rgba(248, 250, 252, 0.8);
  padding: 32px 40px;
  border-top: 1px solid rgba(229, 231, 235, 0.5);
  backdrop-filter: blur(10px);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  
  .el-button {
    border-radius: 12px;
    font-weight: 600;
    padding: 14px 28px;
    font-size: 14px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: none;
    
    &:not(.el-button--primary) {
      background: rgba(255, 255, 255, 0.8);
      color: #6b7280;
      border: 1px solid rgba(209, 213, 219, 0.6);
      backdrop-filter: blur(10px);
      
      &:hover {
        background: rgba(255, 255, 255, 0.9);
        color: #374151;
        border-color: rgba(156, 163, 175, 0.8);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
      }
    }
    
    &.el-button--primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      box-shadow: 
        0 4px 16px rgba(102, 126, 234, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
      
      &:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-2px);
        box-shadow: 
          0 8px 25px rgba(102, 126, 234, 0.4),
          inset 0 1px 0 rgba(255, 255, 255, 0.2);
      }
    }
  }
}

/* 响应式设计 */
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
      
      .settings-content {
        .el-col {
          margin-bottom: 16px;
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
  
  .notification-detail-header {
    flex-direction: column;
    text-align: center;
  }
  
  .detail-time-info {
    flex-direction: column;
    gap: 16px !important;
  }
}
</style>
