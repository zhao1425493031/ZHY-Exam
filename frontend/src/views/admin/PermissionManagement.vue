<template>
  <div class="modern-permission-management">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><Lock /></el-icon>
            </div>
            <div class="title-text">
              <h1>权限管理</h1>
              <p>管理系统权限和角色配置</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="showCreateDialog = true" class="add-btn">
            <el-icon><Plus /></el-icon>
            <span>新建权限</span>
          </el-button>
          <el-button @click="initPermissions" class="init-btn">
            <el-icon><Refresh /></el-icon>
            <span>初始化权限</span>
          </el-button>
          <el-button @click="$router.push('/admin')" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回控制台</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 权限树 -->
    <div class="tree-section">
      <div class="tree-card">
        <div class="tree-header">
          <div class="tree-title">
            <h3>权限树</h3>
            <p>权限层级结构管理</p>
          </div>
          <div class="tree-actions">
            <el-button size="small" @click="expandAll" class="expand-btn">
              <el-icon><ArrowDown /></el-icon>
              <span>展开全部</span>
            </el-button>
            <el-button size="small" @click="collapseAll" class="collapse-btn">
              <el-icon><ArrowUp /></el-icon>
              <span>收起全部</span>
            </el-button>
          </div>
        </div>
        <div class="tree-container">
          <el-tree
            ref="permissionTreeRef"
            :data="permissionTree"
            :props="treeProps"
            node-key="id"
            :default-expand-all="false"
            :expand-on-click-node="false"
            show-checkbox
            @check="handleTreeCheck"
            class="modern-tree"
          >
            <template #default="{ data }">
              <div class="tree-node">
                <div class="node-content">
                  <el-icon v-if="data.icon" :color="getTypeColor(data.type)" class="node-icon">
                    <component :is="data.icon" />
                  </el-icon>
                  <span class="node-label">{{ data.label }}</span>
                  <el-tag :type="getTypeTagType(data.type)" size="small" class="type-tag">
                    {{ getTypeLabel(data.type) }}
                  </el-tag>
                </div>
                <div class="node-actions">
                  <el-button size="small" @click.stop="editPermission(data)" class="action-btn edit-btn">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button size="small" type="danger" @click.stop="deletePermission(data)" class="action-btn delete-btn">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>
          </el-tree>
        </div>
      </div>
    </div>

    <!-- 角色权限设置 -->
    <div class="role-section">
      <div class="role-card">
        <div class="role-header">
          <div class="role-title">
            <h3>角色权限设置</h3>
            <p>为不同角色分配权限</p>
          </div>
          <div class="role-actions">
            <el-button type="primary" @click="saveRolePermissions" class="save-btn">
              <el-icon><Check /></el-icon>
              <span>保存权限设置</span>
            </el-button>
          </div>
        </div>
        
        <div class="role-content">
          <div class="role-grid">
            <div class="role-panel">
              <div class="role-panel-header">
                <div class="role-avatar admin-avatar">
                  <el-icon><Setting /></el-icon>
                </div>
                <div class="role-info">
                  <h4>管理员权限</h4>
                  <p>系统管理员权限配置</p>
                </div>
              </div>
              <div class="role-tree-container">
                <el-tree
                  ref="adminTreeRef"
                  :data="permissionTree"
                  :props="treeProps"
                  node-key="id"
                  :default-expand-all="true"
                  show-checkbox
                  @check="handleRoleCheck('admin', $event)"
                  class="role-tree"
                />
              </div>
            </div>
            
            <div class="role-panel">
              <div class="role-panel-header">
                <div class="role-avatar user-avatar">
                  <el-icon><User /></el-icon>
                </div>
                <div class="role-info">
                  <h4>普通用户权限</h4>
                  <p>普通用户权限配置</p>
                </div>
              </div>
              <div class="role-tree-container">
                <el-tree
                  ref="userTreeRef"
                  :data="permissionTree"
                  :props="treeProps"
                  node-key="id"
                  :default-expand-all="true"
                  show-checkbox
                  @check="handleRoleCheck('user', $event)"
                  class="role-tree"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 权限列表 -->
    <div class="table-section">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>权限列表</h3>
            <p>所有权限的详细信息</p>
          </div>
          <div class="table-actions">
            <el-button @click="loadPermissions" class="refresh-btn" :loading="loading">
              <el-icon><Refresh /></el-icon>
              <span>刷新</span>
            </el-button>
          </div>
        </div>
        
        <div class="table-container">
          <el-table
            :data="permissions"
            :loading="loading"
            row-key="id"
            stripe
            class="modern-table"
          >
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="权限名称" min-width="150">
              <template #default="{ row }">
                <div class="permission-info">
                  <div class="permission-icon">
                    <el-icon v-if="row.icon" :color="getTypeColor(row.type)">
                      <component :is="row.icon" />
                    </el-icon>
                  </div>
                  <div class="permission-details">
                    <div class="permission-name">{{ row.name }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="code" label="权限代码" min-width="150" />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getTypeTagType(row.type)" size="small" class="type-tag">
                  {{ getTypeLabel(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="path" label="路径" min-width="200" show-overflow-tooltip />
            <el-table-column prop="sort_order" label="排序" width="80" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small" class="status-tag">
                  {{ row.status === 'active' ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" @click="editPermission(row)" class="action-btn edit-btn">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button size="small" type="danger" @click="deletePermission(row)" class="action-btn delete-btn">
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

    <!-- 创建/编辑权限对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingPermission ? '编辑权限' : '新建权限'"
      width="60%"
      :before-close="handleCloseDialog"
      class="modern-permission-dialog"
    >
      <el-form :model="permissionForm" :rules="permissionRules" ref="permissionFormRef" label-width="100px">
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="permissionForm.name" placeholder="请输入权限名称" />
        </el-form-item>
        <el-form-item label="权限代码" prop="code">
          <el-input v-model="permissionForm.code" placeholder="请输入权限代码" />
        </el-form-item>
        <el-form-item label="权限类型" prop="type">
          <el-select v-model="permissionForm.type" placeholder="选择权限类型">
            <el-option label="菜单权限" value="menu" />
            <el-option label="按钮权限" value="button" />
            <el-option label="API权限" value="api" />
            <el-option label="数据权限" value="data" />
          </el-select>
        </el-form-item>
        <el-form-item label="父权限">
          <el-tree-select
            v-model="permissionForm.parent_id"
            :data="permissionTree"
            :props="treeProps"
            placeholder="选择父权限"
            clearable
          />
        </el-form-item>
        <el-form-item label="路径">
          <el-input v-model="permissionForm.path" placeholder="请输入路径" />
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="permissionForm.icon" placeholder="请输入图标名称" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="permissionForm.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="permissionForm.status" placeholder="选择状态">
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="savePermission">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Refresh, ArrowDown, ArrowUp, Edit, Delete, Check,
  User, Book, QuestionFilled, Document, Lock, Setting, ArrowLeft
} from '@element-plus/icons-vue'
import { permissionApi } from '@/api/permissions'

export default {
  name: 'PermissionManagement',
  components: {
    Plus,
    Refresh,
    ArrowDown,
    ArrowUp,
    Edit,
    Delete,
    Check,
    User,
    Book,
    QuestionFilled,
    Document,
    Lock,
    Setting,
    ArrowLeft
  },
  setup() {
    const router = useRouter()
    // 响应式数据
    const loading = ref(false)
    const permissions = ref([])
    const permissionTree = ref([])
    const showCreateDialog = ref(false)
    const editingPermission = ref(null)
    const permissionTreeRef = ref(null)
    const adminTreeRef = ref(null)
    const userTreeRef = ref(null)
    
    // 分页
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    // 权限表单
    const permissionForm = reactive({
      name: '',
      code: '',
      type: 'menu',
      parent_id: 0,
      path: '',
      icon: '',
      sort_order: 0,
      status: 'active'
    })
    
    const permissionRules = {
      name: [
        { required: true, message: '请输入权限名称', trigger: 'blur' }
      ],
      code: [
        { required: true, message: '请输入权限代码', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择权限类型', trigger: 'change' }
      ]
    }
    
    // 树形组件配置
    const treeProps = {
      children: 'children',
      label: 'label',
      value: 'value'
    }
    
    // 方法
    const loadPermissions = async () => {
      try {
        loading.value = true
        const params = {
          page: pagination.page,
          size: pagination.size
        }
        
        const response = await permissionApi.getPermissions(params)
        permissions.value = response.data.items
        pagination.total = response.data.total
      } catch (error) {
        ElMessage.error('加载权限列表失败')
        console.error('Load permissions error:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadPermissionTree = async () => {
      try {
        const response = await permissionApi.getPermissionTree()
        permissionTree.value = response.data
      } catch (error) {
        ElMessage.error('加载权限树失败')
        console.error('Load permission tree error:', error)
      }
    }
    
    const loadRolePermissions = async () => {
      try {
        // 加载管理员权限
        const adminResponse = await permissionApi.getRolePermissions('admin')
        const adminPermissionIds = adminResponse.data.map(p => p.permission_id)
        adminTreeRef.value?.setCheckedKeys(adminPermissionIds)
        
        // 加载普通用户权限
        const userResponse = await permissionApi.getRolePermissions('user')
        const userPermissionIds = userResponse.data.map(p => p.permission_id)
        userTreeRef.value?.setCheckedKeys(userPermissionIds)
      } catch (error) {
        console.error('Load role permissions error:', error)
      }
    }
    
    const handlePageChange = (page) => {
      pagination.page = page
      loadPermissions()
    }
    
    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadPermissions()
    }
    
    const expandAll = () => {
      permissionTreeRef.value?.setExpandedKeys(getAllKeys(permissionTree.value))
    }
    
    const collapseAll = () => {
      permissionTreeRef.value?.setExpandedKeys([])
    }
    
    const getAllKeys = (tree) => {
      const keys = []
      const traverse = (nodes) => {
        nodes.forEach(node => {
          keys.push(node.id)
          if (node.children) {
            traverse(node.children)
          }
        })
      }
      traverse(tree)
      return keys
    }
    
    const handleTreeCheck = (data, checked) => {
      console.log('Tree check:', data, checked)
    }
    
    const handleRoleCheck = (role, data) => {
      console.log('Role check:', role, data)
    }
    
    const editPermission = (permission) => {
      editingPermission.value = permission
      Object.assign(permissionForm, {
        name: permission.name,
        code: permission.code,
        type: permission.type,
        parent_id: permission.parent_id,
        path: permission.path,
        icon: permission.icon,
        sort_order: permission.sort_order,
        status: permission.status
      })
      showCreateDialog.value = true
    }
    
    const deletePermission = async (permission) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除权限"${permission.name}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await permissionApi.deletePermission(permission.id)
        ElMessage.success('删除权限成功')
        loadPermissions()
        loadPermissionTree()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除权限失败')
          console.error('Delete permission error:', error)
        }
      }
    }
    
    const savePermission = async () => {
      try {
        if (editingPermission.value) {
          await permissionApi.updatePermission(editingPermission.value.id, permissionForm)
          ElMessage.success('更新权限成功')
        } else {
          await permissionApi.createPermission(permissionForm)
          ElMessage.success('创建权限成功')
        }
        
        showCreateDialog.value = false
        editingPermission.value = null
        Object.keys(permissionForm).forEach(key => {
          permissionForm[key] = key === 'type' ? 'menu' : key === 'status' ? 'active' : key === 'sort_order' ? 0 : ''
        })
        loadPermissions()
        loadPermissionTree()
      } catch (error) {
        ElMessage.error('保存权限失败')
        console.error('Save permission error:', error)
      }
    }
    
    const saveRolePermissions = async () => {
      try {
        // 获取管理员选中的权限
        const adminCheckedKeys = adminTreeRef.value?.getCheckedKeys() || []
        await permissionApi.setRolePermissions('admin', { permission_ids: adminCheckedKeys })
        
        // 获取普通用户选中的权限
        const userCheckedKeys = userTreeRef.value?.getCheckedKeys() || []
        await permissionApi.setRolePermissions('user', { permission_ids: userCheckedKeys })
        
        ElMessage.success('保存权限设置成功')
      } catch (error) {
        ElMessage.error('保存权限设置失败')
        console.error('Save role permissions error:', error)
      }
    }
    
    const handleCloseDialog = () => {
      showCreateDialog.value = false
      editingPermission.value = null
      Object.keys(permissionForm).forEach(key => {
        permissionForm[key] = key === 'type' ? 'menu' : key === 'status' ? 'active' : key === 'sort_order' ? 0 : ''
      })
    }
    
    const initPermissions = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要初始化权限数据吗？这将创建默认的权限配置。',
          '确认初始化',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await permissionApi.initPermissions()
        ElMessage.success('初始化权限数据成功')
        loadPermissions()
        loadPermissionTree()
        loadRolePermissions()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('初始化权限数据失败')
          console.error('Init permissions error:', error)
        }
      }
    }
    
    // 工具方法
    const getTypeLabel = (type) => {
      const labels = {
        menu: '菜单权限',
        button: '按钮权限',
        api: 'API权限',
        data: '数据权限'
      }
      return labels[type] || type
    }
    
    const getTypeTagType = (type) => {
      const types = {
        menu: 'primary',
        button: 'success',
        api: 'warning',
        data: 'info'
      }
      return types[type] || 'default'
    }
    
    const getTypeColor = (type) => {
      const colors = {
        menu: '#409eff',
        button: '#67c23a',
        api: '#e6a23c',
        data: '#909399'
      }
      return colors[type] || '#909399'
    }
    
    // 生命周期
    onMounted(() => {
      loadPermissions()
      loadPermissionTree()
      loadRolePermissions()
    })
    
    return {
      loading,
      permissions,
      permissionTree,
      showCreateDialog,
      editingPermission,
      permissionTreeRef,
      adminTreeRef,
      userTreeRef,
      pagination,
      permissionForm,
      permissionRules,
      treeProps,
      loadPermissions,
      handlePageChange,
      handleSizeChange,
      expandAll,
      collapseAll,
      handleTreeCheck,
      handleRoleCheck,
      editPermission,
      deletePermission,
      savePermission,
      saveRolePermissions,
      handleCloseDialog,
      initPermissions,
      getTypeLabel,
      getTypeTagType,
      getTypeColor
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-permission-management {
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
          }
        }
      }
    }
    
    .header-right {
      display: flex;
      gap: 12px;
      
      .add-btn, .init-btn {
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        border: none;
        
        &:hover {
          transform: translateY(-2px);
        }
      }
      
      .add-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
        
        &:hover {
          box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }
      }
      
      .init-btn {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
        
        &:hover {
          box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        }
      }
      
      .back-btn {
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        transition: all 0.3s ease;
        
        &:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-2px);
        }
      }
    }
  }
}

