<template>
  <div class="permission-management">
    <div class="page-header">
      <h1>权限管理</h1>
      <div class="header-info">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新建权限
        </el-button>
        <el-button @click="initPermissions">
          <el-icon><Refresh /></el-icon>
          初始化权限
        </el-button>
      </div>
    </div>

    <!-- 权限树 -->
    <div class="permission-tree">
      <el-card>
        <div class="tree-header">
          <h3>权限树</h3>
          <div class="tree-actions">
            <el-button size="small" @click="expandAll">
              <el-icon><ArrowDown /></el-icon>
              展开全部
            </el-button>
            <el-button size="small" @click="collapseAll">
              <el-icon><ArrowUp /></el-icon>
              收起全部
            </el-button>
          </div>
        </div>
        <el-tree
          ref="permissionTreeRef"
          :data="permissionTree"
          :props="treeProps"
          node-key="id"
          :default-expand-all="false"
          :expand-on-click-node="false"
          show-checkbox
          @check="handleTreeCheck"
        >
          <template #default="{ data }">
            <div class="tree-node">
              <div class="node-content">
                <el-icon v-if="data.icon" :color="getTypeColor(data.type)">
                  <component :is="data.icon" />
                </el-icon>
                <span class="node-label">{{ data.label }}</span>
                <el-tag :type="getTypeTagType(data.type)" size="small">
                  {{ getTypeLabel(data.type) }}
                </el-tag>
              </div>
              <div class="node-actions">
                <el-button size="small" @click.stop="editPermission(data)">
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button size="small" type="danger" @click.stop="deletePermission(data)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </template>
        </el-tree>
      </el-card>
    </div>

    <!-- 角色权限设置 -->
    <div class="role-permissions">
      <el-card>
        <div class="role-header">
          <h3>角色权限设置</h3>
        </div>
        <div class="role-content">
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="role-section">
                <h4>管理员权限</h4>
                <el-tree
                  ref="adminTreeRef"
                  :data="permissionTree"
                  :props="treeProps"
                  node-key="id"
                  :default-expand-all="true"
                  show-checkbox
                  @check="handleRoleCheck('admin', $event)"
                />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="role-section">
                <h4>普通用户权限</h4>
                <el-tree
                  ref="userTreeRef"
                  :data="permissionTree"
                  :props="treeProps"
                  node-key="id"
                  :default-expand-all="true"
                  show-checkbox
                  @check="handleRoleCheck('user', $event)"
                />
              </div>
            </el-col>
          </el-row>
        </div>
        <div class="role-actions">
          <el-button type="primary" @click="saveRolePermissions">
            <el-icon><Check /></el-icon>
            保存权限设置
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 权限列表 -->
    <div class="permissions-list">
      <el-card>
        <div class="list-header">
          <div class="list-title">
            <span>权限列表</span>
          </div>
          <div class="list-actions">
            <el-button size="small" @click="loadPermissions">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>

        <el-table
          :data="permissions"
          :loading="loading"
          row-key="id"
          stripe
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="权限名称" min-width="150" />
          <el-table-column prop="code" label="权限代码" min-width="150" />
          <el-table-column prop="type" label="类型" width="120">
            <template #default="{ row }">
              <el-tag :type="getTypeTagType(row.type)" size="small">
                {{ getTypeLabel(row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="path" label="路径" min-width="200" show-overflow-tooltip />
          <el-table-column prop="sort_order" label="排序" width="80" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
                {{ row.status === 'active' ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="editPermission(row)">
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="deletePermission(row)">
                删除
              </el-button>
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

    <!-- 创建/编辑权限对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingPermission ? '编辑权限' : '新建权限'"
      width="600px"
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
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Refresh, ArrowDown, ArrowUp, Edit, Delete, Check,
  User, Book, QuestionFilled, Document, Lock, Setting
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
    Setting
  },
  setup() {
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
      initPermissions,
      getTypeLabel,
      getTypeTagType,
      getTypeColor
    }
  }
}
</script>

<style scoped>
.permission-management {
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

.permission-tree {
  margin-bottom: 20px;
}

.tree-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tree-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.tree-actions {
  display: flex;
  gap: 10px;
}

.tree-node {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.node-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.node-label {
  font-weight: 500;
  color: #303133;
}

.node-actions {
  display: flex;
  gap: 5px;
}

.role-permissions {
  margin-bottom: 20px;
}

.role-header {
  margin-bottom: 20px;
}

.role-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.role-content {
  margin-bottom: 20px;
}

.role-section {
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.role-section h4 {
  margin: 0 0 15px 0;
  color: #606266;
  font-size: 16px;
}

.role-actions {
  text-align: center;
}

.permissions-list {
  margin-bottom: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.list-title {
  font-size: 16px;
  font-weight: 500;
}

.list-actions {
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

:deep(.el-tree-node__content) {
  height: 40px;
}

:deep(.el-tree-node__label) {
  font-size: 14px;
}

:deep(.el-table .el-table__row) {
  cursor: pointer;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f7fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .permission-management {
    padding: 15px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .role-content .el-col {
    margin-bottom: 20px;
  }
  
  .tree-header {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
