<template>
  <div class="template-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ template.name }}</span>
          <el-tag type="success" v-if="template.is_public">公开</el-tag>
          <el-tag v-else>私有</el-tag>
        </div>
      </template>
      
      <div class="template-info">
        <p><strong>描述：</strong>{{ template.description }}</p>
        <p><strong>科目：</strong>{{ getSubjectName(template.subject_id) }}</p>
        <p><strong>使用次数：</strong>{{ template.usage_count }}</p>
        <p><strong>创建时间：</strong>{{ formatDate(template.created_at) }}</p>
      </div>
      
      <div class="template-config" v-if="template.template_config">
        <h4>模板配置：</h4>
        <pre>{{ JSON.stringify(template.template_config, null, 2) }}</pre>
      </div>
      
      <div class="template-actions">
        <el-button type="primary" @click="handleUse">使用模板</el-button>
        <el-button @click="handleEdit">编辑</el-button>
        <el-button type="danger" @click="handleDelete">删除</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

export default {
  name: 'TemplateView',
  props: {
    template: {
      type: Object,
      required: true
    },
    subjects: {
      type: Array,
      default: () => []
    }
  },
  emits: ['use', 'edit', 'delete'],
  setup(props, { emit }) {
    const getSubjectName = (subjectId) => {
      const subject = props.subjects.find(s => s.id === subjectId)
      return subject ? subject.name : '未知科目'
    }
    
    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
    }
    
    const handleUse = () => {
      emit('use', props.template)
    }
    
    const handleEdit = () => {
      emit('edit', props.template)
    }
    
    const handleDelete = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要删除这个模板吗？',
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        emit('delete', props.template)
        ElMessage.success('删除成功')
      } catch (error) {
        // 用户取消删除
      }
    }
    
    return {
      getSubjectName,
      formatDate,
      handleUse,
      handleEdit,
      handleDelete
    }
  }
}
</script>

<style scoped>
.template-view {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.template-info p {
  margin: 8px 0;
}

.template-config {
  margin: 20px 0;
}

.template-config pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}

.template-actions {
  margin-top: 20px;
  text-align: right;
}

.template-actions .el-button {
  margin-left: 10px;
}
</style>