.tree-section {
  padding: 32px 32px 0;
  
  .tree-card {
    max-width: 1800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    
    .tree-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      
      .tree-title {
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
      
      .tree-actions {
        display: flex;
        gap: 8px;
        
        .expand-btn, .collapse-btn {
          padding: 10px 20px;
          border-radius: 12px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 6px;
          background: #f8f9fa;
          border-color: #e9ecef;
          color: #6c757d;
          transition: all 0.3s ease;
          
          &:hover {
            background: #e9ecef;
            transform: translateY(-2px);
          }
        }
      }
    }
    
    .tree-container {
      .modern-tree {
        :deep(.el-tree-node__content) {
          height: 40px;
          border-radius: 8px;
          margin-bottom: 4px;
          transition: all 0.3s ease;
          
          &:hover {
            background: rgba(102, 126, 234, 0.05);
          }
        }
        
        .tree-node {
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
          
          .node-content {
            display: flex;
            align-items: center;
            gap: 12px;
            
            .node-icon {
              font-size: 16px;
            }
            
            .node-label {
              font-weight: 500;
              color: #1a1a1a;
            }
            
            .type-tag {
              font-size: 12px;
            }
          }
          
          .node-actions {
            display: flex;
            gap: 4px;
            
            .action-btn {
              padding: 6px 12px;
              border-radius: 8px;
              transition: all 0.3s ease;
              
              &.edit-btn {
                background: #e3f2fd;
                border-color: #bbdefb;
                color: #1976d2;
                
                &:hover {
                  background: #bbdefb;
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
    }
  }
}

.role-section {
  padding: 32px;
  
  .role-card {
    max-width: 1800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    
    .role-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      
      .role-title {
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
      
      .save-btn {
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
      }
    }
    
    .role-content {
      .role-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 24px;
        
        .role-panel {
          background: rgba(248, 250, 252, 0.8);
          border-radius: 16px;
          padding: 24px;
          border: 1px solid rgba(226, 232, 240, 0.8);
          transition: all 0.3s ease;
          
          &:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
          }
          
          .role-panel-header {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 20px;
            
            .role-avatar {
              width: 50px;
              height: 50px;
              border-radius: 16px;
              display: flex;
              align-items: center;
              justify-content: center;
              box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
              
              .el-icon {
                font-size: 24px;
                color: white;
              }
              
              &.admin-avatar {
                background: linear-gradient(135deg, #667eea, #764ba2);
              }
              
              &.user-avatar {
                background: linear-gradient(135deg, #4facfe, #00f2fe);
              }
            }
            
            .role-info {
              h4 {
                margin: 0 0 4px 0;
                font-size: 18px;
                font-weight: 600;
                color: #1a1a1a;
              }
              
              p {
                margin: 0;
                font-size: 14px;
                color: #666;
              }
            }
          }
          
          .role-tree-container {
            .role-tree {
              max-height: 400px;
              overflow-y: auto;
              
              :deep(.el-tree-node__content) {
                height: 36px;
                border-radius: 6px;
                margin-bottom: 2px;
                transition: all 0.3s ease;
                
                &:hover {
                  background: rgba(102, 126, 234, 0.05);
                }
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
      
      .refresh-btn {
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        background: #f8f9fa;
        border-color: #e9ecef;
        color: #6c757d;
        transition: all 0.3s ease;
        
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
        
        .permission-info {
          display: flex;
          align-items: center;
          gap: 12px;
          
          .permission-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            
            .el-icon {
              font-size: 16px;
              color: white;
            }
          }
          
          .permission-details {
            .permission-name {
              font-weight: 600;
              color: #1a1a1a;
            }
          }
        }
        
        .action-buttons {
          display: flex;
          gap: 8px;
          
          .action-btn {
            padding: 6px 12px;
            border-radius: 8px;
            transition: all 0.3s ease;
            
            &.edit-btn {
              background: #e3f2fd;
              border-color: #bbdefb;
              color: #1976d2;
              
              &:hover {
                background: #bbdefb;
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
    
    .pagination-wrapper {
      margin-top: 24px;
      display: flex;
      justify-content: center;
      
      .modern-pagination {
        :deep(.el-pagination) {
          .el-pager li {
            border-radius: 8px;
            margin: 0 2px;
            transition: all 0.3s ease;
            
            &:hover {
              background: rgba(102, 126, 234, 0.1);
              transform: translateY(-1px);
            }
            
            &.is-active {
              background: linear-gradient(135deg, #667eea, #764ba2);
              color: white;
            }
          }
          
          .btn-prev, .btn-next {
            border-radius: 8px;
            transition: all 0.3s ease;
            
            &:hover {
              background: rgba(102, 126, 234, 0.1);
              transform: translateY(-1px);
            }
          }
        }
      }
    }
  }
}

// 对话框样式
:deep(.modern-permission-dialog) {
  .el-dialog {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  }
  
  .el-dialog__header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 24px 32px;
    border-bottom: none;
    
    .el-dialog__title {
      color: white;
      font-weight: 700;
      font-size: 18px;
    }
  }
  
  .el-dialog__body {
    padding: 32px;
  }
  
  .el-dialog__footer {
    padding: 0 32px 32px;
    text-align: right;
    
    .el-button {
      border-radius: 12px;
      padding: 12px 24px;
      font-weight: 600;
      transition: all 0.3s ease;
      
      &:not(.el-button--primary) {
        background: #f8f9fa;
        border-color: #e9ecef;
        color: #6c757d;
        
        &:hover {
          background: #e9ecef;
          transform: translateY(-2px);
        }
      }
      
      &.el-button--primary {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border: none;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
      }
    }
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .modern-header .header-content,
  .tree-section,
  .role-section,
  .table-section {
    padding-left: 20px;
    padding-right: 20px;
  }
  
  .role-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .modern-header .header-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .tree-header, .role-header, .table-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .tree-card, .role-card, .table-card {
    padding: 20px;
  }
}
</style>
